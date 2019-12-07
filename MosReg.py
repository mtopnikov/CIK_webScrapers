#importing libraries

import csv
import pandas as pd
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

#setting the URL of the site to parce
my_url = "http://www.moscow_reg.vybory.izbirkom.ru/region/moscow_reg?action=show&vrn=25020002699373&region=50&prver=0&pronetvd=null"

#connection and grabbing the page
uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()

#html parcing
page_soup = soup(page_html, "html.parser")
containers = page_soup.findAll("option")

#defining 
frames=[]

for i in range(1,len(containers)):
    my_url = containers[i]["value"] #getting URL ready to viewing a table
    
    uClient = uReq(my_url)
    page_html = uClient.read()
    uClient.close()
    page_soup = soup(page_html, "html.parser")
    containers2 = page_soup.findAll("td",{"class":"tdReport"})
   
    my_url = containers2[5].a["href"] #getting the link to the table
    
    df = pd.read_html(my_url)[7] #creating a data frame
    df = df.head(n=2).transpose()
    df.columns = ['UIK', 'pop']

    frames.append(df)
    
#beautifizing the rezult
result = pd.concat(frames)
result['UIK'] = result['UIK'].astype(str).str.replace('\D+', '')


#export to .csv
result.to_csv("UIKsMosReg.csv", sep=';', encoding='utf-8')