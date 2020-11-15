import requests
import bs4
import lxml
import random
import numpy as np
import pandas as pd

# assign user-agent
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

productlinks = []

for i in range(1,6):
    # pick a random user agent
    user_agent = random.choice(user_agent_list)
    # set the headers
    headers = {'User-Agent' : user_agent}

# make the request
for x in range(1,4):
    result = requests.get(f"https://www.diy.com/departments/flooring-tiling/flooring-underlay/laminate-flooring/DIY566433.cat?page={x}", headers=headers)    
    soup = bs4.BeautifulSoup(result.content, 'lxml')
    productlist = soup.find_all('li', class_='b9bdc658')
    for item in productlist:
        for link in item.find_all('a', href=True):
            # print(link['href'])
            productlinks.append(baseurl + link['href'])
            
print(result.status_code)
print(len(productlinks))

# testlink = 'https://www.diy.com/departments/dartmoor-oak-effect-laminate-flooring-1-48m-pack/5013599012878_BQ.prd'

productData = []

for link in productlinks:
    r = requests.get(link, headers=headers)
    soup = bs4.BeautifulSoup(r.content, 'lxml')
    # get name
    name = soup.find('h1', class_='ccb9d67a _17d3fa36 _1c13b5e2 _58b3d2d9 _514c3e90 _75d33510 _266816c0 _6ba14bc3 fcf8ebfc _78852320 bae4848b cc6bbaee _23ee746f').text.strip()
    for tr in soup.find_all('tr')[2:]:
        td = tr.find_all('th')
    # get sku
    table = soup.find('table')
    tableRows = table.find_all('tr')

    for tr in tableRows:
        td = tr.find_all('td')    
        for i in td: 
            row = i.text
    # get rating
    try:
        rating = soup.find('div', class_='_45e852d0 _6418d197 _2263bdd0').text.strip()
    except:
        rating = 'no rating'
    # get reviews
    try:
        reviews = soup.find('span', class_='ccb9d67a _17d3fa36 _50344329 b1bfb616 cc6bbaee').text.strip()
    except:
        reviews = 'no reviews'
    # get price
    price = soup.find('div', class_='b25ad5d5 _4e80f7be _23ee746f _7b343263 _21dc035c').text.strip()
    # get unit price
    unitPrice = soup.find('div', class_='b00398fe b1bfb616 _8da52348 b1bfb616').text
    
    floor = {
        'sku': row,
        'name': name,
        'rating': rating,
        'reviews': reviews,
        'price': price,
        'unitPrice': unitPrice,
        'link': link
        }
        
    productData.append(floor)

print(len(productData))

df = pd.DataFrame(productData)
pd.set_option('display.max_columns', 100)

# save to excel
df.to_excel('bs4Floor.xlsx', index=False, header=True)
data = pd.read_excel('/Users/jforbes84/PycharmProjects/bs4Floor.xlsx')
print(df.head)
