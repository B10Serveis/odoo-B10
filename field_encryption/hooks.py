from .keyring import ensure_database_key


def post_init_hook(env):
    """Initialize the instance key reference for a newly installed database."""
    ensure_database_key(env)
