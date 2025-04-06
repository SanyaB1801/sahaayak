import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

def detect_health_anomaly(health_data):
    """
    Simulate anomaly detection in health data
    In a real application, this would use actual ML models
    """
    anomalies = []
    
    # Get the latest readings
    latest = health_data.iloc[-1]
    
    # Check heart rate
    if latest['heart_rate'] > 90:
        anomalies.append(f"Elevated heart rate detected: {latest['heart_rate']} BPM")
    elif latest['heart_rate'] < 60:
        anomalies.append(f"Low heart rate detected: {latest['heart_rate']} BPM")
    
    # Check blood pressure
    if latest['systolic'] > 140:
        anomalies.append(f"High systolic blood pressure: {latest['systolic']} mmHg")
    elif latest['systolic'] < 90:
        anomalies.append(f"Low systolic blood pressure: {latest['systolic']} mmHg")
    
    if latest['diastolic'] > 90:
        anomalies.append(f"High diastolic blood pressure: {latest['diastolic']} mmHg")
    elif latest['diastolic'] < 60:
        anomalies.append(f"Low diastolic blood pressure: {latest['diastolic']} mmHg")
    
    # Check glucose
    if latest['glucose'] > 140:
        anomalies.append(f"Elevated glucose level: {latest['glucose']} mg/dL")
    elif latest['glucose'] < 70:
        anomalies.append(f"Low glucose level: {latest['glucose']} mg/dL")
    
    # Simulate random anomalies occasionally (for demo purposes)
    if random.random() < 0.3:  # 30% chance of a random anomaly
        possible_random_anomalies = [
            "Irregular heart rhythm pattern detected",
            "Unusual blood pressure fluctuation in the last 3 hours",
            "Potential sleep disturbance detected last night",
            "Medication effect may be wearing off earlier than expected"
        ]
        anomalies.append(random.choice(possible_random_anomalies))
    
    return anomalies

def analyze_sentiment(text):
    """
    Simple sentiment analysis function
    In a real application, this would use an actual NLP model
    """
    # List of positive and negative words for simple matching
    positive_words = [
        "happy", "good", "great", "excellent", "wonderful", "fantastic",
        "joy", "pleased", "delighted", "glad", "love", "enjoy", "nice",
        "better", "amazing", "thank", "thanks", "grateful", "appreciate"
    ]
    
    negative_words = [
        "sad", "bad", "terrible", "awful", "horrible", "poor", "unhappy",
        "disappointed", "upset", "angry", "hate", "dislike", "worry",
        "worried", "anxious", "anxiety", "fear", "scared", "lonely",
        "alone", "pain", "hurt", "sick", "ill", "tired", "exhausted"
    ]
    
    # Convert to lowercase for matching
    text_lower = text.lower()
    
    # Count matches
    positive_count = sum(1 for word in positive_words if word in text_lower)
    negative_count = sum(1 for word in negative_words if word in text_lower)
    
    # Determine sentiment
    if positive_count > negative_count:
        return "positive"
    elif negative_count > positive_count:
        return "negative"
    else:
        return "neutral"

def predict_health_trend(health_data, metric):
    """
    Simulate predicting health trends
    In a real application, this would use time series forecasting
    """
    # Get the data for the specified metric
    if metric not in health_data.columns:
        return None
    
    values = health_data[metric].values
    
    # Simple linear trend (for demonstration)
    x = np.arange(len(values))
    slope, intercept = np.polyfit(x, values, 1)
    
    # Predict next 24 hours (hourly)
    future_x = np.arange(len(values), len(values) + 24)
    predictions = slope * future_x + intercept
    
    # Create timestamps for predictions
    last_timestamp = health_data['timestamp'].iloc[-1]
    future_timestamps = [last_timestamp + timedelta(hours=i+1) for i in range(24)]
    
    # Create prediction dataframe
    prediction_df = pd.DataFrame({
        'timestamp': future_timestamps,
        f'predicted_{metric}': predictions
    })
    
    return prediction_df