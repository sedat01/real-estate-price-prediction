import link_scrapers
import property_explorer_requests
import pandas as pd


grand_json = {}
grand_tables = {}
sitemap_url = "https://www.immoweb.be/sitemap.xml"
property_type = "house"

provinces = ['antwerp','belgian_luxembourg','brussels','east_flanders','flemish_brabant','hainaut','liege','limburg','namur','waloon_brabant','west_flanders']
provinces1 = ["Antwerp",'Belgian Luxembourg','Brussels','East Falnders','Flemish Brabant','Hainaut','Liege','Limburg','Namur',"Waloon Brabant",'West Flanders']

# link_scrapers.xml_scrape(sitemap_url, property_type)

for province in range(len(provinces)):
    
    grand_json, grand_tables = property_explorer_requests.explorer(province=provinces[province],province1=provinces1[province])
    print(len(grand_json))


df1 = pd.DataFrame.from_dict(grand_json,orient="index")
df2 = pd.DataFrame.from_dict