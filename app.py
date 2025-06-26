import os
import sys
import certifi

from networksecurity.pipeline.training_pipeline import TrainingPipeline
from networksecurity.utils.ml_utils.model.estimator import NetworkModel

ca = certifi.where()

from dotenv import load_dotenv
load_dotenv()
mongo_db_url = os.getenv("MONGO_DB_URL")
print("MongoDB URL:", mongo_db_url)

import pymongo
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile , Request
from uvicorn import run as app_run
from fastapi.responses import Response
from starlette.responses import RedirectResponse
import pandas as pd

from networksecurity.utils.main_utils.utils import load_object
from networksecurity.constant.training_pipeline import DATA_INGESTION_DATABASE_NAME , DATA_INGESTION_COLLECTION_NAME

client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)
database = client[DATA_INGESTION_DATABASE_NAME]
collection = database[DATA_INGESTION_COLLECTION_NAME]
app = FastAPI()

origin = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origin,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="./templates") ## templates directory should be in the same directory as app.py
## doesnt require to have compulsory directory name as templates , but bad preactice



@app.get("/",tags=["Authentication"])
async def index():
    """
    Redirects to the documentation page.
    """
    return RedirectResponse(url="/docs")

@app.get("/train")
async def train_route():
    """
    Endpoint to trigger the training process.
    """
    try:
        train_pipeline = TrainingPipeline()
        train_pipeline.run_pipeline()
        return Response(content="Training pipeline executed successfully.")
    except Exception as e:
        raise NetworkSecurityException(e, sys)
    

@app.post("/predict", tags=["Prediction"])
async def predict_route(request: Request , file: UploadFile = File(...)):
    """
    Endpoint to render the prediction page.
    """
    try:
        df = pd.read_csv(file.file)
        ##print(df)
        preprocessor = load_object(file_path="final_model/preprocessor.pkl")
        final_model =load_object(file_path="final_model/model.pkl")
        network_model = NetworkModel(preprocessor=preprocessor, model=final_model)  # Assuming model is loaded inside NetworkModel
        print(df.iloc[0])
        y_pred = network_model.predict(df)
        print(y_pred)
        df['predicted_column'] = y_pred
        print(df['predicted_column'])
        # df["predicted_column"] = df["predicted_column"].replace({-1: 0})
        # return df.to_json()
        df.to_csv("predicted_output/output.csv") 
        table_html = df.to_html(classes="table table-striped")
        # print(table_html)
        return templates.TemplateResponse("table.html", {"request": request, "table_html": table_html})
    except Exception as e:
        raise NetworkSecurityException(e, sys)








if __name__ == "__main__":
    app_run(app,host="localhost",port=8000)