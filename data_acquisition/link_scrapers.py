from bs4 import BeautifulSoup
import requests
from joblib import Parallel, delayed
import hashlib

from selenium import webdriver
from selenium.webdriver.common.by import By


def delete_duplicate() -> None:
    completed_lines_hash = set()

    output = open('links_clean.txt', "w+", encoding="utf-8")

    for line in open('links_dirty.txt', "r"):

        hash_value = hashlib.md5(line.rstrip().encode("utf-8")).hexdigest()

        if hash_value not in completed_lines_hash:
            output.write(line)
            completed_lines_hash.add(hash_value)

    output.close()


def xml_scrape(sitemap_url="https://www.immoweb.be/sitemap.xml", property_type="house"):
    """
        A function to scrape property links using Python Requests from XML sitemap.
        Recommended method to get property links. Use Selenium method if this one fails.
        param sitemap_url: Url where a list of sitemaps with property link are located.
        param property_type: Indicates the type of properties to be scanned. Can be "house" or "apartment"

        """

    session = requests.Session()

    sitemap = session.get(sitemap_url)
    sitemap = BeautifulSoup(sitemap.content, "xml").find_all("loc")
    sitemap_url_list = []
    for current_url in range(len(sitemap)):
        if "classifieds" in sitemap[current_url].text:
            sitemap_url_list.append(sitemap[current_url].text)

    def get_property_links(url):
        data = session.get(url)
        urls = BeautifulSoup(data.content, "xml").find_all("url")
        with open("links_dirty.txt", "a", encoding="utf-8") as f:
            for url in range(len(urls)):
                if "/en/" in urls[url].find("loc").text and property_type in urls[url].find("loc").text:
                    print(urls[url].find("loc").text, file=f)

    Parallel(n_jobs=-3)(delayed(get_property_links)(url) for url in sitemap_url_list)
    delete_duplicate()

    print("done")


def selenium_links(pages=333):
    """
    This is a function to get the property links from search result pages. The process is slow and due to immoweb's
    limitations it allows maximum of 333pages by 30 ads or total 9900 results. The pro of this method is it imitates
    human behavior via a Chrome browser
    param pages: Number of search result pages to scrape. Default is maximum (333)
    """

    def open_page(url):
        driver = webdriver.Chrome(executable_path=r"C:\chromedriver.exe")
        driver.minimize_window()
        driver.get(url)
        driver.implicitly_wait(10)
        try:
            elem = driver.find_element(By.XPATH, '//*[@id="uc-btn-accept-banner"]')
            elem.click()
            pg_code = driver.page_source
            scrape_links(pg_code, url)
        except:
            with open("selenium_log.txt", "a+", encoding='utf-8') as log:
                print(f"Skipping {url}")

    def scrape_links(pg_code, url):
        url_list = []
        with open("links_dirty.txt", "a+", encoding="utf-8") as f:
            soup = BeautifulSoup(pg_code, "lxml")
            property_list = soup.find_all('li', class_='search-results__item')
            print(f"page {url}", file=f)
            for house in range(len(property_list)):
                try:
                    current_property = property_list[house].find('a', href=True)
                    if "immoweb" in current_property["href"]:
                        url_list.append(current_property['href'])
                        print(current_property["href"], file=f)

                except:
                    with open("selenium_log.txt", "a+", encoding='utf-8') as log:
                        print(f"Skipping {url}")

    urls = []

    for page in range(1, pages + 1):
        urls.append(f"https://www.immoweb.be/en/search/house/for-sale?countries=BE&page={page}&orderBy=relevance")
        # print(url)
        # open_page(url)

    Parallel(n_jobs=-1, require="sharedmem", verbose=10)(delayed(open_page)(url) for url in urls)
    delete_duplicate()
