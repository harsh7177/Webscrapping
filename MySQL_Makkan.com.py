#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup as bs
import pandas as pd
import mysql.connector as conn
class Makkan():
    def __init__(self):
        self.t=[]
        self.a=[]
        self.p=[]
        self.s=[]
        self.st=[]
        self.AG=[]
        self.ini=[]
        self.L=[]
       
        
        self.loc=input('Enter the City:- ')
        mydb=conn.connect(host='localhost',user='root',password='hkpapa',database='makkan')
        cursor=mydb.cursor()
        cursor.execute('show tables')
        self.ex_tb=cursor.fetchall()
        
        self.loc1=[]
        
        for i in self.ex_tb:
            self.loc1.append(i[0])
        if self.loc not in self.loc1:
            self.loc1.append(self.loc)
            self.new_table()
        else:
            self.db()

    def new_table(self):
        url1='https://www.makaan.com/{}-residential-property/buy-property-in-{}-city'.format(self.loc,self.loc)
        headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win 64 ; x64) Apple WeKit /537.36(KHTML , like Gecko) Chrome/80.0.3987.162 Safari/537.36'}
        web = requests.get(url1,headers=headers).text
        scrap=bs(web)
        #pages=int(scrap.find('div',class_="search-result-footer").text.split('...')[-1])
        self.pages=2
        for i in range (self.pages):
            url='https://www.makaan.com/{}-residential-property/buy-property-in-{}-city?page={}'.format(self.loc,self.loc,self.pages)
            headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win 64 ; x64) Apple WeKit /537.36(KHTML , like Gecko) Chrome/80.0.3987.162 Safari/537.36'}
            web1=requests.get(url,headers=headers).text
            self.scrap1=bs(web1)
        for i in self.scrap1.find_all('div',class_='title-line'):
            self.t.append(i.text)
        for i in self.scrap1.find_all('div',class_='locWrap'):
            self.a.append(i.text)
        for i in self.a:
            self.L.append(i.split(',')[-1])    
        for i in self.scrap1.find_all('td',class_='price'):
            a=i.text
            if 'Cr' in a:
                b=float(a.split('Cr')[0])
                s=str(round(b*100,2))
                self.p.append(s + ' L')
            else:
                self.p.append(a)
        for i in self.scrap1.find_all('td',class_='size'):
            self.s.append(i.text+' sq ft')
        for i in self.scrap1.find_all('tr',class_="hcol w44"):
            a=i.text
            if 'Under Construction' in a:
                self.st.append(a.split('Construction')[0]+' Construction')
            else:
                self.st.append(a.split('Construction')[0])
        for i in self.scrap1.find_all('ul',class_="listing-details"):
            ini=i.text
            self.AG.append(ini)    
        
        mydb=conn.connect(host='localhost',user='root',password='hkpapa',database='Makkan')
        cursor=mydb.cursor()
        query=('Create table {} (Title varchar(200), Area varchar(200),City varchar(10), Price varchar(200), Size varchar(200), Build varchar(200),Details varchar(50))').format(self.loc)
        cursor.execute(query)
        
        for a,b,c,d,e,f,g in zip(self.t,self.a,self.L,self.p,self.s,self.st,self.AG):
            values = (a,b,c,d,e,f,g)
            sql = ("INSERT INTO {} VALUES (%s, %s, %s, %s, %s, %s, %s)").format(self.loc)
            cursor.execute(sql, values)
        mydb.commit()
        self.db()
    def db(self):
        mydb=conn.connect(host='localhost',user='root',password='hkpapa',database='Makkan')
        cursor=mydb.cursor()
        query = ("SELECT * FROM {}").format(self.loc)
        data = pd.read_sql(query, mydb)
        return data


# In[ ]:




