
# coding: utf-8

# In[1]:


import csv
import os
import zipfile
import pandas as pd
import numpy as np
import glob
import sys
import logging
from bs4 import BeautifulSoup
from io import BytesIO
from urllib.request import urlopen
from zipfile import ZipFile
import time
import datetime
import requests

args = sys.argv[1:]

year = ''
counter = 0
if len(args) == 0:
    year = "2003"
for arg in args:
    if counter == 0:
        year= str(arg)
    counter += 1
    
logging.basicConfig(filename="logs.txt", level=logging.DEBUG,format='%(asctime)s - %(levelname)s - %(message)s') 
logging.debug('Start of Log entries')
logging.debug('                    ')
logging.debug('Checking valid year entry or not')

logYear = ['2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015','2016','2017']
for log in logYear:    
    if year not in log:
        print(year + "does not exist")


# In[2]:


url = 'https://www.sec.gov/data/edgar-log-file-data-set.html'   


# In[3]:


html = urlopen(url)


# In[4]:


soup = BeautifulSoup(html, "html.parser")


# In[5]:


all_div = soup.findAll("div", attrs={'id': 'asyncAccordion'})


# In[6]:


for div in all_div:
       h2tag = div.findAll("a")
       for a in h2tag:
           if str(year) in a.get('href'):
               global ahref
               ahref = a.get('href')


# In[7]:


linkurl = 'https://www.sec.gov' + ahref
linkurl


# In[8]:


linkhtml = urlopen(linkurl)


# In[9]:


allzipfiles = BeautifulSoup(linkhtml, "html.parser")


# In[10]:


ziplist = allzipfiles.find_all('li')


# In[11]:


monthlistdata = []
count = 0
for li in ziplist:
    zipatags = li.findAll('a')
    for zipa in zipatags:
        if "01.zip" in zipa.text:
            monthlistdata.append(zipa.get('href'))


# In[12]:


monthlistdata


# In[13]:


df = pd.DataFrame()
foldername = str(year)
path = str(os.getcwd()) + "/" + foldername
if not os.path.exists(path):
    os.makedirs(path)


# In[14]:


for month in monthlistdata:
    with urlopen(month) as zipresp:
        with ZipFile(BytesIO(zipresp.read())) as zfile:
            zfile.extractall(path)


# In[15]:


all_data = pd.DataFrame()
for f in glob.glob(path + '/log*.csv'):
    df = pd.read_csv(f, parse_dates=[1])
    all_data = all_data.append(df, ignore_index=True)


# In[16]:


df = all_data


# In[17]:


df


# In[18]:


all_data = df


# In[19]:


new_data = pd.DataFrame()
all_data['zone'] = all_data['zone'].astype('int64')
all_data['cik'] = all_data['cik'].astype('int64')


# In[20]:



all_data['noagent'] = all_data['noagent'].astype('int64')
all_data['norefer'] = all_data['norefer'].astype('int64')


# In[21]:


all_data['code'] = all_data['code'].astype('int64')


# In[22]:


all_data['idx'] = all_data['idx'].astype('int64')


# In[23]:


all_data['crawler'] = all_data['crawler'].astype('int64')
all_data['find'] = all_data['find'].astype('int64')


# In[24]:


data = pd.DataFrame()


# In[25]:


all_data.loc[all_data['extention'] == '.txt', 'extention'] = all_data["accession"].map(str) + all_data["extention"]
all_data['browser'] = all_data['browser'].fillna('win')
all_data['size'] = all_data['size'].fillna(0)
all_data['size'] = all_data['size'].astype('int64')
all_data = pd.DataFrame(all_data.join(all_data.groupby('cik')['size'].mean(), on='cik', rsuffix='_newsize'))
all_data['size_newsize'] = all_data['size_newsize'].fillna(0)
all_data['size_newsize'] = all_data['size_newsize'].astype('int64')
all_data.loc[all_data['size'] == 0, 'size'] = all_data.size_newsize
del all_data['size_newsize']
data = all_data


# In[26]:


data


# In[27]:


newdata = data


# In[28]:


newdata.to_csv("merged.csv",encoding='utf-8')

