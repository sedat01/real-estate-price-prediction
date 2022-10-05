from bs4 import BeautifulSoup
import link_finder2



with open("./links.txt","r",encoding='utf-8') as f:
    url_list = f.readlines()
    
page_source = link_finder2.open_page(url_list[1])
data = {}
soup = BeautifulSoup(page_source,"lxml")
tables = soup.find_all("tbody", class_="classified-table__body")
for table in tables:
    table = table.select("tr")
    
    for item in range(len(table)):
        keys = table[item].select("th")
        values = table[item].select("td")
        for i in range(len(keys)):
            with open("table_test.txt","w+",encoding='utf-8') as f:
                try:
                    print(keys[i].text.strip(),values[i].text.strip(),"stop",file=f)
                    key = keys[i].text.strip();value = values[i].text.strip()
                    data [key] = value
                except:
                    continue
            
with open("./table_test.txt","w+",encoding="utf-8") as f:
    f.write(data)
            
            