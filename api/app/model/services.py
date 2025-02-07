import asyncio
import json
import time
import uuid
import redis
from aioredis import Redis
from .. import settings

# TODO
# Connect to Redis and assign to variable `db``
# Make use of settings.py module to get Redis settings like host, port, etc.
""" db = redis.Redis(
    host=settings.REDIS_IP,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB_ID)
 """

async def model_predict(image_name):
    
    print(f"Processing image {image_name}...")
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
    print(f"Processing image {image_name}...")
    prediction = None
    score = None

    # Step 1: Assign a unique ID for this job
    job_id = str(uuid.uuid4())  # Generate a unique job ID

    # Step 2: Create a dictionary with the job data
    job_data = {
        "id": job_id,
        "image_name": image_name,
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
