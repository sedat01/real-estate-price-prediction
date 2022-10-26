import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup


pages = 1

url_list = []

page_source = ''

session = requests.Session()
    
start = time.perf_counter()
            
def open_page(url):  
        options = Options()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(executable_path=r"C:\chromedriver.exe",options=options)
        driver.minimize_window()
        driver.get(url)
        driver.implicitly_wait(10)
        try:
            elem = driver.find_element(By.XPATH,'//*[@id="uc-btn-accept-banner"]')
            elem.click()
            pg_code = driver.page_source
            scrape_links(pg_code,url)
            return(pg_code)
        except:
            pass

    
def  scrape_links(pg_code,url):
    # header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'}
    
    # pg_code = session.get(url, headers=header)
    # print(pg_code)
    with open("west_flanders_links.txt","a+", encoding="utf-8") as f:
        soup = BeautifulSoup(pg_code,"lxml")
        #print(soup,file=f)
        property_list = soup.select('li', class_='search-results__item')
        print(type(property_list))
    
        #print(property_list,file=f)
        for i in range(38):
            #try:
            #print(i)
            current = property_list[i].find("a",href=True)
            print(len(current))
            print(current['href'],file=f)
            #current_property = property_list[i].find('a',href=True)
            #print(current_property)
            #url_list.append(current_property['href'])
            #print(current_property["href"], file=f)
                    
            #except:
             #   continue
                
    
        
urls = []
                  
for page in range(1,pages+1):
    url = f"https://www.immoweb.be/en/search/house/for-sale/west-flanders/province?countries=BE&page={page}&orderBy=relevance"
    urls.append(url)
    #print(url)
    open_page(url)
    
#Parallel(n_jobs=-3,require="sharedmem",verbose=10)(delayed(open_page)(url) for url in urls)


print(time.perf_counter()-start)