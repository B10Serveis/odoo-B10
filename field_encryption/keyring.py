import fcntl
import json
import os
import stat
import tempfile
from functools import lru_cache

from cryptography.fernet import Fernet, MultiFernet
from odoo.tools import config


KEY_PATH_PARAMETER = 'field_encryption.key_path'
KEY_FILENAME = 'field_encryption.key'
LEGACY_DEFAULT_KEY = '8Rr9SfNkzmJj-EqW4YPaQlCqBxbD_1Z7mjL8QOHAPuA=='


def default_key_path():
    """Return the shared key path beside the active Odoo configuration file."""
    config_file = config.rcfile
    if not config_file:
        raise RuntimeError('Odoo configuration file path is unavailable')
    return os.path.join(os.path.dirname(os.path.abspath(config_file)), KEY_FILENAME)


def _read_keyring(key_path):
    if os.path.islink(key_path):
        raise RuntimeError('field_encryption key file must not be a symbolic link')
    with open(key_path, 'r', encoding='ascii') as key_file:
        key_data = json.load(key_file)

    active_key = key_data['active'].encode('ascii')
    previous_keys = [key.encode('ascii') for key in key_data.get('previous', [])]
    fernets = [Fernet(active_key)] + [Fernet(key) for key in previous_keys]
    if stat.S_IMODE(os.stat(key_path).st_mode) & 0o077:
        os.chmod(key_path, 0o600)
    return MultiFernet(fernets), [active_key, *previous_keys]


@lru_cache(maxsize=32)
def get_fernet_from_path(key_path):
    """Read the Fernet keyring once per path and cache it in this Odoo worker."""
    return _read_keyring(key_path)[0]


def ensure_key_file(key_path, configured_key=None):
    """Create the shared key file once, retaining old keys for migration reads."""
    key_path = os.path.abspath(key_path)
    key_dir = os.path.dirname(key_path)
    if not os.path.isdir(key_dir):
        raise RuntimeError('field_encryption key directory does not exist: %s' % key_dir)

    configured_key = configured_key.encode('ascii') if configured_key else None
    if configured_key:
        Fernet(configured_key)  # Validate before persisting configuration.

    lock_path = key_path + '.lock'
    lock_fd = os.open(lock_path, os.O_CREAT | os.O_RDWR, 0o600)
    try:
        os.fchmod(lock_fd, 0o600)
        fcntl.flock(lock_fd, fcntl.LOCK_EX)

        if os.path.lexists(key_path):
            _, known_keys = _read_keyring(key_path)
            if configured_key and configured_key not in known_keys:
                raise RuntimeError(
                    'Configured encryption_key conflicts with %s; resolve the key mismatch '
                    'before starting Odoo.' % key_path
                )
        else:
            active_key = Fernet.generate_key()
            previous_keys = []
            for key in (configured_key, LEGACY_DEFAULT_KEY.encode('ascii')):
                if key and key != active_key and key not in previous_keys:
                    previous_keys.append(key)
            key_data = {
                'active': active_key.decode('ascii'),
                'previous': [key.decode('ascii') for key in previous_keys],
            }

            fd, temporary_path = tempfile.mkstemp(prefix='.field_encryption.', dir=key_dir)
            try:
                os.fchmod(fd, 0o600)
                with os.fdopen(fd, 'w', encoding='ascii') as key_file:
                    json.dump(key_data, key_file)
                    key_file.write('\n')
                    key_file.flush()
                    os.fsync(key_file.fileno())
                try:
                    os.link(temporary_path, key_path)
                except FileExistsError:
                    _, known_keys = _read_keyring(key_path)
                    if configured_key and configured_key not in known_keys:
                        raise RuntimeError(
                            'Configured encryption_key conflicts with %s; resolve the key '
                            'mismatch before starting Odoo.' % key_path
                        )
            finally:
                if os.path.exists(temporary_path):
                    os.unlink(temporary_path)

        get_fernet_from_path.cache_clear()
        return get_fernet_from_path(key_path)
    finally:
        fcntl.flock(lock_fd, fcntl.LOCK_UN)
        os.close(lock_fd)


def ensure_database_key(env):
    """Store this database's reference to the instance-wide key file."""
    parameters = env['ir.config_parameter'].sudo()
    stored_path = parameters.get_param(KEY_PATH_PARAMETER)
    key_path = os.path.abspath(stored_path) if stored_path else default_key_path()
    configured_key = config.get('encryption_key', False)
    ensure_key_file(key_path, configured_key)
    if key_path != stored_path:
        parameters.set_param(KEY_PATH_PARAMETER, key_path)
    return key_path


def get_fernet(env):
    """Get the Fernet keyring referenced by this database's system parameter."""
    parameters = env['ir.config_parameter'].sudo()
    key_path = parameters.get_param(KEY_PATH_PARAMETER)
    if not key_path:
        key_path = ensure_database_key(env)
    key_path = os.path.abspath(key_path)
    if not os.path.isfile(key_path):
        raise RuntimeError('field_encryption key file is missing: %s' % key_path)
    return get_fernet_from_path(key_path)
