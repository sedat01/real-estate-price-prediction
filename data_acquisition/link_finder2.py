from joblib import Parallel, delayed
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, thread
import threading


pages = 333

url_list = []

page_source = ''
    
start = time.perf_counter()
            
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

    
def  scrape_links(pg_code,url):
    with open("links.txt","a+", encoding="utf-8") as f:
        soup = BeautifulSoup(pg_code,"lxml")
        property_list = soup.find_all('li', class_='search-results__item')
        print(f"page {url}",file=f)
        for house in range(len(property_list)):
            try:
                current_property = property_list[house].find('a',href=True)
                if "immoweb" in current_property["href"]:
                    url_list.append(current_property['href'])
                    print(current_property["href"], file=f)
                    
            except:
                continue
                
    
        
urls = []
                  
for page in range(1,pages+1):
    urls.append(f"https://www.immoweb.be/en/search/house/for-sale?countries=BE&page={page}&orderBy=relevance")
    #print(url)
    #open_page(url)
    
Parallel(n_jobs=-1,prefer="threads")(delayed(open_page)(url) for url in urls)

print(time.perf_counter()-start)