from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestRegressor
import pandas as pd
import numpy as np
import joblib
'''
Dropping unnesecary columns
'''
df = pd.read_csv("./model_training/cleaned.csv")
df = df[df["price"]<=1000000]
df = df.drop(["Unnamed: 0","id","type","subtype","Bedroom 4 surface","Bedroom 5 surface","Surface of the plot","Garden","Garden orientation"],axis=1,errors="ignore")

df["Bathrooms"].fillna(1,inplace=True)
df["Double glazing"].fillna(0,inplace=True)

data = df.drop(["zip","Living room surface","Kitchen surface","Bedroom 1 surface","Bedroom 2 surface","Bedroom 3 surface","Terrace surface","Street frontage width",
                "Energy class","Double glazing","Jacuzzi","Sauna"],axis=1,errors="ignore")

'''
Encoding categorical features
'''
encoder_energy = OneHotEncoder(sparse=False)
encoder_province = OneHotEncoder(sparse=False)

energy_type = encoder_energy.fit_transform(data["energy_heatingType"].to_numpy().reshape(-1,1))
province = encoder_province.fit_transform(data["Province"].to_numpy().reshape(-1,1))

energy_type = pd.DataFrame(energy_type,columns=encoder_energy.get_feature_names_out())
province = pd.DataFrame(province,columns=encoder_province.get_feature_names_out())
data = pd.concat([data,energy_type,province],axis=1).drop(['energy_heatingType','Province'],axis=1)
data.dropna(inplace=True)

'''
Train test split
'''
X=data.drop("price",axis=1)
y=data["price"]
X_train,X_test,y_train,y_test = train_test_split(X,y,random_state=41,test_size=0.2)

'''
Training a Random Forest Regressor model
'''
regressor = RandomForestRegressor()
regressor.fit(X_train,y_train)
print(regressor.score(X_test,y_test))
y_rfr=regressor.predict(X_test)

'''
Saving the encoders and the regressor to files
'''
joblib.dump(encoder_energy,"./api/preprocessing/encoder_energy.joblib")
joblib.dump(encoder_province,'./api/preprocessing/encoder_province.joblib')
joblib.dump(regressor,"./api/model/regressor.joblib")

print(X.columns)