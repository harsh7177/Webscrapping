#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pymongo
import requests
import bs4
from bs4 import BeautifulSoup as bs
import pandas as pd


# In[2]:


#scrapping
product=input('Enter the prduct name:=')
url='https://www.flipkart.com/search?q={}'.format(product)
headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win 64 ; x64) Apple WeKit /537.36(KHTML , like Gecko) Chrome/80.0.3987.162 Safari/537.36'}
scrap=requests.get(url,headers=headers)
x=scrap
web=bs(x.text)
o=int(web.find_all('div',class_="_2MImiq")[0].text.split('1234')[0][-3::1])

Product=[]
price=[]
Discount=[]
R_R=[]
Rating=[]


for i in range(o):
    n='https://www.flipkart.com/search?q={}&page={}'.format(product,i)
    n_scrap=requests.get(n,headers=headers).text
    bs_s=bs(n_scrap)
    for i in  bs_s.find_all('div',class_="_4rR01T"):
        Product.append(i.text)
    for i in bs_s.find_all('div',class_='_30jeq3 _1_WHN1'):
        price.append(int(i.text.replace(',','').replace('₹','')))
    for i in bs_s.find_all('span',class_="_2_R_DZ"):
        R_R.append(i.text.split('\xa0&\xa0'))
    for i in bs_s.find_all('div',class_="_3LWZlK"):
        Rating.append(i.text[0])
    
        


# In[36]:


n='https://www.flipkart.com/search?q={}&page={}'.format(product,i)
n_scrap=requests.get(n,headers=headers)
bs_s=bs(n_scrap.text)
bs_s.find_all('div',class_="_3LWZlK")


# In[16]:


df=pd.DataFrame(list(zip(Product,price,R_R,Rating)),columns=['Name','Price','Rating&Reviews','Rating'])


# In[2]:


#mongodb
db=pymongo.MongoClient


# In[3]:


client=db("mongodb://localhost:27017")


# In[5]:


sc=client['Flipkart']


# In[70]:


col=sc[product]


# In[71]:


a={"Product":Product,"Price":price,"Discount":Discount,'R_R':R_R,'Rating':Rating}


# In[72]:


col.insert_one(a)


# In[73]:


sc.list_collection_names()


# In[74]:


list(col.find({}))


# In[28]:





# In[ ]:





# In[30]:





# In[ ]:





# In[ ]:




