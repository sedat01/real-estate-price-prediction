from bs4 import BeautifulSoup
import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests

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
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "bg-BG,bg;q=0.9,en;q=0.8,nl;q=0.7,de;q=0.6",
        "cookie": "__cf_bm=r4IjRFHtlr2QFIA8K0OWtx8MizguGihMCKeel00MyiY-1665184098-0-ASTvNCRVzIDtBc5p6N+DvfBn2huvC5ku69Gia14YP/8RzFX1bHw+Y5e9NwVvPEQ0+VT1FGGIpP0p9KbPgYFbNu4=; XSRF-TOKEN=eyJpdiI6IjZFcTE1RjVKZkhjNUJsR240Q21paHc9PSIsInZhbHVlIjoiOEJYWlI5MFQ0VUcwS1A0bzFvRVEraU9wUXF0TW56R1NxT0xkbUMvb1N5RUpDbjRCQWdVUk9DSlpNaWtrTDZqcGQ3VHJWYm1CYXdDaFJraHU2a3NUZUhOM1JBQ3VHdlFieG81ZkFmSmNHWFByZnZwNEttUzlvVVRhaENSTTlJbmYiLCJtYWMiOiI5MzA4OTdmYzNiYWQyZDFjNjY5ZjUwOWQ2ODVlZDRmZDkzZGM0ODYwMmI2ZTIxMDRhYTRiMzQ2YThhOTU4ZGE2In0%3D; immoweb_session=eyJpdiI6IkxvMUtvanNPMmZvNVdvNmcxdzhIbGc9PSIsInZhbHVlIjoiQk01L0w4WnJhaXY5TWY1bEcvYU5OMTJxcFI2aFBaQk0rRjVIU1lyS0dYeXkzQnV6alI5TzUrdTlObGY0S1dDbGd0UkhHbldnY3BReDkvdHYzZ3V1V0ptV3EwS1JLR3FCa0oxb215R29WWnQ2ZTBLWmxMWkhRWmtnT3R3eEtIQ1EiLCJtYWMiOiJiYTRiMThhYzhiMTA4MzIwNzkwYjRkMThjZTk5ZDU1NzUzZWY1YTFiNjMwZTg5ZDE4MTNkNmZlODQ2NjNlMDg4In0%3D; _ga=GA1.2.758451540.1665184099; _gid=GA1.2.826184938.1665184099; _ga_CJKP1787KG=GS1.1.1665184099.1.1.1665184099.0.0.0; _gcl_au=1.1.1747172368.1665184101; _uetsid=f00a0200469411ed9949c71588b9fe82; _uetvid=f009f520469411edbb4aebf1b7de0c23; _hjSessionUser_927717=eyJpZCI6IjZlN2E1MTk4LTczYzEtNTU0OC04YzQ3LTc2YjQwYTI4ZmEzMiIsImNyZWF0ZWQiOjE2NjUxODQxMDE1MDksImV4aXN0aW5nIjpmYWxzZX0=; _hjFirstSeen=1; _hjIncludedInSessionSample=0; _hjSession_927717=eyJpZCI6ImU1YWUwN2QzLWJlYTctNDBlMi1iYWI0LTFlMjEzZTBhMzJiOSIsImNyZWF0ZWQiOjE2NjUxODQxMDE2MzYsImluU2FtcGxlIjpmYWxzZX0=; _hjAbsoluteSessionInProgress=0; _hjCachedUserAttributes=eyJhdHRyaWJ1dGVzIjp7InVzZXJfYXR0cmlidXRlIjowfSwidXNlcklkIjpudWxsfQ==; _clck=1731rn2|1|f5i|0; _clsk=1gb4ocs|1665184102329|1|1|a.clarity.ms/collect",
        "sec-ch-ua": '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Windows",
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1'}

    pat1 = "\\n";pat2 = "  "
    pat = r'|'.join((pat1,pat2))
    page_source = requests.get(url, headers=headers)
    with open("source_look.txt", "w+", encoding="utf-8") as req:
        print(page_source.text, file=req)
    data = {}
    soup = BeautifulSoup(page_source.text,"lxml")
    property_id = soup.find("div",class_="classified__header--immoweb-code")
    property_id = property_id.text
    property_id = re.sub("Immoweb code : ","",property_id)
    property_id = re.sub(pat,"",property_id)
    print(property_id)
    tables = soup.find_all("tbody", class_="classified-table__body")
    for table in tables:
        row = table.select("tr", class_="classified-table__row")
        
        for element in row:
            #print(row, type(row))
            keys = element.find_all("th", class_="classified-table__header")
            values = element.find_all("td", class_="classified-table__data")
            for i in range(len(keys)):
                key = str(keys[i])
                key = re.sub("<.+?>","",key)
                value = str(values[i])
                value = re.sub("<.+?>","",value)
                data[key] = value
    for key, value in data.items():
        data [key] = re.sub(pat,"",value)
        
    with open("table_test.txt","a+",encoding="utf-8") as f:    
        print(data, file=f)
    #     print(data)

    with open("table_test.txt","a+", encoding="utf-8") as f:
        print(property_id,type(property_id),file=f)    
        
    data_all [property_id] = data


for i in range(100):
    explore_property(url_list[i])

    
df = pd.DataFrame.from_dict(data_all, orient="index")
with open("dataframe.txt","w+",encoding="utf-8") as f:
    print(df, file=f)
    
df.to_csv("try_csv.csv")