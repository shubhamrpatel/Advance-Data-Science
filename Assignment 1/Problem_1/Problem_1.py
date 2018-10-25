
# coding: utf-8

# In[10]:


import re
import requests
from bs4 import BeautifulSoup
import urllib.request
import csv
import sys
import os
import zipfile
import logging
import time
import datetime

args = sys.argv[1:]
cik = ''
accession = ''
counter = 0
if len(args) == 0:
    cik = '0000051143'
    accession = '0000051143-13-000007'
else:
    cik = args[0]
    accession = args[1]

if not os.path.exists('csvFile'):
    os.makedirs('csvFile')


cik = str(cik)
accession = str(accession)
cik = cik.lstrip('0')
acc = re.sub(r'[-]', r'', accession)
url = 'https://www.sec.gov/Archives/edgar/data/' + cik + '/' + acc + '/' + accession + '/-index.htm'

final_url = ""
html = urllib.request.urlopen(url) 
soup = BeautifulSoup(html, "html.parser")
all_tables = soup.find('table', class_='tableFile')
tr = all_tables.find_all('tr')

for row in tr:
    final_url = row.findNext("a").attrs['href']
    break
next_url = "https://www.sec.gov" + final_url
print(next_url)

htmlpage = urllib.request.urlopen(next_url)
page = BeautifulSoup(htmlpage, "html.parser")

all_divtables = page.find_all('table')


# In[5]:


refined_tables=[]

for tab in all_divtables:
    for tr in tab.find_all('tr'):
        f=0
        for td in tr.findAll('td'):
            if('$' in td.get_text() or '%' in td.get_text()):
                refined_tables.append(tab)
                f=1;
                break;
        if(f==1):
            break;   


# In[6]:


for tab in refined_tables:
    records = []
    for tr in tab.find_all('tr'):
        rowString=[]
        for td in tr.findAll('td'):
            p = td.find_all('p')
            if len(p)>0:
                for ps in p:
                    ps_text = ps.get_text().replace("\n"," ") 
                    ps_text = ps_text.replace("\xa0","")                 
                    rowString.append(ps_text)
            else:
                td_text=td.get_text().replace("\n"," ")
                td_text = td_text.replace("\xa0","")
                rowString.append(td_text)
        records.append(rowString)        
    with open(os.path.join('csvFile' , str(refined_tables.index(tab)) + 'tables.csv'), 'w') as f:
        writer = csv.writer(f)
        writer.writerows(records)


# In[11]:


def zipdir(path, ziph, refined_tables):
    # ziph is zipfile handle
    for tab in refined_tables:
        ziph.write(os.path.join('csvFile', str(refined_tables.index(tab))+'tables.csv'))   

zipf = zipfile.ZipFile('csv.zip', 'w', zipfile.ZIP_DEFLATED)
zipdir('/', zipf, refined_tables)
zipf.close()

