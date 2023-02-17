import os
import joblib
import pandas as pd
import lightgbm as lgb
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Union, List
from fastapi.openapi.utils import get_openapi

app = FastAPI()

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="DÜRR DENTAL test CarPrice API",
        version="0.5.0",
        description="This is a very custom OpenAPI schema",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://www.duerrdental.net/fileadmin/template/img/Logo_DD_EN_RGB.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi


class PreidictionObject(BaseModel):
    price: float

class CarObjectRequest(BaseModel):
    milage: int
    make: str
    model: str
    fuel: str
    gear: str
    offerType: str
    hp: int
    year: int

@app.get("/")
def read_root():
    return {"message": "you are here for a reason, follow your heart."}

# main endpoint for car price prediction model
@app.get("/predict_price", response_model=PreidictionObject)
async def predict(request: CarObjectRequest):
    # load model
    cwd = os.getcwd()
    gbm = joblib.load(f'{cwd}/app/german_cars_pricing_model.pkl')

    # preprocess the request data to model compatible format
    mydict = dict()
    for e in request:
        mydict[e[0]] = [e[1]]
    # print(mydict)
    query_record = pd.DataFrame.from_records(mydict)

    # Casting into categorical just like we did in the training
    obj_feat = list(query_record.loc[:, query_record.dtypes == 'object'].columns.values)
    for feature in obj_feat:
        query_record[feature] = pd.Series(query_record[feature], dtype="category")

    # model making predictions
    price = gbm.predict(query_record)

    return {"price": price}