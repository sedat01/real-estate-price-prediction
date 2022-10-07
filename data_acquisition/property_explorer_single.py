from bs4 import BeautifulSoup
import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

with open("./links_clean.txt","r",encoding='utf-8') as f:
    url_list = f.readlines()
data_all = {}
    
    

def open_page(url):  
        driver = webdriver.Chrome(executable_path=r"C:\chromedriver.exe")
        driver.minimize_window()
        driver.get(url)
        driver.implicitly_wait(10)
        try:
            elem = driver.find_element(By.XPATH,'//*[@id="uc-btn-accept-banner"]')
            elem.click()
            pg_code = driver.page_source
            #scrape_links(pg_code,url)
            return(pg_code)
        except:
            pass

    
def explore_property(url):
    pat1 = "\\n";pat2 = "  "
    pat = r'|'.join((pat1,pat2))
    page_source = open_page(url)
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


for i in range(5):
    explore_property(url_list[i])

    
df = pd.DataFrame.from_dict(data_all, orient="index")
with open("dataframe.txt","w+",encoding="utf-8") as f:
    print(df,file=f)
    
df.to_csv("try_csv.csv")