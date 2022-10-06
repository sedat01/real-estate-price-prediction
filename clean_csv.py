import pandas as pd

with open("try_csv.csv","r",encoding="utf-8") as f:
    df = pd.read_csv(f)


df.rename(columns={"Unnamed: 0":"ID"},inplace=True)
df = df.drop(columns=['Available as of', 'Available date',"Neighbourhood or locality","Reference number of the EPC report","Flood zone type",
                      "Website","External reference","Gas, water & electricity","Dining room","Basement surface","Attic surface","Proceedings for breach of planning regulations",
                      "Virtual visit","Accessible for disabled people","Intercom","As built plan","Garden orientation","Armored door","Land is facing street", "Wooded land", "Plot at rear",
                      "Flat land","Caretaker","Secure access / alarm","Air conditioning","Visio phone","Internet","Conformity certification for fuel tanks","Professional space surface"])

df["Primary energy consumption"] = df["Primary energy consumption"].str.extract('(\d+)', expand=False)
df["Primary energy consumption"] = df["Primary energy consumption"].astype(float)

df["Price"] = df["Price"].str.extract('(\d+.\d+)', expand=False)
#df["Price"] = df["Price"].str.replace(",",".")

df["Cadastral income"] = df["Cadastral income"].str.extract('(\d+.\d+)', expand=False)
df["Cadastral income"] = df["Cadastral income"].str.replace(",",".")
df["Cadastral income"] = df["Cadastral income"].str.replace(" ",".")
df["Cadastral income"] = df["Cadastral income"].astype(float)
with open("clean_csv.csv","w+",encoding="utf-8") as f:
    df.to_csv(f,lineterminator='\n')

