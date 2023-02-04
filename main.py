import requests
from datetime import datetime
import os

APP_KEY = os.environ.get('NT_APP_KEY')
APP_ID = os.environ.get('NT_APP_ID')

api_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"

exercise_text = input("Tell me which exercise you did?")

headers = {
    "x-app-id": APP_ID,
    "x-app-key": APP_KEY
}
parameters = {
    "query": exercise_text,
    "gender": "male",
    "weight_kg": 55,
    "height_cm": 173,
    "age": 25
}

response = requests.post(url=api_endpoint, json=parameters, headers=headers)
result = response.json()

############################ STEP 4 ############################
sheety_postapi_endpoint = os.environ.get('SHEET_ENDPOINT')

today_date = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%X")

for exercise in result["exercises"]:
    sheet_inputs = {
        "workout": {
            "date": today_date,
            "time": now_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }

    bearer_headers = {
        "Authorization": f"Bearer {os.environ.get('TOKEN')}"
    }

    sheet_response = requests.post(url=sheety_postapi_endpoint, json=sheet_inputs, headers=bearer_headers)
    print(sheet_response.text)
