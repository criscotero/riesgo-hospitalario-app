import json
import os
import time

import numpy as np
import redis
import settings
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications.resnet50 import decode_predictions, preprocess_input
from tensorflow.keras.preprocessing import image

# TODO
# Connect to Redis and assign to variable `db``
# Make use of settings.py module to get Redis settings like host, port, etc.
db = redis.Redis(
    host=settings.REDIS_IP,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB_ID)

try:
    db.ping()  # Send a simple PING command to check connection
    print("Connected to Redis!")
except redis.ConnectionError as e:
    print(f"Failed to connect to Redis: {e}")
# TODO
# Load your ML model and assign to variable `model`
# See https://drive.google.com/file/d/1ADuBSE4z2ZVIdn66YDSwxKv-58U7WEOn/view?usp=sharing
# for more information about how to use this model.
model = ResNet50(include_top=True, weights="imagenet")


def predict(image_name):
    """
    Load image from the corresponding folder based on the image name
    received, then, run our ML model to get predictions.

    Parameters
    ----------
    image_name : str
        Image filename.

    Returns
    -------
    class_name, pred_probability : tuple(str, float)
        Model predicted class as a string and the corresponding confidence
        score as a number.
    """
    class_name = None
    pred_probability = None
    # TODO: Implement the code to predict the class of the image_name

    # Load image

    # Apply preprocessing (convert to numpy array, match model input dimensions (including batch) and use the resnet50 preprocessing)

    # Get predictions using model methods and decode predictions using resnet50 decode_predictions

    try:
        
        # Load image
        img_path = os.path.join(settings.UPLOAD_FOLDER, image_name)
        print(f"Loading image from {img_path}")
        img = image.load_img(img_path, target_size=(224, 224))
        print(f"Image loaded successfully from {img}")

        # Apply preprocessing
        img_array = image.img_to_array(img)  # Convert image to numpy array
        img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
        img_array = preprocess_input(img_array)  # Preprocess for ResNet50
        print("Image preprocessed successfully.")
        
        # Get predictions
        predictions = model.predict(img_array)  # `model` is assumed to be loaded globally
        decoded_predictions = decode_predictions(predictions, top=1)  # Get top 1 prediction
        print(f"Predictions: {decoded_predictions}")


        # Extract class name and probability
        _, class_name, pred_probability = decoded_predictions[0][0]  # Top prediction
        pred_probability = round(float(pred_probability), 4)  # Convert to float and round
        print(f"Predicted class: {class_name}, Probability: {pred_probability}")
    except Exception as e:
        print(f"Error during prediction: {e}")

    return class_name, pred_probability


def classify_process():
    """
    Loop indefinitely asking Redis for new jobs.
    When a new job arrives, takes it from the Redis queue, uses the loaded ML
    model to get predictions and stores the results back in Redis using
    the original job ID so other services can see it was processed and access
    the results.

    Load image from the corresponding folder based on the image name
    received, then, run our ML model to get predictions.
    """
    while True:
        # Inside this loop you should add the code to:
        #   1. Take a new job from Redis
        #   2. Run your ML model on the given data
        #   3. Store model prediction in a dict with the following shape:
        #      {
        #         "prediction": str,
        #         "score": float,
        #      }
        #   4. Store the results on Redis using the original job ID as the key
        #      so the API can match the results it gets to the original job
        #      sent
        # Hint: You should be able to successfully implement the communication
        #       code with Redis making use of functions `brpop()` and `set()`.
        # TODO
        # Take a new job from Redis
        try:
           
         db.ping()  
                    
         msg_json = db.brpop(settings.REDIS_QUEUE)

        # Decode the JSON data for the given job

         print(f"Retrieved message12: {msg_json}, type: {type(msg_json)}")
         channel, message = msg_json  # Unpack the tuple
        # msg = json.loads(message.decode('utf-8'))

         msg = json.loads(message.decode('utf-8'))

         print(f"Retrieved message12: { msg}, type: {type(msg)}")
        
        # Call the predict function, passing in the image name
         class_name, pred_probability = predict(msg["image_name"])
        
         print(f"Predicted class: {class_name}, score: {pred_probability}") 
        # Store model prediction in a dict
         prediction_dict = {
                "prediction": class_name,
                "score": pred_probability,  # Store as a float
            }
    
        # Serialize the result into a JSON string
         prediction_json = json.dumps(prediction_dict)

        # 6. Get the original job ID from the message
         msg_id = msg["id"]

        # 7. Store the results on Redis using the original job ID as the key
         db.set(msg_id, prediction_json)

        # Sleep for a bit
         time.sleep(settings.SERVER_SLEEP)
        
        except Exception as e:
         print(f"Error in classify_process loop: {e}")

if __name__ == "__main__":
    # Now launch process
    print("Launching ML service...")
    classify_process()
