import sqlite3
import pandas as pd
from datetime import datetime, timedelta
import random
import os

# Database file path
DB_PATH = "sahaayak.db"

def initialize_db():
    """Initialize the database with required tables if they don't exist"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create health data table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS health_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_name TEXT,
        timestamp TEXT,
        heart_rate INTEGER,
        systolic INTEGER,
        diastolic INTEGER,
        glucose INTEGER,
        temperature REAL,
        oxygen_level INTEGER
    )
    ''')
    
    # Create safety logs table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS safety_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_name TEXT,
        timestamp TEXT,
        status TEXT,
        details TEXT,
        location TEXT
    )
    ''')
    
    # Create reminders table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS reminders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_name TEXT,
        type TEXT,
        text TEXT,
        datetime TEXT,
        completed INTEGER DEFAULT 0,
        completed_at TEXT
    )
    ''')
    
    # Create chat history table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS chat_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_name TEXT,
        timestamp TEXT,
        role TEXT,
        content TEXT
    )
    ''')
    
    # Create alerts table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS alerts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_name TEXT,
        timestamp TEXT,
        type TEXT,
        message TEXT,
        severity TEXT,
        active INTEGER DEFAULT 1
    )
    ''')
    
    conn.commit()
    
    # Generate sample data if tables are empty
    if cursor.execute("SELECT COUNT(*) FROM health_data").fetchone()[0] == 0:
        generate_sample_data()
    
    conn.close()

def generate_sample_data():
    """Generate sample data for demonstration purposes"""
    conn = sqlite3.connect(DB_PATH)
    
    # Sample users
    users = ["Mrs. Sharma", "Mr. Patel", "Mrs. Gupta"]
    
    # Generate health data for the past 7 days
    for user in users:
        # Base values for each user (slightly different for variety)
        base_hr = random.randint(65, 75)
        base_systolic = random.randint(115, 130)
        base_diastolic = random.randint(75, 85)
        base_glucose = random.randint(90, 110)
        
        # Generate data points for each hour in the past 7 days
        for i in range(7*24):
            timestamp = (datetime.now() - timedelta(hours=i)).strftime('%Y-%m-%d %H:%M:%S')
            
            # Add some random variation
            heart_rate = base_hr + random.randint(-5, 5)
            systolic = base_systolic + random.randint(-10, 10)
            diastolic = base_diastolic + random.randint(-5, 5)
            glucose = base_glucose + random.randint(-10, 10)
            temperature = round(36.5 + random.uniform(-0.5, 0.8), 1)
            oxygen_level = random.randint(94, 99)
            
            # Insert health data
            conn.execute('''
            INSERT INTO health_data (user_name, timestamp, heart_rate, systolic, diastolic, glucose, temperature, oxygen_level)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (user, timestamp, heart_rate, systolic, diastolic, glucose, temperature, oxygen_level))
    
    # Generate safety logs
    statuses = ["Safe", "Movement Detected", "Inactivity", "Fall Detected", "Left Home", "Returned Home"]
    locations = ["Living Room", "Bedroom", "Kitchen", "Bathroom", "Garden", "Front Door"]
    
    for user in users:
        # Generate 20 random safety logs per user
        for i in range(20):
            timestamp = (datetime.now() - timedelta(hours=random.randint(1, 168))).strftime('%Y-%m-%d %H:%M:%S')
            status = random.choice(statuses)
            
            if status == "Fall Detected":
                details = "Potential fall detected, monitoring situation"
            elif status == "Inactivity":
                details = "No movement detected for extended period"
            elif status == "Movement Detected":
                details = "Regular movement patterns observed"
            else:
                details = f"Status: {status}"
            
            location = random.choice(locations)
            
            # Insert safety log
            conn.execute('''
            INSERT INTO safety_logs (user_name, timestamp, status, details, location)
            VALUES (?, ?, ?, ?, ?)
            ''', (user, timestamp, status, details, location))
    
    # Generate reminders
    reminder_types = ["Medication", "Appointment", "Exercise", "Meal", "Other"]
    medications = ["Blood Pressure Medicine", "Diabetes Medicine", "Vitamin Supplements", "Pain Medication"]
    appointments = ["Doctor Appointment", "Physical Therapy", "Lab Test", "Eye Checkup"]
    
    for user in users:
        # Generate 10 random reminders per user
        for i in range(10):
            reminder_type = random.choice(reminder_types)
            
            if reminder_type == "Medication":
                text = random.choice(medications)
            elif reminder_type == "Appointment":
                text = random.choice(appointments)
            elif reminder_type == "Exercise":
                text = "30 minutes of walking"
            elif reminder_type == "Meal":
                text = random.choice(["Breakfast", "Lunch", "Dinner", "Evening Snack"])
            else:
                text = "Custom reminder"
            
            # Random datetime in the next 7 days
            hours_ahead = random.randint(-48, 168)  # Some in the past, some in the future
            reminder_datetime = (datetime.now() + timedelta(hours=hours_ahead)).strftime('%Y-%m-%d %H:%M:%S')
            
            # 50% chance of being completed if in the past
            completed = 1 if hours_ahead < 0 and random.random() > 0.5 else 0
            completed_at = (datetime.now() + timedelta(hours=hours_ahead, minutes=30)).strftime('%Y-%m-%d %H:%M:%S') if completed else None
            
            # Insert reminder
            conn.execute('''
            INSERT INTO reminders (user_name, type, text, datetime, completed, completed_at)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (user, reminder_type, text, reminder_datetime, completed, completed_at))
    
    # Generate chat history
    user_messages = [
        "Good morning, how are you today?",
        "What time is my doctor's appointment?",
        "I'm feeling a bit tired today",
        "Can you remind me to take my medicine?",
        "What's the weather like today?",
        "I need help with the TV remote",
        "Could you call my daughter?",
        "I'm feeling lonely today",
        "Tell me a joke to cheer me up",
        "What day is it today?"
    ]
    
    assistant_messages = [
        "Good morning! I'm doing well. How did you sleep last night?",
        "Your doctor's appointment is at 2:30 PM today with Dr. Mehta.",
        "I'm sorry to hear that. Have you taken your medication today? Would you like to rest?",
        "I'll remind you. Your next medication is due at 1:00 PM.",
        "It's sunny and 28°C outside. A beautiful day!",
        "Press the red button at the top of the remote to turn on the TV, then use the arrow buttons to navigate.",
        "Of course, I'll call your daughter Priya right away.",
        "I'm here to keep you company. Would you like to hear some music or perhaps play a game?",
        "Why don't scientists trust atoms? Because they make up everything!",
        "Today is Tuesday, June 4th, 2025."
    ]
    
    for user in users:
        # Generate 10 conversation exchanges per user
        for i in range(10):
            # User message
            user_timestamp = (datetime.now() - timedelta(minutes=random.randint(5, 1000))).strftime('%Y-%m-%d %H:%M:%S')
            user_content = user_messages[i]
            
            conn.execute('''
            INSERT INTO chat_history (user_name, timestamp, role, content)
            VALUES (?, ?, ?, ?)
            ''', (user, user_timestamp, "user", user_content))
            
            # Assistant response
            assistant_timestamp = (datetime.now() - timedelta(minutes=random.randint(4, 999))).strftime('%Y-%m-%d %H:%M:%S')
            assistant_content = assistant_messages[i]
            
            conn.execute('''
            INSERT INTO chat_history (user_name, timestamp, role, content)
            VALUES (?, ?, ?, ?)
            ''', (user, assistant_timestamp, "assistant", assistant_content))
    
    # Generate alerts
    alert_types = ["Medical Emergency", "Fall Detected", "Medication Missed", "Unusual Activity", "Other"]
    alert_messages = [
        "Potential medical emergency detected",
        "Fall detected in the bathroom",
        "Blood pressure medication missed",
        "No movement detected for 6 hours",
        "Left home at unusual hour"
    ]
    severities = ["Low", "Medium", "High", "Critical"]
    
    for user in users:
        # Generate 5 random alerts per user
        for i in range(5):
            timestamp = (datetime.now() - timedelta(hours=random.randint(1, 168))).strftime('%Y-%m-%d %H:%M:%S')
            alert_type = alert_types[i]
            message = alert_messages[i]
            severity = random.choice(severities)
            
            # 20% chance of being active
            active = 1 if random.random() < 0.2 else 0
            
            # Insert alert
            conn.execute('''
            INSERT INTO alerts (user_name, timestamp, type, message, severity, active)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (user, timestamp, alert_type, message, severity, active))
    
    conn.commit()
    conn.close()

def get_health_data(user_name):
    """Get health data for a specific user"""
    conn = sqlite3.connect(DB_PATH)
    
    # Get the last 24 hours of data
    query = '''
    SELECT timestamp, heart_rate, systolic, diastolic, glucose, temperature, oxygen_level
    FROM health_data
    WHERE user_name = ?
    ORDER BY timestamp DESC
    LIMIT 24
    '''
    
    df = pd.read_sql_query(query, conn, params=(user_name,))
    conn.close()
    
    # Convert timestamp to datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Sort by timestamp
    df = df.sort_values('timestamp')
    
    return df

def get_safety_logs(user_name):
    """Get safety logs for a specific user"""
    conn = sqlite3.connect(DB_PATH)
    
    query = '''
    SELECT timestamp, status, details, location
    FROM safety_logs
    WHERE user_name = ?
    ORDER BY timestamp DESC
    LIMIT 20
    '''
    
    df = pd.read_sql_query(query, conn, params=(user_name,))
    conn.close()
    
    return df

def log_safety_event(user_name, status, details, location="Living Room"):
    """Log a new safety event"""
    conn = sqlite3.connect(DB_PATH)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    conn.execute('''
    INSERT INTO safety_logs (user_name, timestamp, status, details, location)
    VALUES (?, ?, ?, ?, ?)
    ''', (user_name, timestamp, status, details, location))
    
    conn.commit()
    conn.close()

def get_reminders(user_name):
    """Get reminders for a specific user"""
    conn = sqlite3.connect(DB_PATH)
    
    query = '''
    SELECT id, type, text, datetime, completed, completed_at
    FROM reminders
    WHERE user_name = ?
    ORDER BY datetime ASC
    '''
    
    df = pd.read_sql_query(query, conn, params=(user_name,))
    conn.close()
    
    return df

def add_reminder(user_name, reminder_type, text, datetime_obj):
    """Add a new reminder"""
    conn = sqlite3.connect(DB_PATH)
    datetime_str = datetime_obj.strftime('%Y-%m-%d %H:%M:%S')
    
    conn.execute('''
    INSERT INTO reminders (user_name, type, text, datetime)
    VALUES (?, ?, ?, ?)
    ''', (user_name, reminder_type, text, datetime_str))
    
    conn.commit()
    conn.close()

def mark_reminder_done(reminder_id):
    """Mark a reminder as completed"""
    conn = sqlite3.connect(DB_PATH)
    completed_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    conn.execute('''
    UPDATE reminders
    SET completed = 1, completed_at = ?
    WHERE id = ?
    ''', (completed_at, reminder_id))
    
    conn.commit()
    conn.close()

def get_chat_history(user_name):
    """Get chat history for a specific user"""
    conn = sqlite3.connect(DB_PATH)
    
    query = '''
    SELECT timestamp, role, content
    FROM chat_history
    WHERE user_name = ?
    ORDER BY timestamp ASC
    '''
    
    df = pd.read_sql_query(query, conn, params=(user_name,))
    conn.close()
    
    # Convert to list of dictionaries
    chat_history = []
    for _, row in df.iterrows():
        chat_history.append({
            "role": row["role"],
            "content": row["content"]
        })
    
    return chat_history

def log_chat_message(user_name, role, content):
    """Log a new chat message"""
    conn = sqlite3.connect(DB_PATH)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    conn.execute('''
    INSERT INTO chat_history (user_name, timestamp, role, content)
    VALUES (?, ?, ?, ?)
    ''', (user_name, timestamp, role, content))
    
    conn.commit()
    conn.close()

def get_alerts(user_name):
    """Get alerts for a specific user"""
    conn = sqlite3.connect(DB_PATH)
    
    query = '''
    SELECT id, timestamp, type, message, severity, active
    FROM alerts
    WHERE user_name = ?
    ORDER BY timestamp DESC
    '''
    
    df = pd.read_sql_query(query, conn, params=(user_name,))
    conn.close()
    
    return df

def log_alert(user_name, alert_type, message, severity="Medium"):
    """Log a new alert"""
    conn = sqlite3.connect(DB_PATH)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    conn.execute('''
    INSERT INTO alerts (user_name, timestamp, type, message, severity, active)
    VALUES (?, ?, ?, ?, ?, 1)
    ''', (user_name, timestamp, alert_type, message, severity))
    
    conn.commit()
    conn.close()