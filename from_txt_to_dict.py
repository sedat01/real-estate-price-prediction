from io import StringIO
import pandas as pd
import json
import sys



data = {}

with open ("current.txt", "r", encoding="utf-8") as f:
     
    data = f.readlines()    
    
test_data = StringIO(data)
#print(data[1][25])
#data = json.loads(data)    
#print(data)
# data = json.loads(data)
#print(type(data))
#df = pd.DataFrame.from_dict(data, orient="index")
#print(df)
df = pd.read_csv(test_data) 
print(df)