import streamlit as st
import joblib
import numpy as np
import json
import pandas as pd
import json

import numpy as np

def create_features_for_prediction(
    Information_Owner, from_station, to_station, hour, label_encoders, feature_info, 
    route_stats_df=None, default_values=None
):
    """
    Prepares a feature vector for model prediction.
    - from_station: str, e.g. 'Mr'
    - to_station: str, e.g. 'Gn'
    - hour: int, 0-23
    - label_encoders: dict, loaded from joblib
    - feature_info: dict, loaded from model_info.json
    - default_values: dict of fallback values for missing stats (optional)
    Returns: np.array of shape (1, n_features)
    """

    # Compose route string as in training
    route = f"{from_station}_{to_station}"

    # Cyclical hour encoding
    hour_sin = np.sin(2 * np.pi * hour / 24)
    hour_cos = np.cos(2 * np.pi * hour / 24)


    # Peak hour indicators
    is_rush_hour = int((7 <= hour <= 9) or (17 <= hour <= 19))
    is_night = int((hour <= 6) or (hour >= 22))

    print(label_encoders)

    # Encode route
    if 'route_encoder' in label_encoders and route in label_encoders['route_encoder'].classes_:
        route_encoded = label_encoders['route_encoder'].transform([route])[0]
    else:
        route_encoded = 0  # fallback to 0 if unseen



    # Encode route
    if 'InformationOwner_encoder' in label_encoders and Information_Owner in label_encoders['InformationOwner_encoder'].classes_:
        InformationOwner_encoded = label_encoders['InformationOwner_encoder'].transform([Information_Owner])[0]
    else:
        InformationOwner_encoded = 0  # fallback to 0 if unseen


    # Build feature vector in the correct order
    feature_names = feature_info['feature_names']
    feature_dict = {
        'Hour': hour,
        'hour_sin': hour_sin,
        'hour_cos': hour_cos,
        'is_rush_hour': is_rush_hour,
        'is_night': is_night,
        'route': route_encoded,
        'InformationOwner': InformationOwner_encoded
    }

    # Ensure order matches training
    features = np.array([[feature_dict[feat] for feat in feature_names]])
    return features



# Load your model and encoders
model = joblib.load('./streamlit/trained_model.pkl')
label_encoders = joblib.load('./streamlit/encoders.pkl')
with open('./streamlit/model_info.json', 'r') as f:
    feature_info = json.load(f)



with open('./streamlit/info_owner_options.json', 'r') as f:
    info_owner_options = json.load(f)
with open('./streamlit/from_station_options.json', 'r') as f:
    from_station_options = json.load(f)
with open('./streamlit/to_station_options.json', 'r') as f:
    to_station_options = json.load(f)

# Load station code-name mapping
with open('./streamlit/station_code_name_map.json', 'r', encoding='utf-8') as f:
    station_map = json.load(f)

# Build mapping dicts
code_to_name = {row['LocationSignature']: row['AdvertisedLocationName'] for row in station_map}
name_to_code = {row['AdvertisedLocationName']: row['LocationSignature'] for row in station_map}

from_station_names = sorted(name_to_code.keys())
to_station_names = sorted(name_to_code.keys())

st.title("Train Delay Prediction")

# User input widgets (now as dropdowns with names)
Information_Owner = st.selectbox("Information Owner", info_owner_options)
from_station_name = st.selectbox("From Station", from_station_names)
to_station_name = st.selectbox("To Station", to_station_names)
hour = st.number_input("Departure Hour (0-23)", min_value=0, max_value=23, value=8)

# Convert selected names to codes for backend
from_station = name_to_code[from_station_name]
to_station = name_to_code[to_station_name]

if st.button("Predict Delay"):
    features = create_features_for_prediction(Information_Owner, from_station, to_station, hour, label_encoders, feature_info)
    prediction = model.predict(features)[0]
    st.success(f"Predicted delay: {prediction:.1f} minutes")