import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from model import predict_delivery_time, train_model, chatbot_message

# Load restaurant data
df = pd.DataFrame([
    {"id": 1, "name": "Taste of Thai", "lat": 42.437810, "lon": -76.507968, "distance_km": 2.7, "Preparation_Time_min": 15},
    {"id": 2, "name": "Collegetown Bagels", "lat": 42.442200, "lon": -76.485513, "distance_km": 0.2, "Preparation_Time_min": 10},
    {"id": 3, "name": "Pho Time", "lat": 42.441837, "lon": -76.484625, "distance_km": 0.1, "Preparation_Time_min": 13},
    {"id": 4, "name": "New Delhi Diamond's", "lat": 42.438730, "lon": -76.499380, "distance_km": 1.8, "Preparation_Time_min": 17},
    {"id": 5, "name": "Thompson and Bleecker", "lat": 42.440280, "lon": -76.496161, "distance_km": 1.12, "Preparation_Time_min": 23},
    {"id": 6, "name": "Texas Roadhouse", "lat": 42.430783, "lon": -76.507588, "distance_km": 3.52, "Preparation_Time_min": 22},
    {"id": 7, "name": "McDonald's", "lat": 42.421976, "lon": -76.517705, "distance_km": 4.16, "Preparation_Time_min": 3}
])

# User location
user_loc = {'lat': 42.441409, 'lon': -76.484592}

st.title("Food Delivery Prediction 🍔")

# Initialize session state
if 'selected_id' not in st.session_state:
    st.session_state.selected_id = df.iloc[0]['id']

# Render map and detect clicks
def render_map():
    m = folium.Map(location=[user_loc['lat'], user_loc['lon']], zoom_start=13)
    folium.CircleMarker(
        location=[user_loc['lat'], user_loc['lon']], radius=8,
        color='blue', fill=True, fill_color='blue', tooltip='You'
    ).add_to(m)
    for _, r in df.iterrows():
        icon_color = 'red' if r['id'] == st.session_state.selected_id else 'green'
        folium.Marker(
            location=[r['lat'], r['lon']],
            tooltip=r['name'],
            popup=str(r['id']),
            icon=folium.Icon(color=icon_color, icon='cutlery', prefix='fa')
        ).add_to(m)
    return m

map_data = st_folium(render_map(), width=700, height=500)
# Click detection
if map_data and map_data.get('last_clicked'):
    lat, lon = map_data['last_clicked']['lat'], map_data['last_clicked']['lng']
    df['dist'] = ((df['lat']-lat)**2 + (df['lon']-lon)**2)
    nearest = df.loc[df['dist'].idxmin()]
    if nearest['dist'] < 0.005:
        st.session_state.selected_id = nearest['id']
        st.rerun()

# Sidebar selector
names = df['name'].tolist()
def idx():
    return names.index(df[df['id']==st.session_state.selected_id]['name'].values[0])
sel = st.sidebar.selectbox("Choose restaurant:", names, index=idx())
sel_id = df[df['name']==sel]['id'].values[0]
if sel_id != st.session_state.selected_id:
    st.session_state.selected_id = sel_id
    st.rerun()
# Show selected
selected = df[df['id']==st.session_state.selected_id].iloc[0]
st.sidebar.markdown(f"**Selected:** {selected['name']}")

# ETA Prediction UI
st.sidebar.header("ETA Prediction")
weather = st.sidebar.selectbox("Weather", ["Clear", "Rainy"])
traffic = st.sidebar.selectbox("Traffic Level", ["Low", "Medium", "High"])
time = st.sidebar.selectbox("Time of Day", ["Morning", "Afternoon", "Evening"])
vehicle = st.sidebar.selectbox("Vehicle Type", ["Car", "Bike", "Scooter"])
exp = st.sidebar.slider("Courier Experience", 0, 10, 1)
if st.sidebar.button("Predict ETA"):
    features = {
        'distance_km': selected['distance_km'],
        'Preparation_Time_min': selected['Preparation_Time_min'],
        'Weather': weather,
        'Traffic_Level': traffic,
        'Time_of_Day': time,
        'Vehicle_Type': vehicle,
        'Courier_Experience_yrs': exp
    }
    eta = predict_delivery_time(features)
    st.sidebar.success(f"ETA: {eta:.1f} min")

# Delivery Insights Chatbot
st.sidebar.header("Delivery Insights Chatbot")

# Use a form so the button stays active and we can show spinner cleanly
with st.sidebar.form(key="my_form"):
    ask = st.form_submit_button("Why is my order delayed?")
    if ask:
        # Clear any previous message
        st.session_state.pop("chat_message", None)
        # Show spinner while waiting
        with st.spinner("Analyzing delivery data…"):
            st.session_state.chat_message = chatbot_message({
                'distance_km': selected['distance_km'],
                'Preparation_Time_min': selected['Preparation_Time_min'],
                'Weather': weather,
                'Traffic_Level': traffic,
                'Time_of_Day': time,
                'Vehicle_Type': vehicle,
                'Courier_Experience_yrs': exp
            })

# Once we have a response, display it
if "chat_message" in st.session_state:
    st.sidebar.info(st.session_state.chat_message)
