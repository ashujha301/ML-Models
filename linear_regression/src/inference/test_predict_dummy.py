from src.inference.predict import predict

payload = {
    "Impressions": 5000,
    "Engagement_Score": 120,
    "Duration": "65 days",
    "Channel_Used": "Google_ads",
    "Campaign_Type": "Email"
}

print(predict(payload))
