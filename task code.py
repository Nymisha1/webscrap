from bs4.element import NamespacedAttribute
import requests
from bs4 import BeautifulSoup
import json
import pandas as pd

url = "https://www.stfrancismedicalcenter.com/find-a-provider/"
df=pd.DataFrame()
extract=[]



for i in range(1,41):    
    page = requests.post(url,data={"PhysicianSearch$FTR01$PagingID":i})
    
    if(page.status_code==200):
        
        soup = BeautifulSoup(page.text,"html.parser")
        name = soup.findAll('span',class_='title-style-5')
        speciality = soup.findAll('div', class_="specialty-list items-1 note-style-1 ui-repeater")
        dial= soup.findAll('li',class_="inline-svg phone")
        Address=soup.findAll('ul',class_='mar-t-1')
        
        for j in range(0, len(name)):
            Name = name[j].text
            if(len(name)==len(speciality)):
                Speciality = speciality[j].text.replace('\n',"")
            else:
                Speciality=" "
            if(len(name)==len(dial)):
                Phone = dial[j].text.replace('\n',"").replace('\t',"")
            else:
                Phone = " "
            Add = Address[j].text.replace('\n',"").replace('\t',"")
            
            extract.insert(j,[Name,Speciality,Phone,Add,url])
            
output= pd.DataFrame(extract,columns=['Full name','Speciality','Phonenumber','Address','URL'])


output.to_csv("scrap.csv")
print(output)
    