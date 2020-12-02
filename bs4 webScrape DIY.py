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

baseurl = 'https://www.diy.com'
subCatLinks = []
brickLinks = []
productlinks = []
nestedLinks = []

# pick a random user agent
for i in range(1,6):
    user_agent = random.choice(user_agent_list)
    # set the headers
    headers = {'User-Agent' : user_agent}


# get sub-category
for subCat in range(1):
    url = "https://www.diy.com/departments/flooring-tiling/DIY764939.cat"
    result = requests.get(url, headers=headers)    
    soup = bs4.BeautifulSoup(result.content, 'lxml')
    subCatMenu = soup.find('ul', class_='js-menu-children is-expanded')

    time.sleep(0.5)

    for subCat in subCatMenu.find_all('a', href=True):
        subCatLinks.append(baseurl + subCat['href'])
        time.sleep(1)
# print(result.status_code)
# print(subCatLinks)


# get brick category
try:        
    for brick in subCatLinks:
        r = requests.get(brick, headers=headers)
        broth = bs4.BeautifulSoup(r.content, 'lxml')
        brickCatMenu = broth.find('ul', class_='js-menu-children is-expanded')
        for brick in brickCatMenu.find_all('a', href=True):
            brickLinks.append(baseurl + brick['href'])
            time.sleep(1)
            # print(baseurl + brick['href'])
except Exception as ex:
    print('Brick looping complete: ', ex)


# get product grid next pages
try:
    for next_page in brickLinks:
        result = requests.get(next_page, headers=headers)
        stew = bs4.BeautifulSoup(result.content, 'lxml')

        # get nested page links
        try:
            for urlLink in stew.find_all('a', class_='_6317a47c _6073bbf6 b9523d7b b48f4ced _38e857b5 eec494cf b7d7b84f'): # next page url
                if urlLink.find('a') == None:
                    continue
                else:
                    brickLinks.append(urlLink.find('a'))
                    print(urlLink.find('a'))
                    break
            if baseurl + urlLink['href'] not in brickLinks:
                brickLinks.append(baseurl + urlLink['href'])

                # create and save pagination url
                nestedURL = baseurl + urlLink['href']
                nestedLinks.append(nestedURL)
                print('nestedLinks: ' + nestedURL)
        
        except Exception as ex:
            print('Error: no 2nd page', ex)
except Exception as ex:
            print('Error: ', ex)
    
print(len(brickLinks))


# get products
for prods in brickLinks:
    result = requests.get(prods, headers=headers)    
    soup = bs4.BeautifulSoup(result.content, 'lxml')
    productlist = soup.find_all('li', class_='b9bdc658')
    for item in productlist:
        for link in item.find_all('a', href=True):
            if link in productlinks:
                break
            else:
                productlinks.append(baseurl + link['href'])
                time.sleep(1)
print(result.status_code)
print('product links: ' + str(len(productlinks)))


# get product attributes
try:
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
        # get customer review
        """
        try:
        container = soup.find_all('li', class_='bv-content-item bv-content-top-review bv-content-review bv-content-loaded')
            for cr in container:
                for review in cr.findAll('div', class_='bv-content-summary-body-text'):
                    cusR = review.text
        except:
            container = 'no review'
        """           
        sku = {
            
            'sku': row,
            'name': name,
            'category': category,
            'subCat': subCat,
            'brickCat': brickCat,
            'rating': rating,
            'reviews': reviews,
            'price': price,
            'unitPrice': unitPrice,
            'clearance': clearance,
            'link': link
            # 'customer_review': container
            }
        
        productData.append(sku)
        time.sleep(1)
            
    print(len(productData))
    
    # create dataframe
    df = pd.DataFrame(productData)
    pd.set_option('display.max_columns', 100)

    # save to excel
    df.to_excel(r'C:\Users\forbej06\OneDrive - Kingfisher PLC\dev\Range\B&Q\Flooring\bs4Floor.xlsx', sheet_name='flooring', index=False, header=True)
    data = pd.read_excel(r'C:\Users\forbej06\OneDrive - Kingfisher PLC\dev\Range\B&Q\Flooring\bs4Floor.xlsx')
    print(df)
except Exception as ex:
    print('Error in product data: ', ex)
"""
## TO DO
# create dataframe
df1 = pd.DataFrame(productlinks)
pd.set_option('display.max_columns', 100)

# save to excel
df1.to_excel('bs4FloorLinks.xlsx', index=False, header=True)
"""
