from flask import Flask, request
import joblib
from preprocessing.preprocess import preprocess


app = Flask(__name__)
regressor = joblib.load('./api/model/regressor.joblib')
@app.route('/')
def alive():
   return 'Alive and kicking'

@app.route('/predict',methods=["GET","POST"])
def predict():
    if request.method == "GET":
        return 'This is house price predictor'
    elif request.method == "POST":
        input_json = request.get_json(force=True)
        cleaned_json = preprocess(input_json)
        #print(cleaned_json)
        prediction = regressor.predict(cleaned_json)
        prediction = str(prediction)
        prediction = prediction.strip("[].")   
        
        return {"predicted_price":float(prediction)}
    else:
        return {"error":"Use POST method to send json"}


if __name__ == '__main__':
   app.run(port=5000,debug=True)