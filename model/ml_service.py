import json
import os
import time
import pickle
import signal

import numpy as np
import pandas as pd
import redis
import settings
import xgboost as xgb

# Graceful Shutdown Handling
running = True
def shutdown_handler(signum, frame):
    global running
    print("Shutting down classify_process...")
    running = False

signal.signal(signal.SIGINT, shutdown_handler)

# Redis Connection
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

# Load ML Model
print("Loading ML model...")
model_path = os.path.join("resources", "xgb_model.pkl")
with open(model_path, "rb") as model_file:
    model = pickle.load(model_file)
print("Model loaded successfully!")

# Load Feature Indices
print("Loading feature indices...")
feature_indices_path = os.path.join("resources", "feature_indices.pkl")
with open(feature_indices_path, "rb") as indices_file:
    feature_indices = pickle.load(indices_file)
print("Feature indices loaded successfully!")

# Construct Feature Vector
def construct_feature_vector(params):
    ordered_features = [feature for feature, _ in sorted(feature_indices.items(), key=lambda item: item[1])]
    feature_values = [params.get(feature, 0) for feature in ordered_features]  # Default 0 for missing
    return pd.DataFrame([feature_values], columns=ordered_features)

# Predict Function
def predict(params, model):
    try:
        feature_vector = construct_feature_vector(params)
        dmatrix = xgb.DMatrix(feature_vector)
        prediction = model.predict(dmatrix)
        prediction_value = float(prediction[0])  # Ensure JSON serializability
        print(f"Prediction: {prediction_value}")
        return prediction_value
    except Exception as e:
        print(f"Error during prediction: {e}")
        return None

# Job Processing
def classify_process():
    while running:
        try:
            msg_json = db.brpop(settings.REDIS_QUEUE, timeout=10)
            if msg_json is None:
                print("No jobs found, retrying...")
                continue
            
            _, message = msg_json
            msg = json.loads(message.decode('utf-8'))
            print(f"Processing job: {msg}")

            job_id = msg.get("id", "unknown_job")
            params = {key: msg.get(key, 0) for key in feature_indices}

            prediction = predict(params, model)
            
            result = json.dumps({"prediction": prediction if prediction is not None else "Error"})
            db.set(job_id, result)
            print(f"Stored result for job {job_id}: {result}")
            
            time.sleep(settings.SERVER_SLEEP)
        except redis.exceptions.ConnectionError as e:
            print(f"Redis connection lost: {e}")
            time.sleep(5)
        except Exception as e:
            print(f"Error in classify_process loop: {e}")

if __name__ == "__main__":
    print("Launching ML service...")
    classify_process()
