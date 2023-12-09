import requests
import re
import os
from datetime import datetime, time

ticker = 'AAPL'

base_url = 'https://www.google.com/search?q='
url = base_url + ticker

securities_path = '/home/mark/projects/market/dataloader/data/security/securities.csv'
output_dir = '/home/mark/projects/market/scraper/output'
filename = 'AAPL.csv'
output_path = os.path.join(output_dir, filename)

dtfmt = "%Y-%m-%d %H:%M:%S"
start_pattern = r'>Stock Price<'
end_pattern = r'Currency in USD'
snippet_pattern = re.compile(f'(?<={re.escape(start_pattern)})(.*?)(?={re.escape(end_pattern)})', re.DOTALL)
price_pattern = re.compile('\d+\.\d{2}')

write_mode = "a" if os.path.exists(output_path) else "w"

now = datetime.now()

if now.time() <= time(15, 0): # before 3pm
    response = requests.get(url)
    html_body = response.text

    html_snip = snippet_pattern.findall(html_body)

    if html_snip:
        decimals = price_pattern.findall(html_snip[0])
        if decimals:
            price = decimals[0]
            line = ','.join([now.strftime(dtfmt), ticker, price])
            print(line)
            with open(output_path, write_mode) as f:
                f.write(line + '\n')
        else:
            print(f"{now.strftime(dtfmt)} - price not found for {ticker}")
