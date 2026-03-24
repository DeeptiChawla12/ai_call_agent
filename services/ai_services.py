import requests
from config import API_KEY

def ask_ai(user_text):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={API_KEY}"

    data = {
        "contents": [{
            "parts": [{
                "text": f"You are an assistant for booking appointments. Keep replies short. User: {user_text}"
            }]
        }]
    }

    res = requests.post(url, json=data)
    result = res.json()

    try:
        return result['candidates'][0]['content']['parts'][0]['text']
    except:
        return "Sorry, I didn't understand."