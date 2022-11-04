import pandas as pd
import joblib
import numpy as np


def preprocess(input_json):
    encoder_energy = joblib.load('./api/preprocessing/encoder_energy.joblib')
    encoder_province = joblib.load('./api/preprocessing/encoder_province.joblib')
    data = pd.DataFrame.from_dict(input_json,orient="index")
    
    energy_type = encoder_energy.transform(data["energy_heatingType"].to_numpy().reshape(-1,1))
    province = encoder_province.transform(data["Province"].to_numpy().reshape(-1,1))

    energy_type = pd.DataFrame(energy_type,columns=encoder_energy.get_feature_names_out(),index=["0"])
    province = pd.DataFrame(province,columns=encoder_province.get_feature_names_out(),index=["0"])
    data = pd.concat([data,energy_type,province],axis=1).drop(['energy_heatingType','Province'],axis=1)
    return data
