import pandas as pd
import matplotlib.pyplot as plt

# get data sets
bv = pd.read_excel(r'C:\Users\forbej06\OneDrive - Kingfisher PLC\email data\B&Q\BazaarVoice\Diy_RR_AllReviewsReport_20200701_20200930_2550880.xlsx')
bs4Floor = pd.read_excel(r'C:\Users\forbej06\OneDrive - Kingfisher PLC\dev\Range\B&Q\Flooring\bs4Floor.xlsx')
bs4heatPlumb = pd.read_excel(r'C:\Users\forbej06\OneDrive - Kingfisher PLC\dev\Range\B&Q\HeatPlumb\bs4heatPlumb.xlsx')
skuSales = pd.read_excel(r'C:\Users\forbej06\OneDrive - Kingfisher PLC\email data\SAP\Monthly Sales Performance\SAP - EAN Monthly Sales (Digital).xlsx')


dfBV = pd.DataFrame(bv)

pd.set_option('display.max_columns', None)
pd.set_option('expand_frame_repr', True)

new_header = dfBV.iloc[2]
dfBV = dfBV[3:]
dfBV.columns = new_header

print(bs4heatPlumb.shape)
print(bv.shape)
print(skuSales.shape)


skuSales = skuSales.loc[skuSales['Order Creation Site Label'] == 'DIY.COM']

# join data sets on SKU

floorTiles = pd.merge(bs4Floor, skuSales, how='outer', left_on=['sku'], right_on=['EAN Code'])
heatingPlumbing = pd.merge(bs4heatPlumb, skuSales, how='outer', left_on=['sku'], right_on=['EAN Code'])
print(heatingPlumbing.head(5))

# save to excel
floorTiles.to_excel(r'C:\Users\forbej06\OneDrive - Kingfisher PLC\dev\Range\B&Q\Flooring\floorTiles.xlsx')
heatingPlumbing.to_excel(r'C:\Users\forbej06\OneDrive - Kingfisher PLC\dev\Range\B&Q\HeatPlumb\heatingPlumbing.xlsx')
"""
# group by brick
brickGroup = floorTiles.groupby('brickCat')
print(brickGroup.sum())
qtyOrdered = brickGroup.sum()['Realised Quantity']

bricks = [brick for brick, floorTiles in brickGroup]

# plot to bar graph
plt.bar(bricks, qtyOrdered)
plt.ylabel('Quantity Ordered')
plt.xlabel('Brick Category')
plt.xticks(bricks, rotation='vertical', size=8)


prices = floorTiles.groupby('brickCat').mean()['Realised Sales']

fig, ax1 = plt.subplots()

ax2 = ax1.twinx()
ax1.bar(bricks, qtyOrdered, color='g')
ax2.plot(bricks, prices, 'b-')

ax1.set_xlabel('Brick Name')
ax1.set_ylabel('Qty Ordered', color='g')
ax2.set_ylabel('Price (£)', color='b')
ax1.set_xticklabels(bricks, rotation='vertical', size=8)

# plt.show()
"""

# how many products are visible online?
bs4Skus = heatingPlumbing.groupby('brickCat').count()['sku']
sapSkus = heatingPlumbing.groupby('Brick Label').count()['EAN Code']
# how many of these are selling?

# top rated products

# average rating by category
