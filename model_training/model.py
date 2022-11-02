from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestRegressor
import pandas as pd
import numpy as np
import joblib

df = pd.read_csv("cleaned.csv")
df = df[df["price"]<=1000000]
df.isnull().sum()
df.head()
df = df.drop(["Unnamed: 0","id","type","subtype","Bedroom 4 surface","Bedroom 5 surface","Surface of the plot","Garden","Garden orientation"],axis=1,errors="ignore")
df.isnull().sum()

df["Bathrooms"].fillna(1,inplace=True)
df["Double glazing"].fillna(0,inplace=True)
df.isnull().sum()

data = df.drop(["Living room surface","Kitchen surface","Bedroom 1 surface","Bedroom 2 surface","Bedroom 3 surface","Terrace surface","Street frontage width",
                "Energy class","Double glazing","Jacuzzi","Sauna"],axis=1,errors="ignore")

data["energy_heatingType"].unique()
print(data.isnull().sum())

encoder_energy = OneHotEncoder(sparse=False)
encoder_province = OneHotEncoder(sparse=False)

energy_type = encoder_energy.fit_transform(data["energy_heatingType"].to_numpy().reshape(-1,1))
province = encoder_province.fit_transform(data["Province"].to_numpy().reshape(-1,1))

print(encoder_energy.get_feature_names_out())
print(energy_type)
energy_type = pd.DataFrame(energy_type,columns=encoder_energy.get_feature_names_out())
province = pd.DataFrame(province,columns=encoder_province.get_feature_names_out())
print(energy_type)
data = pd.concat([data,energy_type,province],axis=1).drop(['energy_heatingType','Province'],axis=1)
print(data.columns)
data.dropna(inplace=True)


X=data.drop("price",axis=1)
y=data["price"]
X_train,X_test,y_train,y_test = train_test_split(X,y,random_state=41,test_size=0.2)

print(X.shape)

regressor = RandomForestRegressor()
regressor.fit(X_train,y_train)
print(regressor.score(X_test,y_test))
y_rfr=regressor.predict(X_test)

joblib.dump(encoder_energy,"encoder_energy.joblib")
joblib.dump(encoder_province,'encoder_province.joblib')
joblib.dump(regressor,"regressor.joblib")