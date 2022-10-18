from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup


driver = webdriver.Chrome(executable_path=r"C:\chromedriver.exe")
driver.implicitly_wait(10)
driver.maximize_window()
driver.get("https://www.immoweb.be/en/search/house/for-sale?countries=BE&page=1&orderBy=relevance")
driver.implicitly_wait(10)
elem = driver.find_element(By.XPATH,'//*[@id="uc-btn-accept-banner"]')
print(elem)
elem.click()
time.sleep(1)
for i in range(46):
    time.sleep(0.5)
    #elem2 = driver.find_element(By.CLASS_NAME,'pagination__link pagination__link--next button button--text button--size-small')
    #elem2.click()
    driver.get(f"https://www.immoweb.be/en/search/house/for-sale/luxembourg/province?countries=BE&page={i}&orderBy=relevance")
    page_source = driver.page_source
    soup = BeautifulSoup(page_source,"lxml")
    property_list = soup.find_all('li', class_='search-results__item')
    for property in range(len(property_list)):
        current_property = property_list[property].find('a',href=True)
        with open("links_belgian_luxembourg.txt","a+",encoding="utf-8") as f:
            try:
                print(current_property['href'], file=f)
            except:
                print("None")
                
