#MIAA-ML
#lufer
from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import os
#for multiple instances
from typing import List
import numpy as np
import pandas as pd

# ----------------------------------------------------------------------------
# Define the input data schema using Pydantic (only onde test instance)
class InputData(BaseModel):
    """Schema for a single house price prediction request."""
    MedInc: float
    AveRooms: float
    AveOccup: float
    
# Define the input data schema for multiple predictions
class MultipleInputData(BaseModel):
    """Schema for multiple house price prediction requests."""
    instances: List[InputData]

# ----------------------------------------------------------------------------

# Initialize FastAPI app
app = FastAPI(
    title="for House Price Prediction API",
    description="API to predict house prices using a trained model! Made by FastAPI!",
    version="MIAA ML - 2024-2025 - 1.0.0",
    docs_url="/docs",   # Swagger UI
    redoc_url="/redoc"  # Make sure Redoc is enabled
    )
 
# Load the model during startup
model_path = os.path.join("model", "linearRegressionModel.pkl")
with open(model_path, 'rb') as f:
    model = pickle.load(f)
 
# ----------------------------------------------------------------------------
# Sinlge instance prediction
@app.post("/predict", summary="Predicting description", tags=["Prediction"])
def predict(data: InputData):
    """
    Predict the house price for a single instance.

    **Request Body:**
    - `MedInc` (float): Median Income in the block.
    - `AveRooms` (float): Average number of rooms per dwelling.
    - `AveOccup` (float): Average house occupancy.

    **Response:**
    - Returns a JSON object containing the predicted house price.
    """
    # Prepare the data for prediction
    input_features = [[data.MedInc, data.AveRooms, data.AveOccup]]
    
    # Make prediction using the loaded model
    prediction = model.predict(input_features)
    
    # Return the prediction result
    return {"predicted_house_price": prediction[0]}

# ----------------------------------------------------------------------------
    
# Multiple-instance prediction
@app.post("/predictMany", summary="Predict a single house price from a set of instances",tags=["Predictions"])
def predictMany(data: MultipleInputData):
    """
    Predict house prices for multiple instances.

    **Request Body:**
    - `instances`: A list of house feature objects.
      - Each object should contain:
        - `MedInc` (float): Median Income.
        - `AveRooms` (float): Average Rooms.
        - `AveOccup` (float): Average Occupancy.

    **Response:**
    - Returns a JSON object containing a list of predicted house prices.
    """
    input_features = np.array([[d.MedInc, d.AveRooms, d.AveOccup] for d in data.instances])
    predictions = model.predict(input_features).tolist()
    return {"predicted_house_prices": predictions}

# ----------------------------------------------------------------------------

# Load X_test dataset
X_test_path = os.path.join("model", "X_test.csv")  # Adjust path as needed
X_test = pd.read_csv(X_test_path)

@app.get("/predictGlobal", summary="Predict prices for all global test data", tags=["GlobalPrediction"])
def predictGlobal():
    """Predict house prices for the entire test dataset (X_test)."""
    try:
        input_features = X_test.values  # Convert DataFrame to NumPy array
        predictions = model.predict(input_features).tolist()  # Predict and convert to list
        return {"predicted_house_prices": predictions}
    except Exception as e:
        return {"Error from API": str(e)}

# ----------------------------------------------------------------------------

# Auxiliary endpoint for checking the existence of X_test.
# Not available on Swagger documentation
@app.get("/check-path", summary="Check if the X_test.csv file is available", include_in_schema=False)
def check_path():
    """Check if X_test.csv exists in the model directory."""
    if os.path.exists(X_test_path):
        return {"status": "File found!", "path": X_test_path}
    else:
        return {"status": "File NOT found!", "path": X_test_path}