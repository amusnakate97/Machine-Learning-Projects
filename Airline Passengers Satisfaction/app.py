from flask import Flask, request, render_template
import sklearn
import pickle
import pandas as pd

app = Flask(__name__)
model = pickle.load(open("random_forest_classification_model.pkl", "rb"))


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/predict", methods=["GET", "POST"])
def predict():
    if request.method == "POST":
        # Total Stops
        inflight_wifi_service = int(request.form["wifi"])
        online_boarding = int(request.form["online"])
        inflight_entertainment = int(request.form["Entertainment"])
        seat_comfort = int(request.form["seat"])
        ease_of_online_booking = int(request.form["online_book"])

        checkin_service = int(request.form["checkin"])
        onboard_service = int(request.form["onboard_service"])
        inflight_service = int(request.form["inflight_service"])
        baggage_handling = int(request.form["baggage"])
        cleanliness = int(request.form["cleanliness"])
        leg_room_service = int(request.form["leg_room"])

        # Airline
        # AIR ASIA = 0 (not in column)

        personal_type_of_travel = request.form['travel_type']
        if (personal_type_of_travel == 'Personal'):
            personal_type_of_travel=1
        else:
            personal_type_of_travel=0

        class_of_customer=request.form['class_travel']
        if class_of_customer=='Business':
            class_of_customer=1
        elif class_of_customer=='Eco_Plus':
            class_of_customer=2
        else:
            class_of_customer=3

        disloyal_customer_type = request.form['cust_type']
        if (disloyal_customer_type == 'disloyal'):
            disloyal_customer_type = 1
        else:
            disloyal_customer_type = 0
        #     Air_India,
        #     Multiple_carriers,
        #     SpiceJet,
        #     Vistara,
        #     GoAir,
        #     Multiple_carriers_Premium_economy,
        #     Jet_Airways_Business,
        #     Vistara_Premium_economy,
        #     Trujet)



    prediction = model.predict([[inflight_wifi_service, online_boarding, personal_type_of_travel,
       class_of_customer, disloyal_customer_type, inflight_entertainment,
       seat_comfort, ease_of_online_booking, checkin_service,
       onboard_service, inflight_service, baggage_handling,
       cleanliness, leg_room_service]])

    output = prediction[0]

    if output==0:
        return render_template('home.html', prediction_text="You need to make improvements in your services")
    else:
        return render_template('home.html', prediction_text="Keep it up!! Customers are satisfies")


    return render_template("home.html")


if __name__ == "__main__":
    app.run(debug=True)
