from src.inference.predict import predict

payload = {
    "median_income": 6.0,
    "housing_median_age": 20,
    "total_rooms": 3000,
    "population": 1200,
    "households": 500,
    "latitude": 34.2,
    "longitude": -118.4
}

print(predict(payload))
