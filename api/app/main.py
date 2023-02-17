# import torch
from fastapi import FastAPI
# from .utility import inference
from pydantic import BaseModel, Field
from typing import Union, List

app = FastAPI()

class DetectedObject(BaseModel):
    xmin: float
    # ymin: float
    # xmax: float
    # ymax: float
    # confidence: float
    # detected_class: int = Field(alias='class')
    # name: str

class DetectionResponse(BaseModel):
    milage: float
    fuel_type: str
    offer_type: str
    horse_power: float

@app.get("/")
def read_root():
    return {"message": "you are here for a reason, follow your heart."}

# main endpoint for object detection using yolo5 small model
@app.get("/predict_price", response_model=DetectedObject)
async def predict(image_url:str):
    # objects = inference(image_url)
    return {"xmin": 0.0}