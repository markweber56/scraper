import requests
import re
import os
import csv

from datetime import datetime, time

securities_path = '/home/mark/projects/market/dataloader/data/security/securities.csv'

# load tickers
with open(securities_path) as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    tickers = [row[1] for row in reader]

ticker = tickers[1]

base_url = 'https://www.google.com/search?q='

output_dir = '/home/mark/projects/market/scraper/output'
output_filename = 'prices.csv'
output_path = os.path.join(output_dir, output_filename)

dtfmt = "%Y-%m-%d %H:%M:%S"
start_pattern = r'>Stock Price<'
end_pattern = r'Currency in USD'
snippet_pattern = re.compile(f'(?<={re.escape(start_pattern)})(.*?)(?={re.escape(end_pattern)})', re.DOTALL)
price_pattern = re.compile('\d+\.\d{2}')

write_mode = "a" if os.path.exists(output_path) else "w"

start_time = datetime.now()

with open(output_path, write_mode) as output_file:
    for ticker in tickers:
        url = f'{base_url + ticker}+stock+price'
        now = datetime.now()

        response = requests.get(url)
        html_body = response.text

        html_snip = snippet_pattern.findall(html_body)

        if html_snip:
            decimals = price_pattern.findall(html_snip[0])
            if decimals:
                price = decimals[0]
                line = ','.join([now.strftime(dtfmt), ticker, price])
                print(line)

                output_file.write(line + '\n')
        else:
            print(f"{now.strftime(dtfmt)} - price not found for {ticker}")

print(f'time elapsed: {datetime.now() - start_time}')
