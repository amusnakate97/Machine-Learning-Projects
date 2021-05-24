import os

from flask import Flask, render_template, request
import jsonify
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)
model = pickle.load(open('random_forest_regression_model.pkl', 'rb'))


@app.route('/', methods=['GET'])
def Home():
    return render_template('index.html')


standard_to = StandardScaler()


@app.route("/predict", methods=['POST'])
def predict():
    if request.method == 'POST':
        Age = int(request.form['age'])
        BMI = float(request.form['bmi'])
        children = float(request.form['children'])

        Region = request.form['region']
        northwest=0
        southeast=0
        southwest=0
        if (Region == 'northwest'):
            northwest = 1
            southeast = 0
            southwest = 0
        elif (Region == 'southeast'):
            northwest = 0
            southeast = 1
            southwest = 0
        elif (Region == 'southwest'):
            northwest = 0
            southeast = 0
            southwest = 1
        else:
            northwest = 0
            southeast = 0
            southwest = 0

        gender = request.form['gender']
        if (gender == 'Male'):
            gender = 1
        else:
            gender = 0


        smoking_status= request.form['smoke_status']
        if (smoking_status == 'yes'):
            smoking_status = 1

        else:
            smoking_status = 0



        prediction = model.predict([[Age,BMI,children,gender,smoking_status,northwest,southeast,southwest]])
        output = prediction[0]

        return render_template('index.html', prediction_text="Insurance cost will be around {}".format(output))

    else:
        return render_template('index.html')


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, port=port)

