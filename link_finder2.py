from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, thread
import threading


pages = 1

url_list = []

page_source = ''
    

            
def open_page(url):  
        driver = webdriver.Chrome(executable_path=r"C:\chromedriver.exe")
        driver.maximize_window()
        driver.get(url)
        driver.implicitly_wait(10)
        elem = driver.find_element(By.XPATH,'//*[@id="uc-btn-accept-banner"]')
        elem.click()
        page_source = driver.page_source
        return driver.page_source

    
def  scrape_links():
    with open("links.txt","w+", encoding="utf-8") as f:
        soup = BeautifulSoup(page_source,"lxml")
        property_list = soup.find_all('li', class_='search-results__item')
        print(f"Page {page}",file=f)
        for house in range(len(property_list)):
            try:
                current_property = property_list[house].find('a',href=True)
                if "immoweb" in current_property["href"]:
                    url_list.append(current_property['href'])
                    print(current_property["href"], file=f)
                    
            except:
                continue
                
    
        

                  
for page in range(pages+1):
    url = f"https://www.immoweb.be/en/search/house/for-sale?countries=BE&page={page}&orderBy=relevance"
    #print(url)
    page_source = open_page(url)
    scrape_links()
    
#print(url_list)

