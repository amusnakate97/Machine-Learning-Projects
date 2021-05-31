import os

from flask import Flask, render_template, request
import jsonify
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)
model = pickle.load(open('cafe.pkl', 'rb'))


@app.route('/', methods=['GET'])
def Home():
    return render_template('home.html')


standard_to = StandardScaler()


@app.route("/predict", methods=['POST'])
def predict():
    Fuel_Type_Diesel = 0
    if request.method == 'POST':
        online_table = request.form['online_table']
        if online_table=='yes':
            online_table=1
        else:
            online_table=0
        online_delivery = request.form['online_delivery']
        if online_delivery == 'yes':
            online_delivery = 1
        else:
            online_delivery = 0
        online_active = request.form['online_active']
        if online_active == 'yes':
            online_active = 1
        else:
            online_active = 0
        p_range = int(request.form['range'])
        votes = int(request.form['votes'])
        avg = int(request.form['avg'])

        city=request.form['City']
        city_arr=[]
        if (city == 'New Delhi'):
            city_arr=[1,0,0,0]
        elif(city == 'Gurgaon'):
            city_arr=[0,1,0,0]
        elif(city=='Noida'):
            city_arr=[0,0,1,0]
        elif (city == 'Faridabad'):
            city_arr = [0, 0, 0, 1]

        else:
            city_arr = [0, 0, 0, 0]
        selected = request.form.getlist('cusines')
        print(selected)
        any_selected = bool(selected)
        cuisines=['Bakery', 'Seafood', 'European', 'Continental',
       'Asian', 'Chinese', 'North Indian', 'Cafe', 'Italian', 'Desserts',
       'Thai', 'Mughlai', 'Mexican', 'American', 'Fast Food', 'South Indian',
       'Street Food']
        cuisines_arr=[]
        for item in cuisines:
            if item in selected:
                cuisines_arr.append(1)
            else:
                cuisines_arr.append(0)
        featueres=[online_table, online_delivery, online_delivery,
        p_range, votes, avg]+city_arr+cuisines_arr
        prediction = model.predict([featueres])
        output = round(prediction[0], 2)
        print(output)
        return render_template('home.html', prediction_texts="Predicted rating is  {}".format(output))

    else:
        return render_template('home.html')


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, port=port)

