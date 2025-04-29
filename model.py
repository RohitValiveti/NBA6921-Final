import pandas as pd
import re
from tqdm.notebook import tqdm
import json
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, balanced_accuracy_score, f1_score, precision_score, recall_score, confusion_matrix, roc_curve, roc_auc_score
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import openai
from openai import OpenAI

API_KEY = ""

def train_model():
    ## CHANGE THIS IF YOU WANT
    GOOGLE_SPREADSHEET_LINK = "https://docs.google.com/spreadsheets/d/1rNhxGcKdDnWhLzD8WhOLoR62STgK8NYtrTv6NfCFWLw/edit?usp=sharing"

    sheet_id = GOOGLE_SPREADSHEET_LINK.split("/")[5]

    url=f'https://docs.google.com/spreadsheet/ccc?key={sheet_id}&output=xlsx'
    dataset_train = pd.read_excel(url, sheet_name="train")
    dataset_test = pd.read_excel(url, sheet_name="test")

    print("Train data size:", len(dataset_train))
    print("Test data size:", len(dataset_test))

    # encode categorical variables
    columns_to_encode = ["Weather", "Traffic_Level", "Time_of_Day", "Vehicle_Type"]
    dataset_train = pd.get_dummies(dataset_train, columns=columns_to_encode)
    dataset_test = pd.get_dummies(dataset_test, columns=columns_to_encode)

    features = ["Distance_km", "Weather_Clear", "Weather_Rainy", "Traffic_Level_Low", "Traffic_Level_Medium", "Traffic_Level_High",
            "Time_of_Day_Morning", "Time_of_Day_Afternoon", "Time_of_Day_Evening", "Vehicle_Type_Car"]
    Xtrain = dataset_train[features]
    # Xtest = dataset_test[features]

    ytrain = dataset_train["Delivery_Time_min"]
    # ytest = dataset_test["Delivery_Time_min"]

    clf = RandomForestRegressor(n_estimators=100, random_state=42)
    clf.fit(Xtrain, ytrain)

    joblib.dump(clf, 'delivery_time_model.pkl')
    print("Model trained and saved as delivery_time_model.pkl")

def predict_delivery_time(data):
    model = joblib.load('delivery_time_model.pkl')
    
    feature_vector = [
        data.get('distance_km', 0),  # Distance_km
        1 if data.get('Weather', '') == 'Clear' else 0,  # Weather_Clear
        1 if data.get('Weather', '') == 'Rainy' else 0,  # Weather_Rainy
        1 if data.get('Traffic_Level', '') == 'Low' else 0,    # Traffic_Level_Low
        1 if data.get('Traffic_Level', '') == 'Medium' else 0,  # Traffic_Level_Medium
        1 if data.get('Traffic_Level', '') == 'High' else 0,    # Traffic_Level_High
        1 if data.get('Time_of_Day', '') == 'Morning' else 0,   # Time_of_Day_Morning
        1 if data.get('Time_of_Day', '') == 'Afternoon' else 0, # Time_of_Day_Afternoon
        1 if data.get('Time_of_Day', '') == 'Evening' else 0,   # Time_of_Day_Evening
        1 if data.get('Vehicle_Type', '') == 'Car' else 0      # Vehicle_Type_Car
    ]
    
    # Make predictions
    prediction = model.predict([feature_vector])
    
    return (prediction[0])

def chatbot_message(feature_data):
    client = OpenAI(api_key=API_KEY)
    openai.api_key = API_KEY
    feature_data_read = "\n".join(f"{k}: {v}" for k, v in feature_data.items())

    PROMPT_TEMPLATE = f"""
      You are a friendly customer support assistant working for a courier service (e.g., UberEats)
      Given these inputs: 
      {feature_data_read}
      Write a concise and plausible explanation in a professional tone for why the customer's delivery is late.
      Do not include any sign-off ("Best regards"), just the explanation.
    """

    # print(feature_data_read)
    prompt = PROMPT_TEMPLATE.format(input=feature_data_read)  
    # print(prompt)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
          {"role": "system", "content": prompt}
        ]
    )
    message = response.choices[0].message.content
    return message
