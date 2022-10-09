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


def explorer(number_links="max", selenium=False):
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

        id_data = {}
        data_all_tables = {}
        session = requests.Session()
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

        with open("log_explorer.txt", "a+", encoding="utf-8") as log:
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
                    page_source = session.get(url, headers)
                    soup = BeautifulSoup(page_source.text, "lxml")
                    print(soup)
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
                id_data[data_json["id"]] = data_json
                df_json = pd.DataFrame.from_dict(id_data, orient="index")
                df_json = df_json[columns_json]
                df_json.to_csv("from_json.csv")
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

                data_all_tables[property_id] = data
                df_tables = pd.DataFrame.from_dict(data_all_tables, orient="index")
                df_tables = df_tables[columns_tables]
                df_tables.to_csv("from_tables.csv")
            except:
                print("Data error:", file=log)

        df_all = pd.concat(df_json, df_tables)
        df_all.to_csv("Data_all.csv")

    with open("links_clean.txt", "r", encoding="utf-8") as url_list_file:
        full_url_list = url_list_file.readlines()
    if number_links == "max":
        Parallel(n_jobs=-1, prefer="threads")(delayed(explore_property)(url, selenium) for url in full_url_list)

    else:
        url_list = []
        for link in range(number_links):
            url_list.append(full_url_list[link])
        Parallel(n_jobs=-3, require="sharedmem", verbose=10)(delayed(explore_property)(url, selenium) for url in url_list)
