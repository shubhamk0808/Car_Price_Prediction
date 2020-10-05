from flask import Flask, render_template,url_for,request
import jsonify
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler
app = Flask(__name__)



model = pickle.load(open('random_forest_regression_model.pkl', 'rb'))
@app.route('/',methods=['GET'])
def home():
    return render_template('HomePage.html')


standard_to = StandardScaler()
@app.route("/predict", methods=['POST'])
def predict():
    #Fuel_Type_Diesel=0
    if request.method == 'POST':
        Year = int(request.form['pur_year'])
        Year=2020-Year

        Present_Price=float(request.form['sh_price'])
        
        Kms_Driven=int(request.form['km'])        
        # Kms_Driven2=np.log(Kms_Driven)
        
        Owner=int(request.form['owner'])
        
        Fuel_Type_Petrol=request.form['fuel']
        if(Fuel_Type_Petrol=='petrol'):
            Fuel_Type_Petrol=1
            Fuel_Type_Diesel=0
        elif(Fuel_Type_Petrol=='diesel'):
            Fuel_Type_Petrol=0
            Fuel_Type_Diesel=1
        else:
            Fuel_Type_Petrol=0
            Fuel_Type_Diesel=0
        
        
        Seller_Type_Individual=request.form['seller']
        if(Seller_Type_Individual=='individual'):
            Seller_Type_Individual=1
        else:
            Seller_Type_Individual=0

        Transmission_Mannual=request.form['trans']
        if(Transmission_Mannual=='mannual'):
            Transmission_Mannual=1
        else:
            Transmission_Mannual=0

        prediction=model.predict([[Present_Price,Kms_Driven,Owner,Year,Fuel_Type_Diesel,Fuel_Type_Petrol,Seller_Type_Individual,Transmission_Mannual]])
        output=round(prediction[0],2)
        if output<0:
            return render_template('HomePage.html',prediction_texts="Sorry you cannot sell this car")
        else:
            return render_template('HomePage.html',prediction_text="{} lakhs".format(output))
    else:
        return render_template('HomePage.html')

if __name__=="__main__":
    app.run(debug=True)