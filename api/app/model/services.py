import asyncio
import json
import time
import uuid
import redis
from aioredis import Redis
from .. import settings
from app.model.schema import PredictRequest, PredictResponse
# TODO
# Connect to Redis and assign to variable `db``
# Make use of settings.py module to get Redis settings like host, port, etc.
""" db = redis.Redis(
    host=settings.REDIS_IP,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB_ID)
 """

async def model_predict(predict_request: PredictRequest):
    
    print(f"Processing {predict_request}...")
    """
    Receives an image name and queues the job into Redis.
    Will loop until getting the answer from our ML service.

    Parameters
    ----------
    image_name : str
        Name for the image uploaded by the user.

    Returns
    -------
    prediction, score : tuple(str, float)
        Model predicted class as a string and the corresponding confidence
        score as a number.
    """
   
    prediction = None
    score = None

    # Step 1: Assign a unique ID for this job
    job_id = str(uuid.uuid4())  # Generate a unique job ID

    # Step 2: Create a dictionary with the job data
     # Step 2: Create a dictionary with the job data, including the image name and prediction request
    job_data = {
        "id": job_id,
        "r5fallnum": predict_request.r5fallnum,
        "r5uppermob": predict_request.r5uppermob,
        "r5grossa": predict_request.r5grossa,
        "r5lowermob": predict_request.r5lowermob,
        "r5mobilsev": predict_request.r5mobilsev,
        "r5adltot6": predict_request.r5adltot6,
        "r5nagi8": predict_request.r5nagi8, 
        "r5iadlfour": predict_request.r5iadlfour,
        "r5height": predict_request.r5height,
        "r5adla": predict_request.r5adla,
        "r5agey": predict_request.age,
        "r5weight": predict_request.r5weight,
        "r5bmi": predict_request.r5bmi,  # Automatically calculated BMI from PredictRequest
    }





    # Initialize aioredis connection
    redis = Redis(
        host=settings.REDIS_IP,
        port=settings.REDIS_PORT,
        db=settings.REDIS_DB_ID,
        decode_responses=True,  # Automatically decode strings
    )

    try:

        if await redis.ping():
            print("Successfully connected to Redis1!")

        # Step 3: Send the job to the model service using Redis
        await redis.lpush(settings.REDIS_QUEUE, json.dumps(job_data))  # Add job to Redis queue
        print(f"Job {job_data['id']} pushed to Redis queue.")
       
            # Step 4: Poll Redis for the result
        while True:
            # Attempt to get model predictions using job_id
            output = await redis.get(job_id)  # Check if the result is 
            
            # Print the output for debugging
            print(f"Output from Redis for job_id {job_id}: {output}")

            if output is not None:
                # Decode and process the result
                output = json.loads(output)
                prediction = output["prediction"]
                score = output["score"]

                # Clean up the job from Redis
                await redis.delete(job_id)
                break

            # Sleep for a short period before checking again
            await asyncio.sleep(settings.API_SLEEP)
        
    except Exception as e:
        print(f"Error during prediction: {e}")
    finally:
        # Ensure Redis connection is properly closed
        await redis.close()

    return prediction, score
