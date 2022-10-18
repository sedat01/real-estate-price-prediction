from bs4 import BeautifulSoup
import requests
from joblib import Parallel, delayed
import hashlib

with open("links.txt", "w+", encoding="utf-8") as f:
    pass

property_type = "/apartment/for-sale/"
input_file_path = "./links.txt"
output_file_path = "./links_clean.txt"

s = requests.Session()

sitemap = s.get("https://www.immoweb.be/sitemap.xml")
sitemap = sitemap.content
sitemap = BeautifulSoup(sitemap, "xml")
sitemap = sitemap.find_all("loc")
sitemap_url_list = []
for url in range(len(sitemap)):
    if "classifieds" in sitemap[url].text:
        sitemap_url_list.append(sitemap[url].text)


def scrape(url):
    data = s.get(url)
    data = data.content
    soup = BeautifulSoup(data, "xml")
    urls = soup.find_all("url")
    with open("links.txt", "a", encoding="utf-8") as f:
        for url in range(len(urls)):
            if "/en/" in urls[url].find("loc").text and property_type in urls[url].find("loc").text:
                print(urls[url].find("loc").text, file=f)
    print("scrape")


def delete_duplicate(input_file, output_file):
    completed_lines_hash = set()

    output = open(output_file, "w+", encoding="utf-8")

    for line in open(input_file, "r"):

        hash_value = hashlib.md5(line.rstrip().encode("utf-8")).hexdigest()

        if hash_value not in completed_lines_hash:
            output.write(line)
            completed_lines_hash.add(hash_value)
    output.close()


Parallel(n_jobs=-2, verbose=10)(delayed(scrape)(url) for url in sitemap_url_list)

delete_duplicate(input_file_path, output_file_path)
print("Ready")
