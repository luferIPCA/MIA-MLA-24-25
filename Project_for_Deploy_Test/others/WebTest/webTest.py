#MIAA-ML
#lufer
#Web test of FastAPI over a ML model
#
from flask import Flask, render_template, request
import requests  # To call FastAPI

app = Flask(__name__)

# FastAPI URL
FASTAPI_URL = "http://127.0.0.1:8000/predict"
FASTAPI_MANY_URL = "http://127.0.0.1:8000/predictMany"

#--------------------------------------------------------------------

#for testing single predictions
@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None
    if request.method == "POST":
        # Get user input from the form
        medinc = request.form["MedInc"]
        averooms = request.form["AveRooms"]
        aveoccup = request.form["AveOccup"]

        # Prepare the data to send to FastAPI
        data = {
            "MedInc": float(medinc),
            "AveRooms": float(averooms),
            "AveOccup": float(aveoccup)
        }

        # Make a POST request to FastAPI
        response = requests.post(FASTAPI_URL, json=data)

        # Get the single prediction from FastAPI
        if response.status_code == 200:
            prediction = response.json().get("predicted_house_price", "Error")
        else:
            prediction = "Error: Could not get prediction"

    return render_template("index.html", prediction=prediction)
    
#---------------------------------------------------------------
    
#for testing multiple predictions
@app.route("/predictMany", methods=["GET", "POST"])
def predict_many():
    predictions = None
    if request.method == "POST":
        # Get JSON input as text from user
        json_data = request.form["json_data"]

        try:
            # Convert input into a dictionary
            data = {"instances": eval(json_data)}  # Attention with eval!!!!

            # Call FastAPI for multiple predictions
            response = requests.post(FASTAPI_MANY_URL, json=data)

            # Extract predictions
            if response.status_code == 200:
                predictions = response.json().get("predicted_house_prices", "Error")
            else:
                predictions = "Error: Could not get predictions"
        except Exception as e:
            predictions = f"Invalid input format: {e}"

    return render_template("predictMany.html", predictions=predictions)


if __name__ == "__main__":
    app.run(debug=True, port=5001)  # Running Flask on port 5001

