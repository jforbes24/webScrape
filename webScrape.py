import requests
import bs4
import lxml
import random
import numpy as np
import pandas as pd

user_agent_list = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.5 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
    ]

baseurl = 'https://www.diy.com/'
url = "https://www.diy.com/departments/lighting/indoor-lights/floor-lamps/DIY579453.cat?page={x}"

"""

productlinks = []

for x in range(1,6):
    for i in range(1,6):
        # pick a random user agent
        user_agent = random.choice(user_agent_list)
        # set the headers
        headers = {'User-Agent' : user_agent}
        # make the request
        result = requests.get(f"https://www.diy.com/departments/lighting/indoor-lights/floor-lamps/DIY579453.cat?page={x}", headers=headers)    
    soup = bs4.BeautifulSoup(result.content, 'lxml')
    productlist = soup.find_all('li', class_='b9bdc658')

    result_df = pd.DataFrame()

    for item in productlist:
        for link in item.find_all('a', href=True):
            # print(link['href'])
            productlinks.append(baseurl + link['href'])

print(productlinks)

"""

# get product info
testlink = 'https://www.diy.com//departments/goodhome-apennin-matt-cream-floor-light/5036581098452_BQ.prd'
headers = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'
    }
res = requests.get(testlink, headers=headers)
res.raise_for_status()
soup = bs4.BeautifulSoup(res.content, 'lxml')


# get product name
name = soup.select('h1')[0].getText().strip()
print(name)

# get product price
for string in soup.stripped_strings:
    print(repr(string))
# get product rating
print(soup.title.text)
