import requests
import bs4
import lxml
import random
import numpy as np
import pandas as pd
import re
import time


# assign user-agent
user_agent_list = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.5 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
    ]


# pick a random user agent
for i in range(1,6):
    user_agent = random.choice(user_agent_list)
    # set the headers
    headers = {'User-Agent' : user_agent}


testurl = ['https://www.diy.com/departments/mackay-natural-oak-effect-laminate-flooring/1722498_BQ.prd',
           'https://www.diy.com/departments/koping-natural-oak-solid-wood-flooring-sample/3663602421931_BQ.prd',
           'https://www.diy.com/departments/traditional-lap-fence-panel-w-1-83m-h-1-22m/5013053172940_BQ.prd']

# get product attributes
try:
    productData = []

    for link in testurl:
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
        # get category
        breadCrumb = soup.find('div', class_='_3f9519f5 _042bbf7f acaa5c43')
        category = breadCrumb.find_all('p')[1].text
        # get subcat
        subCat = breadCrumb.find_all('p')[2].text
        # get brick category
        brickCat = breadCrumb.find_all('p')[3].text
        # get rating
        try:
            starText = soup.find('div', class_='_45e852d0 _6418d197 _2263bdd0').text.strip()
            starRegex = re.compile('F')
            rating = len(starRegex.findall(starText))
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
        # get clearance
        try:
            clearance = soup.find('p', class_='ccb9d67a _17d3fa36 _4fd271c8 _17d3fa36 _3b22edf5 _23ee746f').text
        except:
            clearance = 'active'
        # get home delivery (not available)
        try:
            hd = soup.find('div', class_='_7be6e5a0 _66dabd6a')
            homeDelivery = hd.find_all('span')[1].text
        except:
            pass
        # get click & collect (not available)
        
        sku = {
            
            'sku': row,
            'name': name,
            'category': category,
            'subCat': subCat,
            'brick': brickCat,
            'rating': rating,
            'reviews': reviews,
            'price': price,
            'unitPrice': unitPrice,
            'homeDelivery': homeDelivery,
            # 'clickCollect': clickCollect,
            'clearance': clearance,
            'link': link
            }
        
        productData.append(sku)
        time.sleep(0.5)
            
    print(productData)

except Exception as ex:
    print('Error: ', ex)
