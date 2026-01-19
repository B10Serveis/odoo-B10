import os
import sys
from datetime import datetime, timedelta
import random
import socket
import struct

if len(sys.argv) == 1:
    print('usage: pyhton3 odoo_log.py <outputfile>')
    exit(1)

print('=========================')
print('Odoo Log Generator v1.0.0')
print('=========================')
print('')
print('Please provide configuration...')


date_format = '%d-%m-%Y'
start_date_str = input('* Start date: ')

try:
    start_date = datetime.strptime(start_date_str, date_format)
except:
    print('err: invalid datetime. expected format ' + str(date_format))
    exit(1)

end_date_str = input('* End date: ')

try:
    end_date = datetime.strptime(end_date_str, date_format)
except:
    print('err: invalid datetime, expected format ' + str(date_format))

if end_date < start_date:
    print('err: the start date cannot be greater than the end date')
    exit(1)

db_name = input('* Database name: ')

accounts_unparsed = input('* Accounts [comma sepparated]: ')
accounts = [x.strip() for x in accounts_unparsed.strip().split(',')]

min_per_day_str = input('* Minimum logins per day: ')

try:
    min_per_day = int(min_per_day_str)
except:
    print('err: must be a number')
    exit(1)

max_per_day_str = input('* Maximum logins per day: ')

try:
    max_per_day = int(max_per_day_str)
except:
    print('err: must be a number')
    exit(1)

if min_per_day < 0 or max_per_day < 0 or max_per_day < min_per_day:
    print('err: minimum and maximum logins must be positive numbers and the minimum one smaller than the maximum')
    exit(1)

num_ips_str = input('* Number of IP addresses: ')

try:
    num_ips = int(num_ips_str)
except:
    print('err: must be a number')
    exit(1)

if num_ips < 1:
    print('err: at least one IP address should be generated')
    exit(1)

print('OK.')
print('=========================')
print('')
print('Generating random IPS....')
print('')

ips = []
while True:
    for _ in range(0, num_ips):
        rand_ip = socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))
        ips.append(rand_ip)
    print('Generated the following IP addresses: ')
    for ip in ips:
        print('* ' + ip)
    resp = input('OK? [y/N] ')
    if resp.upper() == 'Y':
        break
    print('Regenerating...')
    ips = []

current_date = start_date
current_date = current_date.replace(hour=0, minute=0, second=0)

end_weekday = 4

banned_dates = [
    (1, 1),
    (6, 1),
    (7, 4),
    (10, 4),
    (1, 5),
    (11, 5),
    (24, 6),
    (15, 8),
    (29, 9),
    (12, 10),
    (1, 11),
    (6, 12),
    (8, 12),
    (25, 12),
    (26, 12),
]
all_targets = []

def is_banned(dateval):
    for ban in banned_dates:
        if dateval.month == ban[1] and dateval.day == ban[0]:
            return True
    return False

while current_date <= end_date:
    if current_date.weekday() <= end_weekday and not is_banned(current_date):
        all_targets.append(current_date)
    current_date += timedelta(days=1)
    current_date = current_date.replace(hour=0, minute=0, second=0)

print('Picked ' + str(len(all_targets)) + ' credible dates')

different_ip_probability = 50

random.shuffle(accounts)
random.shuffle(ips)

account_map = []
i = 0
for acc in accounts:
    account_map.append((acc, ips[i]))
    if len(ips) == i + 1:
        i = 0
    else:
        i += 1

print('Mapped accounts to IP addresses')
for (k, v) in account_map:
    print('* ' + k + ' --> ' + v)

print('')
print('*********')
print('⚠ READY ⚠')
print('*********')
input('Press any key to generate...')

start_hour = 7
end_hour = 20

random_ip_probability = 50

failure_probability = 30

min_thread = 2500
max_thread = 600000

thread_reset_probability = 3
thread_change_probability = 15

current_thread = random.randrange(min_thread, max_thread/10)
next_thread_step = -1

for target_day in all_targets:
    num_logins = random.randrange(min_per_day, max_per_day)

    unparsed_times = []
    for _ in range(0, num_logins):
        hour = random.randrange(start_hour, end_hour+1)
        minute = random.randrange(0, 60)
        second = random.randrange(0, 60)
        unparsed_times.append((hour, minute, second))
        unparsed_times = sorted(unparsed_times)

    times = []
    for t in unparsed_times:
        times.append("{:02d}:{:02d}:{:02d}".format(t[0], t[1], t[2]))

    for time in times:
        millis = random.randrange(0, 999)
        acc_index = random.randrange(0, len(account_map))
        target_acc = account_map[acc_index][0]
        target_ip = account_map[acc_index][1]
        if random.randrange(0, random_ip_probability) == 0:
            ip_index = random.randrange(0, len(ips))
            target_ip = ips[ip_index]
        status = 'successful'
        if random.randrange(0, failure_probability) == 0:
            status = 'failed'
        if random.randrange(0, thread_change_probability) == 0:
            min_thread_threshold = current_thread - 1
            max_thread_threshold = max_thread
            if random.randrange(0, thread_reset_probability) == 0:
                min_thread_threshold = min_thread
                max_thread_threshold = max_thread/10
            current_thread = random.randrange(min_thread_threshold, max_thread_threshold)
        else:
            current_thread += next_thread_step
            next_thread_step *= -1

        log_line = "{} {};{};{};{};{}".format(
             target_day.strftime('%Y-%m-%d'),
             time,
             db_name,
             status,
             target_acc,
             target_ip,
        )
        with open(sys.argv[1], 'a+') as out_file:
            out_file.write(log_line + '\n')
    print('Generated ' + str(num_logins) + ' logins @ ' + target_day.strftime('%d-%m-%Y'))