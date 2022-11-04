from flask import Flask, request
from flask_expects_json import expects_json
import joblib
from preprocessing.preprocess import preprocess


app = Flask(__name__)

schema = {
  "type": "object",
  "properties": {
    "0": {
      "type": "object",
      "properties": {
        "kitchen_type": {
          "type": "integer"
        },
        "building_condition": {
          "type": "integer"
        },
        "certificates_primaryEnergyConsumptionLevel": {
          "type": "integer"
        },
        "bedroom_count": {
          "type": "integer"
        },
        "land_surface": {
          "type": "integer"
        },
        "outdoor_terrace_exists": {
          "type": "integer"
        },
        "specificities_SME_office_exists": {
          "type": "integer"
        },
        "wellnessEquipment_hasSwimmingPool": {
          "type": "integer"
        },
        "parking_parkingSpaceCount_indoor": {
          "type": "integer"
        },
        "parking_parkingSpaceCount_outdoor": {
          "type": "integer"
        },
        "condition_isNewlyBuilt": {
          "type": "integer"
        },
        "Number of frontages": {
          "type": "integer"
        },
        "Living area": {
          "type": "integer"
        },
        "Bathrooms": {
          "type": "integer"
        },
        "Toilets": {
          "type": "integer"
        },
        "energy_heatingType": {
          "type": "string"
        },
        "Province": {
          "type": "string"
        }
      },
      "required": [
        "kitchen_type",
        "building_condition",
        "certificates_primaryEnergyConsumptionLevel",
        "bedroom_count",
        "land_surface",
        "outdoor_terrace_exists",
        "specificities_SME_office_exists",
        "wellnessEquipment_hasSwimmingPool",
        "parking_parkingSpaceCount_indoor",
        "parking_parkingSpaceCount_outdoor",
        "condition_isNewlyBuilt",
        "Number of frontages",
        "Living area",
        "Bathrooms",
        "Toilets",
        "energy_heatingType",
        "Province"
      ]
    }
  },
  "required": [
    "0"
  ]
}


help = '''

Example JSON:</br>

{"0":{</br>
 "kitchen_type":0,</br>
"building_condition":0,</br>
"certificates_primaryEnergyConsumptionLevel":250,</br>
 "bedroom_count":3,</br>
"land_surface":200,</br>
"outdoor_terrace_exists":1,</br>
"specificities_SME_office_exists":0,</br>
 "wellnessEquipment_hasSwimmingPool":0,</br>
"parking_parkingSpaceCount_indoor":0,</br>
 "parking_parkingSpaceCount_outdoor":2,</br>
"condition_isNewlyBuilt":0,</br>
"Number of frontages":2,</br>
"Living area":120,</br>
"Bathrooms":1,</br>
"Toilets":1,</br>
"energy_heatingType":"gas",</br>
  "Province":"East Flanders"}}</br>
  </br>
  The initial "0" is required in order to orient the data frame in the correct order
  
  
  Kitchen type can be 0,1,2,3 where 0 i unequipped, 1 - semiequiped, 2 - equiped, 3 - hyperequiped</br>
  Building condition can be 0,1,2 where 0 - needs major renovation, 1 - good or need minor things like paint, 2 - as new</br>
  Certificates_primaryEnergyConsumptionLevel is the EPC figure in kW/m2</br>
  </br>
  Energy heating type can be carbon, electric, fueloil, gas, other, pellet, solar", wood" </br>
  Province can be Antwerp,Belgian Luxembourg, Brussels, East Falnders, Flemish Brabant, Hainaut, Liege, Limburg, Namur, Waloon Brabant, West Flanders
  
  
  
'''

regressor = joblib.load('./api/model/regressor.joblib')
@app.route('/')
def alive():
   return 'Alive and kicking'

@app.route('/predict',methods=["GET","POST"])
@expects_json(schema,ignore_for=['GET'])
def predict():
    if request.method == "GET":
        return  help
    elif request.method == "POST":
        input_json = request.get_json(force=True)
        cleaned_json = preprocess(input_json)
        prediction = regressor.predict(cleaned_json)
        prediction = str(prediction)
        prediction = prediction.strip("[].")   
        
        return {"predicted_price":float(prediction),
                "status":200}
    else:
        return {"error":"Use POST method to send json"}


if __name__ == '__main__':
   app.run(host="0.0.0.0",port=5000,debug=True)