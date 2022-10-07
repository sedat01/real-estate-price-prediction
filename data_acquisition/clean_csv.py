import pandas as pd
import numpy as np

with open("try_csv.csv","r",encoding="utf-8") as f:
    df = pd.read_csv(f)


df.rename(columns={"Unnamed: 0":"ID"},inplace=True)
df = df.drop(columns=['Available as of', 'Available date',"Neighbourhood or locality","Reference number of the EPC report","Flood zone type",
                      "Website","External reference","Gas, water & electricity","Dining room","Basement surface","Attic surface","Proceedings for breach of planning regulations",
                      "Virtual visit","Accessible for disabled people","Intercom","As built plan","Garden orientation","Armored door","Land is facing street", "Wooded land", "Plot at rear",
                      "Flat land","Caretaker","Secure access / alarm","Air conditioning","Visio phone","Internet","Conformity certification for fuel tanks","Professional space surface"
                      "Number of floors", "Shower rooms","Age of annuitant","Number of annuitants","Bare ownership sale","Reversionary annuity","Reversionary annuity","Indexed annuity",
                      "Monthly annuity", "Type of building", "Attic", "Sea view", "Professional space", "How many fireplaces?","Obligation to build","Number of floors",
                      "Garden surface","Furnished", "Property name", "Possible priority purchase right", "Latest land use designation", "Agent's name","E-level (overall energy performance)",
                      "Total ground floor buildable", "Living room", ],errors="ignore")

df["Primary energy consumption"] = df["Primary energy consumption"].str.extract('(\d+)', expand=False)
df["Primary energy consumption"] = df["Primary energy consumption"].astype(float)

df["Price"] = df["Price"].str.extract('(\d+.\d+)', expand=False)
df["Price"] = df["Price"].str.replace(",","")
df["Price"] = df["Price"].astype(float)

df["Cadastral income"] = df["Cadastral income"].str.extract('(\d+.\d+)', expand=False)
df["Cadastral income"] = df["Cadastral income"].str.replace(",",".")
df["Cadastral income"] = df["Cadastral income"].str.replace(" ",".")
df["Cadastral income"] = df["Cadastral income"].astype(float)

df["Living area"] = df["Living area"].str.extract('(\d+)')
df["Living room surfacea"] = df["Living room surface"].str.extract('(\d+)')
df["Kitchen surface"] = df["Kitchen surface"].str.extract('(\d+)')
df["Bedroom 1 surface"] = df["Bedroom 1 surface"].str.extract('(\d+)')
df["Bedroom 2 surface"] = df["Bedroom 2 surface"].str.extract('(\d+)')
df["Bedroom 3 surface"] = df["Bedroom 3 surface"].str.extract('(\d+)')
df["Bedroom 4 surface"] = df["Bedroom 4 surface"].str.extract('(\d+)')
#df["Bedroom 5 surface"] = df["Bedroom 5 surface"].str.extract('(\d+)')
df["Terrace surface"] = df["Terrace surface"].str.extract('(\d+)')

df = df.replace(r'\s+( +\.)|#',None,regex=True).replace('',None)
df = df = df.dropna(subset=['Price'])




with open("clean_csv.csv","w+",encoding="utf-8") as f:
    df.to_csv(f,lineterminator='\n')

