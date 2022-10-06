from bs4 import BeautifulSoup
import link_finder2
import re
import pandas as pd
import numpy as np

with open("./links.txt","r",encoding='utf-8') as f:
    url_list = f.readlines()
data_all = {}
    
for link in range(3):
    if len(url_list[link])<50:
        continue
    else:
        pat1 = "\\n";pat2 = "  "
        pat = r'|'.join((pat1,pat2))
        page_source = link_finder2.open_page(url_list[link])
        data = {}
        soup = BeautifulSoup(page_source,"lxml")
        property_id = soup.find("div",class_="classified__header--immoweb-code")
        property_id = property_id.text
        property_id = re.sub("Immoweb code : ","",property_id)
        property_id = re.sub(pat,"",property_id)
        print(property_id)
        tables = soup.find_all("tbody", class_="classified-table__body")
        for table in tables:
            table = table.select("tr")
            
            for item in range(len(table)):
                keys = table[item].select("th")
                values = table[item].select("td")
                for i in range(len(keys)):
                
                    try:
                        
                        key = keys[i].text.strip();value = values[i].text.strip()
                        data [key] = value
                    except:
                        continue
        data_clean = {}            
        for key, value in data.items():
            data [key] = re.sub(pat,"",value)
            
        with open("table_test.txt","a+",encoding="utf-8") as f:    
            print(data, file=f)
        #     print(data)

        with open("table_test.txt","a+", encoding="utf-8") as f:
            print(property_id,type(property_id),file=f)    
            
    data_all [property_id] = data
    
    print(data_all)
    
    
    




print(dF)