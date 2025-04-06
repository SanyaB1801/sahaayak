import streamlit as st
import time
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import altair as alt
import random
import sqlite3
import os

# Import modules
from database import initialize_db, get_health_data, get_safety_logs, get_reminders
from database import add_reminder, mark_reminder_done, log_chat_message, get_chat_history
from database import log_alert, get_alerts, log_safety_event
from ml_utils import detect_health_anomaly, analyze_sentiment
from ollama_utils import get_llm_response

# Page configuration
st.set_page_config(
    page_title="Sahaayak - Elderly Care AI",
    page_icon="👵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize database if it doesn't exist
initialize_db()

# App title and description
st.title("Sahaayak: Elderly Care AI System")
st.markdown("A comprehensive monitoring and assistance system for elderly care")

# Sidebar navigation
st.sidebar.title("Sahaayak")
st.sidebar.image("https://placeholder.svg?height=100&width=100", width=100)

# User selection (in a real app, this would be a login system)
user_name = st.sidebar.selectbox("Select User", ["Mrs. Sharma", "Mr. Patel", "Mrs. Gupta"])

# Navigation
page = st.sidebar.radio(
    "Navigation",
    ["Health Monitoring", "Safety Monitoring", "Daily Reminders", "Social Interaction", "Emergency Alerts"]
)

# Display current time
st.sidebar.markdown(f"**Current Time:** {datetime.now().strftime('%H:%M:%S')}")
st.sidebar.markdown(f"**Current Date:** {datetime.now().strftime('%d-%m-%Y')}")

# Health Monitoring Page
if page == "Health Monitoring":
    st.header("Health Monitoring")
    
    # Get health data from database
    health_data = get_health_data(user_name)
    
    # Create columns for different metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("Heart Rate")
        latest_hr = health_data["heart_rate"].iloc[-1]
        st.metric(
            label="Current BPM", 
            value=f"{latest_hr}", 
            delta=f"{latest_hr - health_data['heart_rate'].iloc[-2]}"
        )
        
        # Heart rate chart
        hr_chart = alt.Chart(health_data).mark_line().encode(
            x='timestamp:T',
            y=alt.Y('heart_rate:Q', scale=alt.Scale(domain=[60, 100])),
            tooltip=['timestamp', 'heart_rate']
        ).properties(height=200)
        st.altair_chart(hr_chart, use_container_width=True)
    
    with col2:
        st.subheader("Blood Pressure")
        latest_systolic = health_data["systolic"].iloc[-1]
        latest_diastolic = health_data["diastolic"].iloc[-1]
        
        st.metric(
            label="Current BP", 
            value=f"{latest_systolic}/{latest_diastolic} mmHg",
            delta=f"{latest_systolic - health_data['systolic'].iloc[-2]}/{latest_diastolic - health_data['diastolic'].iloc[-2]}"
        )
        
        # Blood pressure chart
        bp_data = pd.melt(
            health_data, 
            id_vars=['timestamp'], 
            value_vars=['systolic', 'diastolic'],
            var_name='measurement', 
            value_name='value'
        )
        
        bp_chart = alt.Chart(bp_data).mark_line().encode(
            x='timestamp:T',
            y=alt.Y('value:Q', scale=alt.Scale(domain=[60, 160])),
            color='measurement:N',
            tooltip=['timestamp', 'measurement', 'value']
        ).properties(height=200)
        st.altair_chart(bp_chart, use_container_width=True)
    
    with col3:
        st.subheader("Glucose Level")
        latest_glucose = health_data["glucose"].iloc[-1]
        st.metric(
            label="Current Level", 
            value=f"{latest_glucose} mg/dL",
            delta=f"{latest_glucose - health_data['glucose'].iloc[-2]}"
        )
        
        # Glucose chart
        glucose_chart = alt.Chart(health_data).mark_line().encode(
            x='timestamp:T',
            y=alt.Y('glucose:Q', scale=alt.Scale(domain=[80, 200])),
            tooltip=['timestamp', 'glucose']
        ).properties(height=200)
        st.altair_chart(glucose_chart, use_container_width=True)
    
    # Run health check
    st.subheader("Health Analysis")
    if st.button("Run Health Check"):
        with st.spinner("Analyzing health data..."):
            time.sleep(2)  # Simulate processing time
            anomalies = detect_health_anomaly(health_data)
            
            if anomalies:
                st.error("⚠️ Potential health concerns detected:")
                for anomaly in anomalies:
                    st.markdown(f"- {anomaly}")
            else:
                st.success("✅ All vitals appear to be within normal ranges.")
    
    # Historical data section
    st.subheader("Historical Health Data")
    date_range = st.date_input(
        "Select Date Range",
        value=(datetime.now().date() - timedelta(days=7), datetime.now().date())
    )
    
    # In a real app, we would filter data based on the date range
    st.dataframe(health_data.tail(10))

# Safety Monitoring Page
elif page == "Safety Monitoring":
    st.header("Safety Monitoring")
    
    # Status indicator
    safety_logs = get_safety_logs(user_name)
    latest_status = safety_logs["status"].iloc[-1] if not safety_logs.empty else "Safe"
    
    # Display current status
    status_col1, status_col2 = st.columns([1, 3])
    with status_col1:
        if latest_status == "Safe":
            st.success("Current Status: Safe")
        elif latest_status == "Fall Detected":
            st.error("Current Status: Fall Detected")
        else:
            st.warning(f"Current Status: {latest_status}")
    
    with status_col2:
        # Simulate fall detection
        if st.button("Simulate Fall Detection"):
            with st.spinner("Detecting fall..."):
                time.sleep(1.5)
                log_safety_event(user_name, "Fall Detected", "Potential fall detected in living room")
                st.error("⚠️ Fall detected! Alert sent to caregivers.")
                st.balloons()  # Visual effect
    
    # Activity logs
    st.subheader("Recent Activity Logs")
    
    # Refresh button for logs
    if st.button("Refresh Logs"):
        st.success("Logs refreshed!")
    
    # Get updated logs
    safety_logs = get_safety_logs(user_name)
    
    # Display logs in a table
    st.dataframe(
        safety_logs,
        column_config={
            "timestamp": "Time",
            "status": "Status",
            "details": "Details",
            "location": "Location"
        },
        use_container_width=True
    )
    
    # Activity heatmap
    st.subheader("Activity Heatmap")
    
    # Create dummy data for the heatmap
    hours = list(range(24))
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    
    # Generate random activity data (0-10 scale)
    activity_data = []
    for day in days:
        for hour in hours:
            # More activity during daytime
            if 8 <= hour <= 20:
                value = random.randint(3, 10)
            else:
                value = random.randint(0, 3)
            activity_data.append({"day": day, "hour": hour, "activity": value})
    
    activity_df = pd.DataFrame(activity_data)
    
    # Create heatmap
    heatmap = alt.Chart(activity_df).mark_rect().encode(
        x=alt.X('hour:O', title='Hour of Day'),
        y=alt.Y('day:O', title='Day of Week'),
        color=alt.Color('activity:Q', scale=alt.Scale(scheme='blues')),
        tooltip=['day', 'hour', 'activity']
    ).properties(
        width=600,
        height=250,
        title='Weekly Activity Pattern'
    )
    
    st.altair_chart(heatmap, use_container_width=True)

# Daily Reminders Page
elif page == "Daily Reminders":
    st.header("Daily Reminders")
    
    # Add new reminder
    st.subheader("Add New Reminder")
    with st.form("add_reminder_form"):
        reminder_type = st.selectbox(
            "Reminder Type",
            ["Medication", "Appointment", "Exercise", "Meal", "Other"]
        )
        reminder_text = st.text_input("Reminder Details")
        reminder_date = st.date_input("Date")
        reminder_time = st.time_input("Time")
        
        # Combine date and time
        reminder_datetime = datetime.combine(reminder_date, reminder_time)
        
        # Submit button
        submitted = st.form_submit_button("Add Reminder")
        if submitted and reminder_text:
            add_reminder(user_name, reminder_type, reminder_text, reminder_datetime)
            st.success(f"Reminder added: {reminder_text}")
    
    # Display reminders
    st.subheader("Upcoming Reminders")
    reminders = get_reminders(user_name)
    
    # Filter to show only upcoming reminders
    upcoming_reminders = reminders[reminders['datetime'] > datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
    
    if not upcoming_reminders.empty:
        for i, reminder in upcoming_reminders.iterrows():
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                st.markdown(f"**{reminder['type']}**: {reminder['text']}")
                st.caption(f"Due: {reminder['datetime']}")
            
            with col2:
                if st.button("Mark Done", key=f"done_{i}"):
                    mark_reminder_done(reminder['id'])
                    st.success("Marked as done!")
                    st.rerun()
            
            with col3:
                if st.button("Delete", key=f"delete_{i}"):
                    # In a real app, we would delete the reminder
                    st.warning("Reminder deleted!")
                    st.rerun()
            
            st.divider()
    else:
        st.info("No upcoming reminders. Add some using the form above.")
    
    # Past reminders
    st.subheader("Completed Reminders")
    completed_reminders = reminders[reminders['completed'] == 1]
    
    if not completed_reminders.empty:
        st.dataframe(
            completed_reminders,
            column_config={
                "type": "Type",
                "text": "Details",
                "datetime": "Due Date",
                "completed_at": "Completed At"
            },
            use_container_width=True
        )
    else:
        st.info("No completed reminders yet.")

# Social Interaction Page
elif page == "Social Interaction":
    st.header("Social Interaction")
    
    # Chat interface
    st.subheader("Chat with Sahaayak")
    
    # Initialize chat history if not exists
    if "chat_messages" not in st.session_state:
        # Get chat history from database
        st.session_state.chat_messages = get_chat_history(user_name)
    
    # Display chat messages
    for message in st.session_state.chat_messages:
        if message["role"] == "user":
            st.chat_message("user").write(message["content"])
        else:
            st.chat_message("assistant", avatar="👵").write(message["content"])
    
    # Chat input
    user_input = st.chat_input("Type your message here...")
    
    if user_input:
        # Add user message to chat
        st.chat_message("user").write(user_input)
        st.session_state.chat_messages.append({"role": "user", "content": user_input})
        
        # Save to database
        log_chat_message(user_name, "user", user_input)
        
        # Get response from LLM
        with st.spinner("Thinking..."):
            try:
                response = get_llm_response(user_input)
                
                # Analyze sentiment
                sentiment = analyze_sentiment(user_input)
                
                # Add assistant response to chat
                st.chat_message("assistant", avatar="👵").write(response)
                st.session_state.chat_messages.append({"role": "assistant", "content": response})
                
                # Save to database
                log_chat_message(user_name, "assistant", response)
                
                # Display sentiment if detected
                if sentiment != "neutral":
                    st.info(f"I noticed you might be feeling {sentiment}. Is there anything I can help with?")
                    
            except Exception as e:
                st.error(f"Sorry, I couldn't process that. Error: {str(e)}")
                fallback_response = "I'm here to help. Could you please rephrase that?"
                st.chat_message("assistant", avatar="👵").write(fallback_response)
                st.session_state.chat_messages.append({"role": "assistant", "content": fallback_response})
                log_chat_message(user_name, "assistant", fallback_response)
    
    # Mood tracker
    st.subheader("Daily Mood Tracker")
    
    mood_col1, mood_col2 = st.columns([3, 1])
    
    with mood_col1:
        mood = st.select_slider(
            "How are you feeling today?",
            options=["Very Sad", "Sad", "Neutral", "Happy", "Very Happy"],
            value="Neutral"
        )
    
    with mood_col2:
        if st.button("Log Mood"):
            # In a real app, we would save this to the database
            st.success(f"Mood logged: {mood}")
            
            # Show different responses based on mood
            if mood in ["Very Sad", "Sad"]:
                st.info("I'm sorry to hear that. Would you like to talk about it?")
            elif mood in ["Happy", "Very Happy"]:
                st.balloons()
                st.info("That's wonderful! I'm glad you're feeling good today.")

# Emergency Alerts Page
elif page == "Emergency Alerts":
    st.header("Emergency Alerts")
    
    # Alert status
    alerts = get_alerts(user_name)
    active_alerts = alerts[alerts['active'] == 1]
    
    if not active_alerts.empty:
        st.error("⚠️ ACTIVE ALERTS")
        for _, alert in active_alerts.iterrows():
            st.warning(f"**{alert['type']}**: {alert['message']} - {alert['timestamp']}")
            
            if st.button("Resolve Alert", key=f"resolve_{alert['id']}"):
                # In a real app, we would update the alert status
                st.success("Alert resolved!")
                st.rerun()
    else:
        st.success("No active alerts at this time.")
    
    # Test alert section
    st.subheader("Send Test Alert")
    
    alert_col1, alert_col2 = st.columns(2)
    
    with alert_col1:
        alert_type = st.selectbox(
            "Alert Type",
            ["Medical Emergency", "Fall Detected", "Medication Missed", "Unusual Activity", "Other"]
        )
        alert_message = st.text_input("Alert Details", value="This is a test alert")
    
    with alert_col2:
        alert_severity = st.select_slider(
            "Severity",
            options=["Low", "Medium", "High", "Critical"],
            value="Medium"
        )
        
        recipients = st.multiselect(
            "Alert Recipients",
            ["Primary Caregiver", "Family Doctor", "Emergency Services", "Neighbor"],
            default=["Primary Caregiver"]
        )
    
    if st.button("Send Test Alert"):
        with st.spinner("Sending alert..."):
            time.sleep(1.5)
            log_alert(user_name, alert_type, alert_message, alert_severity)
            st.error(f"Test alert sent to {', '.join(recipients)}")
            st.balloons()
    
    # Alert history
    st.subheader("Alert History")
    
    # Display all alerts
    if not alerts.empty:
        st.dataframe(
            alerts,
            column_config={
                "timestamp": "Time",
                "type": "Type",
                "message": "Details",
                "severity": "Severity",
                "active": "Active"
            },
            use_container_width=True
        )
    else:
        st.info("No alert history available.")
    
    # Emergency contacts
    st.subheader("Emergency Contacts")
    
    contacts = [
        {"name": "Dr. Mehta", "role": "Family Doctor", "phone": "+91 98765 43210"},
        {"name": "Priya Sharma", "role": "Primary Caregiver", "phone": "+91 87654 32109"},
        {"name": "Emergency Services", "role": "Medical Emergency", "phone": "108"}
    ]
    
    for contact in contacts:
        st.markdown(f"**{contact['name']}** ({contact['role']}): {contact['phone']}")

# Footer
st.sidebar.markdown("---")
st.sidebar.caption("© 2025 Sahaayak AI Systems")
st.sidebar.caption("Version 1.0.0")