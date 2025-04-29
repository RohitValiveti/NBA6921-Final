from flask import Flask, render_template, request, jsonify
from model import predict_delivery_time, train_model

app = Flask(__name__)

# Example restaurant data with preset distances (km) and preparation times (min)
restaurants = [
    {"id": 1, "name": "Taste of Thai",   "lat": 42.437810, "lng": -76.507968, "distance_km": 3.2, "Preparation_Time_min": 12},
    {"id": 2, "name": "Collegetown Bagels",   "lat": 42.4421999, "lng": -76.4855129, "distance_km": 2.5, "Preparation_Time_min": 15},
    {"id": 3, "name": "Pho Time",      "lat": 42.441837, "lng": -76.484625, "distance_km": 4.1, "Preparation_Time_min": 10},
    {"id": 4, "name": "New Delhi Diamond's",     "lat": 42.438730,    "lng": -76.499380,     "distance_km": 1.8, "Preparation_Time_min": 8},
    {"id": 5, "name": "Thompson and Bleecker",   "lat": 42.440285,    "lng": -76.496161,     "distance_km": 3.7, "Preparation_Time_min": 14},
    {"id": 6, "name": "Texas Roadhouse",   "lat": 42.4307828,    "lng": -76.5075881,     "distance_km": 3.7, "Preparation_Time_min": 20},
    {"id": 7, "name": "McDonald's",   "lat": 42.4219755,    "lng": -76.5177047,     "distance_km": 3.7, "Preparation_Time_min": 5},

]

time_of_day_options = ["Morning", "Afternoon", "Evening", "Night"]
drivers = [
    {"id":1, "name":"Alice", "Courier_Experience_yrs":2},
    {"id":2, "name":"Bob",   "Courier_Experience_yrs":5},
    {"id":3, "name":"Cara",  "Courier_Experience_yrs":1},
]

# Train the model once at startup
train_model()

@app.route('/')
def index():
    user_loc = {"lat": 42.4219755, "lng": -76.5177047}
    return render_template('index.html', restaurants=restaurants, user=user_loc)

@app.route('/order/<int:rest_id>')
def order(rest_id):
    rest = next((r for r in restaurants if r['id'] == rest_id), None)
    return render_template('order.html', restaurant=rest,
                           times=time_of_day_options, drivers=drivers)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        
        # create feature dictionary
        feature_data = {
            'distance_km': data.get('distance_km', 0),
            'Preparation_Time_min': data.get('Preparation_Time_min', 0),
            'Weather': data.get('Weather', ''),
            'Traffic_Level': data.get('Traffic_Level', ''),
            'Time_of_Day': data.get('Time_of_Day', ''),
            'Vehicle_Type': data.get('Vehicle_Type', ''),
            'Courier_Experience_yrs': data.get('Courier_Experience_yrs', 0)
            
        }

        prediction = predict_delivery_time(feature_data)
        
        return jsonify({"eta_min": round(prediction, 1)})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)