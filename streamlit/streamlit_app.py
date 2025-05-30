import streamlit as st
import joblib
import numpy as np


import numpy as np

def create_features_for_prediction(
    from_station, to_station, hour, label_encoders, feature_info,
    route_stats_df=None, default_values=None
):
    """
    Prepares a feature vector for model prediction.
    - from_station: str, e.g. 'Mr'
    - to_station: str, e.g. 'Gn'
    - hour: int, 0-23
    - label_encoders: dict, loaded from joblib
    - feature_info: dict, loaded from model_info.json
    - route_stats_df: DataFrame with route stats (optional, for avg/std/count/distance)
    - default_values: dict of fallback values for missing stats (optional)
    Returns: np.array of shape (1, n_features)
    """

    # Compose route string as in training
    route = f"{from_station}_{to_station}"

    # Cyclical hour encoding
    hour_sin = np.sin(2 * np.pi * hour / 24)
    hour_cos = np.cos(2 * np.pi * hour / 24)

    # Default/fallbacks
    if default_values is None:
        default_values = {
            'route_distance': 0,
            'route_avg_delay': 0,
            'route_std_delay': 0,
            'route_count': 1
        }

    # Try to get route stats from a DataFrame (if available)
    if route_stats_df is not None and route in route_stats_df.index:
        stats = route_stats_df.loc[route]
        route_distance = stats.get('route_distance', default_values['route_distance'])
        route_avg_delay = stats.get('route_avg_delay', default_values['route_avg_delay'])
        route_std_delay = stats.get('route_std_delay', default_values['route_std_delay'])
        route_count = stats.get('route_count', default_values['route_count'])
    else:
        # Use defaults if not found
        route_distance = default_values['route_distance']
        route_avg_delay = default_values['route_avg_delay']
        route_std_delay = default_values['route_std_delay']
        route_count = default_values['route_count']

    # Peak hour indicators
    is_rush_hour = int((7 <= hour <= 9) or (17 <= hour <= 19))
    is_night = int((hour <= 6) or (hour >= 22))

    # Encode route
    if 'route_encoder' in label_encoders and route in label_encoders['route_encoder'].classes_:
        route_encoded = label_encoders['route_encoder'].transform([route])[0]
    else:
        route_encoded = 0  # fallback to 0 if unseen

    # Build feature vector in the correct order
    feature_names = feature_info['feature_names']
    feature_dict = {
        'hour': hour,
        'hour_sin': hour_sin,
        'hour_cos': hour_cos,
        'route_distance': route_distance,
        'route_avg_delay': route_avg_delay,
        'route_std_delay': route_std_delay,
        'route_count': route_count,
        'is_rush_hour': is_rush_hour,
        'is_night': is_night,
        'route': route_encoded
    }

    # Ensure order matches training
    features = np.array([[feature_dict[feat] for feat in feature_names]])
    return features


# Load your model and encoders
model = joblib.load('trained_model.pkl')
label_encoders = joblib.load('encoders.pkl')
feature_info = joblib.load('model_info.json')

st.title("Train Delay Prediction")

# User input widgets
from_station = st.text_input("From Station Code (e.g. 'Mr')", "")
to_station = st.text_input("To Station Code (e.g. 'Gn')", "")
hour = st.number_input("Hour of Day (0-23)", min_value=0, max_value=23, value=8)

if st.button("Predict Delay"):
    # Prepare features (you may need to adjust this to match your model)
    # Example assumes you have a function to create the feature vector
    features = create_features_for_prediction(from_station, to_station, hour, label_encoders, feature_info)
    prediction = model.predict(features)[0]
    st.success(f"Predicted delay: {prediction:.1f} minutes")