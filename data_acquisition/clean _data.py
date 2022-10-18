import pandas as pd
import seaborn as sns
data = pd.read_csv("collected.csv",low_memory=False)
print(data.shape)
data = data.drop_duplicates()
#print(data.columns.tolist())
data = data.drop(["Unnamed: 0.2","Unnamed: 0.1","Unnamed: 0","Unnamed: 0.3","transactionType","outdoor_garden_surface","building_constructionYear","visualisationOption","atticExists","basementExists","Available as of","Construction year",
                  "Building condition","Bedrooms","Basement","Furnished","Reference number of the EPC report",
                  "COв‚‚ emission","Yearly theoretical total energy consumption","As built plan","Planning permission obtained",
                  "Subdivision permit","Possible priority purchase right","Proceedings for breach of planning regulations",
                  "Flood zone type","Latest land use designation","Price","Cadastral income","Tenement building",
                  "Website","External reference","Province.1","Neighbourhood or locality","Width of the lot on the street",
                  "Gas, water &amp; electricity","Conformity certification for fuel tanks","Available date",
                  "Obligation to build","Covered parking spaces","How many fireplaces?","Dressing room","Office","Professional space surface",
                  "Professional space","Basement surface","Attic surface","Armored door","Land is facing street",
                  "Wooded land","Plot at rear","Flat land","Connection to sewer network","Garden surface","Terrace orientation",
                  "Caretaker","Elevator","Accessible for disabled people","Intercom","Secure access / alarm","Air conditioning",
                  "TV cable","Visio phone","Internet","Heat pump","Photovoltaic solar panels","Thermic solar panels","Common water heater",
                  "Type of building","Office surface","Dining room","Terrace","Virtual visit","Shower rooms","Total ground floor buildable",
                  "Laundry room","Attic","E-level (overall energy performance)","Living room","Isolated","Monthly charges",
                  "Percentage rented","Current monthly revenue","Property name","Number of annexes","Agent's name","EPC description",
                  "Extra information","Venue of the sale","Single session","Terms of visit","Starting price","Lump sum","Monthly annuity",
                  "Indexed annuity","Reversionary annuity","Bare ownership sale","Number of annuitants","Age of annuitant",
                  "Maximum duration of annuity","Age of annuitants","Date of the sale","Value of the property","Sea view",
                  "Architectural style","Construction delay","Energy performance","Is architect included in sale price",
                  "Is blower door test included","Kitchen included","Is outskirts arrangements included","Is safety coordinator included in sale price",
                  "Is soil investigation included in price","Address","Is stability engineer included","Minimum overbid","Price after higher bid","Outdoor parking spaces","Kitchen type",
                  "Monthly rental price","CO₂ emission","Swimming pool"],axis=1,errors="ignore")
print(data.columns)

#data = data[len(data.price)<8] 
#data = data["price"].astype(str)
data.shape
#data["price"] = pd.to_numeric(data["price"])
data['price'].dtype
data = data.astype("str",copy=False)
data = data[data["price"].map(len)<8]
data = data[data["price"].str.isdigit()]
data["price"] = data["price"].apply(pd.to_numeric)
data = data[data["price"] >= 120_000]
data = data[data["price"] <= 1_500_000]
print(data.price.dtype)
kitchen_map = {'nan':0,"notinstalled":0,"semiequipped":1,"usasemiequipped":1,"installed":2,"usainstalled":2,"usauninstalled":2,
               "hyperequipped":3,"usahyperequipped":3}
data.replace({"kitchen_type":kitchen_map},inplace=True)
state_map = {'asnew':2,'good':1,'justrenovated':1,'tobedoneup':0,'torenovate':0,'torestore':0,'nan':1}
data.replace({"building_condition":state_map},inplace=True)
boolean_exists = {"True":1,"Yes":1,"No":0, "nan":0, "False":0}
boolean_list = ["outdoor_terrace_exists","specificities_SME_office_exists","wellnessEquipment_hasSwimmingPool","parking_parkingSpaceCount_indoor",
                "parking_parkingSpaceCount_outdoor","condition_isNewlyBuilt","outdoor_terrace_exists","specificities_SME_office_exists","wellnessEquipment_hasSwimmingPool",
                "parking_parkingSpaceCount_indoor","parking_parkingSpaceCount_outdoor","condition_isNewlyBuilt","Jacuzzi","Sauna"]
for key in boolean_list:
    data.replace({key:boolean_exists},inplace=True)
data.replace({"Number of frontages":{"nan":1}},inplace=True)
data.replace({"Toilets":{"nan":1}},inplace=True)
scalar_list = ["Living area","Living room surface","Kitchen surface","Bedroom 1 surface","Bedroom 2 surface","Bedroom 3 surface","Bedroom 4 surface","Bedroom 5 surface",
               "Surface of the plot","Terrace surface","Primary energy consumption","Street frontage width"]
for scalar in scalar_list:
    
    data[scalar] = data[scalar].str.extract('(\d+)').astype(float)       

print(data.shape)
data = data.drop_duplicates(subset=data.columns.difference(["id"]))
#data["kitchen_type"] = data.loc[data['kitchen_type'] == "notinstalled", "kitchen_type"] = 0
print(data.shape)
data = data[~data.subtype.isin(["castle","pavilion","otherproperty","chalet","bungalowm","countrycottage","mixedusebuilding"])]
#data = data[~data.isin(["nan"]).any(axis=1)]
print(data.shape)



import matplotlib.pyplot as plt
plt.show()
data.to_csv("collected1.csv")