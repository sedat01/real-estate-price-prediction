import time

import requests
from bs4 import BeautifulSoup
import json
import re
import collections
import pandas as pd
from joblib import Parallel, delayed
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


def explorer(province,province1,start=0, number_links="max", selenium=False):
    def open_page(url):

        options = Options()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(executable_path=r"C:\chromedriver.exe", options=options)
        driver.minimize_window()
        driver.get(url)
        driver.implicitly_wait(10)
        try:
            elem = driver.find_element(By.XPATH, '//*[@id="uc-btn-accept-banner"]')
            elem.click()
            pg_code = driver.page_source
            return pg_code
        except:
            pass

        time.sleep(0.5)

    columns_json = ['subtype', 'price', 'zip', 'kitchen_type', 'building_constructionYear', 'building_condition',
                    'energy_heatingType', 'bedroom_count', 'land_surface', 'basementExists',
                    'outdoor_terrace_exists',
                    'specificities_SME_office_exists', 'wellnessEquipment_hasSwimmingPool',
                    'parking_parkingSpaceCount_indoor',
                    'parking_parkingSpaceCount_outdoor']
    columns_tables = ['Number of frontages', 'Living area', 'Bedrooms', 'Bathrooms', 'Surface of the plot',
                      'Primary energy consumption',
                      'Energy class', 'Yearly theoretical total energy consumption', 'Address', 'Toilets',
                      'Garden surface',
                      'Terrace surface', 'Heat pump', 'Building condition', 'Terrace', 'Kitchen surface',
                      'Bedroom 1 surface',
                      'Bedroom 2 surface', 'Bedroom 3 surface']

    id_data = {}
    data_all_tables = {}

    def explore_property(url, selenium):
        def flatten(d, parent_key='', sep='_'):
            items = []
            for k, v in d.items():
                new_key = parent_key + sep + k if parent_key else k
                if isinstance(v, collections.abc.MutableMapping):
                    items.extend(flatten(v, new_key, sep=sep).items())
                else:
                    items.append((new_key, v))
            return dict(items)

        session = requests.Session()
        header = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
            'referer': 'https://www.immoweb.be/en'
        }

        with open("log2_explorer.txt", "a+", encoding="utf-8") as log:
            pat1 = "\\n"
            pat2 = "  "
            pat = r'|'.join((pat1, pat2))
            if selenium:
                try:
                    page_source = open_page(url)
                    soup = BeautifulSoup(page_source, "lxml")
                except:
                    print(f"Exception retrieving page source url= {url}", file=log)
                    pass
            else:
                try:
                    page_source = session.get(url, headers=header)
                    soup = BeautifulSoup(page_source.text, "lxml")
                except:
                    print(f"Exception retrieving page source url= {url}", file=log)
                    pass
            data_json = {}

            try:
                scripts = soup.select("script")
                initial_script = scripts[1].text.strip().replace(" ", "").replace("\n", "")
                initial_script = re.sub('w.+?"classified":', "", initial_script)
                initial_script = re.sub(',"customer".+', "", initial_script)
                data_json = json.loads(initial_script)
                data_json = flatten(data_json)
                data_json["Province"] = province1
                id_data[data_json["id"]] = data_json
                #id_data["Province"] = "Antwerp"
                df_json = pd.DataFrame.from_dict(id_data, orient="index")
                #df_json = df_json[columns_json]
                # df_json.to_csv("from_json.csv",mode='a')
            except:
                print(f"Exception getting data from source url= {url}", file=log)

            try:
                property_id = soup.find("div", class_="classified__header--immoweb-code")
                property_id = property_id.text
                property_id = re.sub("Immoweb code : ", "", property_id)
                property_id = re.sub(pat, "", property_id)
            except:
                print(f"Exception getting property id url= {url}", file=log)
            data = {}
            try:
                tables = soup.find_all("tbody", class_="classified-table__body")
                for table in tables:
                    row = table.select("tr", class_="classified-table__row")

                    for element in row:
                        keys = element.find_all("th", class_="classified-table__header")
                        values = element.find_all("td", class_="classified-table__data")
                        for i in range(len(keys)):
                            key = str(keys[i])
                            key = re.sub("<.+?>", "", key)
                            key = key.strip()
                            value = str(values[i])
                            value = re.sub("<.+?>", "", value)
                            value = value.strip()
                            data[key] = value
                
                for key, value in data.items():
                    data[key] = re.sub(pat, "", value)
                    for key1, value1 in data.items():
                        data[key1] = re.sub(pat, "", value1)
                data["Province"] = province1
                data_all_tables[property_id] = data
                #data_all_tables["Province"] = "Antwerp"
                df_tables = pd.DataFrame.from_dict(data_all_tables, orient="index")
                #df_tables = df_tables[columns_tables]
                # df_tables.to_csv("from_tables.csv","a")
            except:
                print("Data error:", file=log)

        # df_all = pd.concat(df_json, df_tables)

    with open(f"links_{province}.txt", "r", encoding="utf-8") as url_list_file:
        full_url_list = url_list_file.readlines()
    if number_links == "max":
        print(f"Number of links to scrape {len(full_url_list)}")
        Parallel(n_jobs=-3, require="sharedmem", verbose=10)(
            delayed(explore_property)(url, selenium) for url in full_url_list)

    else:
        url_list = []
        for link in range(start, number_links):
            url_list.append(full_url_list[link])
        Parallel(n_jobs=-3, require="sharedmem", verbose=10)(
            delayed(explore_property)(url, selenium) for url in url_list)

    
    df1 = pd.DataFrame.from_dict(id_data, orient="index")
    df1.to_csv(f"from_json_{province}.csv")
    df2 = pd.DataFrame.from_dict(data_all_tables, orient="index")
    df2.to_csv(f"from_tables_{province}.csv")
    df1 = pd.concat([df1, df2], axis=1)
    df1.to_csv(f"data_all_{province}.csv")
    return id_data,data_all_tables