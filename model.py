def predict_delivery_time(features):
    # Replace with actual model inference
    base = features['distance_km'] * 2 + features['Preparation_Time_min']
    weather_factor = {'Clear':1, 'Rain':1.3, 'Snow':1.5}.get(features['Weather'],1)
    traffic_factor = {'Low':1, 'Medium':1.2, 'High':1.5}.get(features['Traffic_Level'],1)
    time_factor = 1 + (features['Courier_Experience_yrs'] * -0.05)
    eta = base * weather_factor * traffic_factor * time_factor
    return round(max(5, eta))