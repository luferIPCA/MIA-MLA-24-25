#MIAA-ML
#lufer
from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import os
import numpy as np
import pandas as pd

#for multiple instances
from typing import List

# Define the input data schema using Pydantic (only onde test instance)
class InputData(BaseModel):
    MedInc: float
    AveRooms: float
    AveOccup: float

# Define the input data schema for multiple instances
class MultipleInputData(BaseModel):
    instances: List[InputData]
    
# Initialize FastAPI app
app = FastAPI(title="House Price Prediction API - MIAA Example")
 
# Load the model during startup
model_path = os.path.join("model", "linearRegressionModel.pkl")
with open(model_path, 'rb') as f:
    model = pickle.load(f)
 
@app.post("/predict")
#or
#@app.route("/predict", methods=["POST"])
def predict(data: InputData):
    # Prepare the data for prediction
    input_features = [[data.MedInc, data.AveRooms, data.AveOccup]]
    
    # Make prediction using the loaded model
    prediction = model.predict(input_features)
    
    # Return the prediction result
    return {"predicted_house_price": prediction[0]}
    
# Multiple-instance prediction
@app.post("/predictMany"(
def predictMany(data: MultipleInputData):
    input_features = np.array([[d.MedInc, d.AveRooms, d.AveOccup] for d in data.instances])
    predictions = model.predict(input_features).tolist()
    return {"predicted_house_prices": predictions}