# -*- coding: utf-8 -*-
"""Day 12.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1MoKJdKbhk0ZPrxEzu11Aib7RHDlpjV7x
"""

#import libraries
import pandas as pd 
import numpy as np 
import seaborn as sns
import matplotlib.pyplot as plt
import os
import glob

#list all csv files only
csv_files = glob.glob('*.{}'.format('csv'))
csv_files

#Make single data for  all csv 
data = pd.concat([pd.read_csv(f) for f in csv_files ], ignore_index=True)
# first five column of data 
data.head()

"""# Data_Preprocessesing AND Data_Preprocessing"""

#cheaking shape of data 
data.shape

#cheaking dtype 
data.info()

#cheaking null valus 
data.isnull().sum()

#let us  dropthe null value 
data.dropna(how='all',inplace=True)
#let us cheak it again ]
"NAN value :"
data[data.isna().any(axis=1)]
## future warning! ValueError: invalid literal for int() with base 10: 
data = data[data['Order Date'].str[0:2] != 'Or']
data.head()

#changeing dtype of column 
data['Quantity Ordered']=data['Quantity Ordered'].astype('int64')   # convert to int64
data['Price Each']=data['Price Each'].astype('float')               #convert to float 
data['Order Date']=pd.to_datetime(data['Order Date'])               #convert to date time

"""Now we add another columns like manth hours days cities"""

def augment_data(data):
  ''' now we add some columns 
  that  are  born  from another columns 
  '''
  #function to get city 
  def get_city(address):
    return address.split(',')[1]

  #function to get state 
  def get_state(address):
    return address.split(',')[2].split( ' ')[1]

  #adding year ti column 
  data['year']=data['Order Date'].dt.year

  #adding month to column 
  data['month']=data['Order Date'].dt.month

  #adding hour to column 
  data['hour']=data['Order Date'].dt.hour

  #adding minute to column 
  data['minute']=data['Order Date'].dt.minute

  ## now let us make the sales column by multiply quantity by price 
  data['sales']=data['Price Each']*data['Quantity Ordered']

  #let us get the cities in orderd column 
  data['Cities'] = data['Purchase Address'].apply(lambda x: f"{get_city(x)} ({get_state(x)})") 

  return data

#now apply this function 
data=augment_data(data)
data.head()

"""# Data_Analysis"""

#Now we plot heatmap to cheak relationship between dependent and independent variable 
plt.figure(figsize=(20,10))
sns.heatmap(data.corr(),annot=True)
plt.show()

"""## Now we cheak the best year of sale and how much you earned that year"""

plt.figure(figsize=(20,10))
sns.countplot(x='year',data=data)
plt.xlabel('Years')
plt.ylabel('sales in $')
plt.title("sales per year")
plt.show()

data.groupby('year').sum()

"""## As we see in above figure  we see that 2019 has maximum sales  of 34483365.68 and  in 2020 has  less sale of 8670.29 as compare to 2019 This is due to  COVID or due to inbalance dataset

Now we cheak what is the best month of sale and how it earn in    that month
"""

data.groupby('month').sum()

plt.figure(figsize=(20,10))
sns.barplot(x=data.groupby('month').sum().index,y=data.groupby('month').sum()['sales'],data=data)
plt.xlabel('Years')
plt.ylabel('sales in $')
plt.title("sales per MONTH")
plt.show()

"""## now we find Which City had the highest number of sales"""

data.groupby('Cities').sum()

plt.figure(figsize=(20,10))
sns.barplot(x=data.groupby('Cities').sum().index,y=data.groupby('Cities').sum()['sales'],data=data)
plt.xlabel('cities')
plt.ylabel('sales in $')
plt.title("sales per Cities")
plt.show()

"""## Now we cheak what time should we display advertismant to maximize likelihood of customers  buying product """

hrs=[hour for hour,df in data.groupby('hour')]
plt.figure(figsize=(28,7))
plt.plot(hrs,data.groupby(['hour']).count())
plt.xlabel('hours')
plt.style.use('fivethirtyeight')
plt.grid(True)
plt.xticks(hrs)
plt.ylabel('no_of_order ')
plt.title('time of customer by product ')
plt.show()

"""so as we that from above diagram 9am or 10am is best time to play an add """

data.groupby('Product').sum()

#let us prepare a variable for plotting 
product_group=data.groupby('Product')
quantity_orderd=product_group.sum()['Quantity Ordered']
prices = data.groupby('Product').mean()['Price Each']
products = [product for product, df in product_group]

#now we vizualize it 
fig, ax1 = plt.subplots(figsize=(24, 8))
ax2 = ax1.twinx()
# AXES 1
ax1.bar(products, quantity_orderd)
ax1.set_xlabel('Product Name')
ax1.set_ylabel('Quantity Orderd', color='b')
ax1.set_xticklabels(products, rotation='vertical')
# AXES 2
ax2.plot(products, prices, 'r-')
ax2.set_ylabel('Price in USD ($)', color='r')

"""## Total Sale and Quantity ordered of different products over months"""

temp_data = data.groupby(['month', 'Product']).sum().reset_index()

#
g = sns.FacetGrid(data, col="month", hue='month', col_wrap=4, size=8)
g.map(sns.barplot, "Quantity Ordered", "Product")
g.fig.subplots_adjust(top=0.9)
g.fig.suptitle('Title', fontsize=36)

"""## Now we cheak how much of each product sell in each city """

# data used in this section
temp_data = data.groupby(['Cities', 'Product']).sum().reset_index()

ax = sns.FacetGrid(temp_data, col="Cities", hue='Cities', col_wrap=3, size=8)
ax.map(sns.barplot, "sales", "Product")
ax.fig.subplots_adjust(top=0.9)
ax.fig.suptitle('City/Product/Total Sale', fontsize=36)

