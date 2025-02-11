import requests
import time

url = "https://anomaly-detection-flask-api.onrender.com/predict"
test_data = [
    {"cpu_usage": 30, "cpu_temp": 60},  # Normal
    {"cpu_usage": 40, "cpu_temp": 95},  # Faulty
    {"cpu_usage": 90, "cpu_temp": 85},  # Normal
    {"cpu_usage": 50, "cpu_temp": 100}, # Faulty
]

for data in test_data:
    response = requests.post(url, json=data)
    print(f"Input: {data}, Prediction: {response.json()}")
