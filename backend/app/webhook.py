import json
import logging
import os
import requests
import traceback

from fastapi import (
    FastAPI, 
    Request,
    Response,
)

from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.logger import logger as fastapi_logger

import twilio

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

gunicorn_error_logger = logging.getLogger("gunicorn.error")
gunicorn_logger = logging.getLogger("gunicorn")
uvicorn_access_logger = logging.getLogger("uvicorn.access")
uvicorn_access_logger.handlers = gunicorn_error_logger.handlers
fastapi_logger.handlers = gunicorn_error_logger.handlers

# Initialize the FastAPI app
app = FastAPI(title="webhook")


if __name__ != "__main__":
    fastapi_logger.setLevel(gunicorn_logger.level)
else:
    fastapi_logger.setLevel(logging.DEBUG)


@app.post("/listen")
async def predict(
    request: Request,
    item: dict
):
    """Prediction endpoint.
    1. This should be a post request!
    2. Make sure to post the right data.
    item: dict. Example:
        {
            "question": "hi, how are you?",
            "chat_history_ids": []
        }
    """
    
    response_payload = None

    try:
        # Parse data
        fastapi_logger.info(f"Input: {str(item)}")
        logger.info(f"Headers: {request.headers}")

        # Define UUID for the request
        request_id = uuid.uuid4().hex

        # Log input data
        fastapi_logger.info(json.dumps({
            "service_name": SERVICE_NAME,
            "type": "InputData",
            "request_id": request_id,
            "data": item,
        }))

        num_turns = 0
        if len(item["chat_history_ids"]) > 0:
            num_turns = item["chat_history_ids"][0].count(SEP_TOKEN)
        logger.info(f"Number of convo turns: {num_turns}")
        if num_turns >= MAX_TURNS:
            logger.info(f"Resetting chat history...")
            item["chat_history_ids"] = []

        # Make predictions and log
        headers = {
            "Authorization": f"Bearer {DATABRICKS_TOKEN}",
            "Content-type": "application/json"
        }

        request_payload = {"inputs": item}
        response = requests.post(url = MODEL_ENDPOINT_URL, headers = headers, data = json.dumps(request_payload))
        logger.info(f'response: {response.text}')
        json_response = json.loads(response.text)
        answer = json_response["answer"]
        chat_history_ids = json_response["chat_history_ids"]

        #If history is too long, reset it
        if len(chat_history_ids) >= MAX_LENGTH:
            logger.info(f"History is longer than MAX_LENGTH ({MAX_LENGTH}), resetting it")
            chat_history_ids = []
        model_output = {
            "answer": answer,
            "chat_history_ids": chat_history_ids
        }

        # Log output data
        fastapi_logger.info(json.dumps({
            "service_name": SERVICE_NAME,
            "type": "OutputData",
            "request_id": request_id,
            "data": model_output
        }))

        # Make response payload
        payload = jsonable_encoder(model_output)
        
    except Exception as e:
        payload = {
            "answer": "bummer, there's an error. maybe I've had too much to drink."
        }
        fastapi_logger.error(f"Error: {traceback.format_exc()}")

    response = JSONResponse(content=payload)
    return response
