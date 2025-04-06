import requests
import json
import random

# Ollama API endpoint (default for local installation)
OLLAMA_API_URL = "http://localhost:11434/api/generate"

def get_llm_response(prompt):
    """
    Get a response from Ollama LLM
    If Ollama is not available, fall back to predefined responses
    """
    try:
        # Try to connect to Ollama
        payload = {
            "model": "llama2",  # or any other model you have pulled
            "prompt": f"You are Sahaayak, an AI assistant for elderly care. Be helpful, clear, and compassionate in your responses. The user says: {prompt}",
            "stream": False
        }
        
        response = requests.post(OLLAMA_API_URL, json=payload, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            return result.get("response", fallback_response(prompt))
        else:
            return fallback_response(prompt)
            
    except Exception as e:
        # If Ollama is not available, use fallback responses
        return fallback_response(prompt)

def fallback_response(prompt):
    """Provide fallback responses when Ollama is not available"""
    # Check for common queries and return appropriate responses
    prompt_lower = prompt.lower()
    
    if any(word in prompt_lower for word in ["hello", "hi", "hey", "greetings"]):
        return "Hello! How are you feeling today? Is there anything I can help you with?"
    
    elif any(word in prompt_lower for word in ["how are you", "how're you", "how do you feel"]):
        return "I'm here and ready to assist you! How are you feeling today?"
    
    elif any(word in prompt_lower for word in ["medicine", "medication", "pill", "tablet"]):
        return "Your next medication is scheduled for 2:00 PM. Would you like me to remind you when it's time?"
    
    elif any(word in prompt_lower for word in ["doctor", "appointment", "visit", "checkup"]):
        return "Your next doctor's appointment is on Friday at 10:30 AM with Dr. Mehta. Would you like me to arrange transportation?"
    
    elif any(word in prompt_lower for word in ["sad", "lonely", "alone", "unhappy"]):
        return "I'm sorry to hear you're feeling that way. Would you like me to call a family member for you? Or perhaps we could look at some photos from your album to cheer you up?"
    
    elif any(word in prompt_lower for word in ["joke", "funny", "laugh", "humor"]):
        jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "What did one wall say to the other wall? I'll meet you at the corner!",
            "Why did the scarecrow win an award? Because he was outstanding in his field!",
            "What do you call a fish with no eyes? Fsh!",
            "Why couldn't the bicycle stand up by itself? It was two tired!"
        ]
        return random.choice(jokes)
    
    elif any(word in prompt_lower for word in ["weather", "temperature", "rain", "sunny"]):
        return "Today's weather is sunny with a high of 28°C. It's a beautiful day! Would you like to sit in the garden for a while?"
    
    elif any(word in prompt_lower for word in ["food", "hungry", "meal", "eat", "lunch", "dinner", "breakfast"]):
        return "It's almost mealtime. Today's menu includes vegetable soup, rice, and fruit salad. Does that sound good to you?"
    
    elif any(word in prompt_lower for word in ["family", "children", "daughter", "son", "grandchildren"]):
        return "Your daughter Priya called this morning. She mentioned she might visit this weekend. Would you like me to call her back?"
    
    elif any(word in prompt_lower for word in ["sleep", "tired", "rest", "nap"]):
        return "If you're feeling tired, it's perfectly fine to take a rest. Would you like me to dim the lights and play some soft music?"
    
    elif any(word in prompt_lower for word in ["thank", "thanks"]):
        return "You're very welcome! I'm always here to help you."
    
    else:
        # Generic responses for other queries
        generic_responses = [
            "I'm here to help you. Could you tell me more about what you need?",
            "I want to make sure I understand correctly. Could you explain that in a different way?",
            "I'm listening. Please tell me more so I can assist you better.",
            "I'm here for you. How else can I help today?",
            "I'll do my best to help with that. Could you provide more details?"
        ]
        return random.choice(generic_responses)