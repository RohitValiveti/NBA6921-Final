from flask import Flask, render_template, request, jsonify
from model import predict_delivery_time

app = Flask(__name__)

# Example restaurant data with preset distances (km) and preparation times (min)
restaurants = [
    {"id": 1, "name": "Pasta Palace",   "lat": 40.730610, "lng": -73.935242, "distance_km": 3.2, "Preparation_Time_min": 12},
    {"id": 2, "name": "Sushi Central",   "lat": 40.740610, "lng": -73.925242, "distance_km": 2.5, "Preparation_Time_min": 15},
    {"id": 3, "name": "Taco Tower",      "lat": 40.720610, "lng": -73.945242, "distance_km": 4.1, "Preparation_Time_min": 10},
    {"id": 4, "name": "Burger Barn",     "lat": 40.725,    "lng": -73.92,     "distance_km": 1.8, "Preparation_Time_min": 8},
    {"id": 5, "name": "Vegan Delight",   "lat": 40.735,    "lng": -73.94,     "distance_km": 3.7, "Preparation_Time_min": 14},
]

time_of_day_options = ["Morning", "Afternoon", "Evening", "Night"]
drivers = [
    {"id":1, "name":"Alice", "Courier_Experience_yrs":2},
    {"id":2, "name":"Bob",   "Courier_Experience_yrs":5},
    {"id":3, "name":"Cara",  "Courier_Experience_yrs":1},
]

@app.route('/')
def index():
    # pass restaurants and a dummy user location
    user_loc = {"lat": 40.732, "lng": -73.933}
    return render_template('index.html', restaurants=restaurants, user=user_loc)

@app.route('/order/<int:rest_id>')
def order(rest_id):
    rest = next((r for r in restaurants if r['id'] == rest_id), None)
    return render_template('order.html', restaurant=rest,
                           times=time_of_day_options, drivers=drivers)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    # data contains weather, traffic, time_of_day, vehicle, plus preset distance & prep & driver_exp
    prediction = predict_delivery_time(data)
    return jsonify({"eta_min": prediction})

if __name__ == '__main__':
    app.run(debug=True)