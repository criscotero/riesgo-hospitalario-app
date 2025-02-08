import json
import os
import time
import pickle

import numpy as np
import pandas as pd
import redis
import settings
import xgboost as xgb

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

# Load the XGBoost model correctly
print("Loading ML model...")
model_path = os.path.join("resources", "xgb_model.pkl")

try:
    # Try loading as XGBoost Booster
    model = xgb.Booster()
    model.load_model(model_path)
    print("Loaded model as XGBoost Booster.")
except xgb.core.XGBoostError:
    try:
        # If Booster fails, try loading as XGBClassifier or XGBRegressor
        with open(model_path, "rb") as model_file:
            model = pickle.load(model_file)
        print("Loaded model as XGBClassifier or XGBRegressor.")
    except (pickle.UnpicklingError, AttributeError) as e:
        print(f"Error loading model: {e}")
        exit(1)

# Load the feature indices dictionary
print("Loading feature indices...")
feature_indices_path = os.path.join("resources", "feature_indices.pkl")
with open(feature_indices_path, "rb") as indices_file:
    feature_indices = pickle.load(indices_file)

# Ensure the feature indices are correctly formatted
if not isinstance(feature_indices, dict):
    print("Error: feature_indices.pkl must be a dictionary.")
    exit(1)

print("Feature indices loaded successfully!")

def construct_feature_vector(params):
    """
    Constructs a feature vector from input parameters.

    Parameters
    ----------
    params : dict
        Dictionary containing feature names and their corresponding values.

    Returns
    -------
    pd.DataFrame
        A DataFrame with one row, ordered by feature indices.
    """
    ordered_features = [feature for feature, _ in sorted(feature_indices.items(), key=lambda item: item[1])]
    feature_values = [params.get(feature, 0) for feature in ordered_features]  # Default to 0 if missing
    return pd.DataFrame([feature_values], columns=ordered_features)

def predict(params, model):
    """
    Predicts an output class based on input parameters using an XGBoost model.

    Parameters
    ----------
    params : dict
        Dictionary containing feature names and values.

    model : xgb.Booster or sklearn XGB model
        Pre-trained XGBoost model (either a Booster or an sklearn-based model).

    Returns
    -------
    float
        Model predicted value, converted to a standard Python type.
    """
    try:
        # Construct feature vector
        feature_vector = construct_feature_vector(params)

        if isinstance(model, xgb.Booster):
            # Convert DataFrame to DMatrix for Booster models
            dmatrix = xgb.DMatrix(feature_vector)
            prediction = model.predict(dmatrix)
        elif isinstance(model, (xgb.XGBClassifier, xgb.XGBRegressor)):
            # Use feature_vector directly for sklearn models
            prediction = model.predict(feature_vector)
        else:
            raise TypeError("Unsupported model type.")

        prediction_value = float(prediction[0])  # Ensure JSON serialization
        print(f"Prediction: {prediction_value}")
        return prediction_value
    except Exception as e:
        print(f"Error during prediction: {e}")
        return None

def classify_process():
    """
    Continuously retrieves and processes jobs from Redis.

    The function:
    1. Retrieves a job from the Redis queue.
    2. Extracts the job ID and required input parameters.
    3. Runs the ML model to make a prediction.
    4. Stores the result in Redis using the original job ID.

    The function runs in an infinite loop to keep processing new jobs.
    """
    while True:
        try:
            # Retrieve job from Redis (with timeout to avoid infinite blocking)
            msg_json = db.brpop(settings.REDIS_QUEUE, timeout=10)

            if msg_json is None:
                print("No jobs found, retrying...")
                continue  # Prevents crashing

            _, message = msg_json
            msg = json.loads(message.decode('utf-8'))
            print(f"Processing job: {msg}")

            # Extract job ID and input parameters
            job_id = msg.get("id", "unknown_job")
            params = {key: msg.get(key, 0) for key in feature_indices}  # Handle missing keys safely

            # Make prediction
            prediction = predict(params, model)

            # Store prediction in Redis
            result = json.dumps({"prediction": prediction if prediction is not None else "Error"})
            db.set(job_id, result)
            print(f"Stored result for job {job_id}: {result}")

            time.sleep(settings.SERVER_SLEEP)
        except Exception as e:
            print(f"Error in classify_process loop: {e}")
            time.sleep(5)  # Prevent CPU overuse in case of rapid errors

if __name__ == "__main__":
    """
    Entry point for launching the ML service.
    This initializes the Redis connection and starts processing jobs.
    """
    print("Launching ML service...")
    classify_process()
