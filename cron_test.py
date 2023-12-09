import os

from datetime import datetime

output_dir = '/home/mark/projects/market/scraper/output'
output_file = 'cron_test_log.log'
log_path = os.path.join(output_dir, output_file)
write_mode = "a" if os.path.exists(log_path) else "w"
dtfmt = "%Y-%m-%d %H:%M:%S"

msg = "python cron test"

print("hopefully this prints to the terminal")

def format_log(msg):
    now = datetime.now().strftime(dtfmt)
    return f'{now} - {msg}'

with open(log_path, write_mode) as f:
    log_msg = format_log(msg)
    f.write(log_msg)
