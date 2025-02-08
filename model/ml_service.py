import json
import os
import time
import pickle

import numpy as np
import pandas as pd
import redis
import settings

# Connect to Redis
print("Connecting to Redis...")
db = redis.Redis(
    host=settings.REDIS_IP,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB_ID
)

try:
    db.ping()
    print("Connected to Redis!")
except redis.ConnectionError as e:
    print(f"Failed to connect to Redis: {e}")
    exit(1)

# Load the XGBoost model
print("Loading ML model...")
model_path = os.path.join("resources", "xgb_model.pkl")
with open(model_path, "rb") as model_file:
    model = pickle.load(model_file)
print("Model loaded successfully!")

# Load the feature indices dictionary
print("Loading feature indices...")
feature_indices_path = os.path.join("resources", "feature_indices.pkl")
with open(feature_indices_path, "rb") as indices_file:
    feature_indices = pickle.load(indices_file)
print("Feature indices loaded successfully!")

def construct_feature_vector(params):
    """
    Construct a feature vector based on the provided parameters
    and the predefined feature indices.

    Parameters
    ----------
    params : dict
        Dictionary containing feature names and values.

    Returns
    -------
    pd.DataFrame
        DataFrame with one row, ordered by feature indices.
    """
    ordered_features = [feature for feature, _ in sorted(feature_indices.items(), key=lambda item: item[1])]
    feature_values = [params.get(feature, 0) for feature in ordered_features]  # Default to 0 if missing
    
    return pd.DataFrame([feature_values], columns=ordered_features)

def predict(params):
    """
    Predict the class using the XGBoost model based on the input parameters.

    Parameters
    ----------
    params : dict
        Dictionary containing input parameters.

    Returns
    -------
    prediction : float
        Model predicted value.
    """
    try:
        feature_vector = construct_feature_vector(params)
        prediction = model.predict(feature_vector) # Get the prediction
        print(f"Prediction: {prediction}")
        return prediction
    except Exception as e:
        print(f"Error during prediction: {e}")
        return None

def classify_process():
    """
    Process jobs from Redis queue, make predictions, and store results.
    """
    while True:
        try:
            # Fetch a job from Redis
            msg_json = db.brpop(settings.REDIS_QUEUE)
            _, message = msg_json
            msg = json.loads(message.decode('utf-8'))
            print(f"Processing job: {msg}")
            
            # Extract job ID and parameters
            job_id = msg["id"]
            params = msg["params"]
            
            # Make prediction
            prediction = predict(params)
            
            # Store results in Redis
            result = json.dumps({"prediction": prediction})
            db.set(job_id, result)
            print(f"Stored result for job {job_id}: {result}")
            
            time.sleep(settings.SERVER_SLEEP)
        except Exception as e:
            print(f"Error in classify_process loop: {e}")

if __name__ == "__main__":
    print("Launching ML service...")
    classify_process()
