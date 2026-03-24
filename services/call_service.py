from twilio.twiml.voice_response import VoiceResponse, Gather
from services.ai_services import ask_ai
from database import save_log, save_appointment
from datetime import datetime, timedelta
import requests

# ✅ PASTE YOUR GOOGLE SCRIPT WEB APP URL HERE
GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbxxxxxxx/exec"

# store state per call
call_states = {}

# ================= GOOGLE SHEETS =================
def save_to_google_sheets(name, date, time):
    data = {
        "name": name,
        "date": date,
        "time": time,
    }

    try:
        response = requests.post(GOOGLE_SCRIPT_URL, json=data)
        print("✅ Google Sheets Response:", response.text)
    except Exception as e:
        print("❌ Google Sheets Error:", e)

# ================= CLEAN FUNCTIONS =================
def clean_name(text):
    return text.lower().replace("my name is", "").strip().title()

def clean_time(text):
    return text.lower().replace(".", "").replace(",", "").upper()

def clean_date(text):
    text = text.lower().strip()

    today = datetime.now()

    if "today" in text:
        return today.strftime("%d %B")
    elif "tomorrow" in text:
        return (today + timedelta(days=1)).strftime("%d %B")
    else:
        return text.title()

# ================= MAIN FUNCTION =================
def handle_call(user_input, call_sid):
    response = VoiceResponse()

    if call_sid not in call_states:
        call_states[call_sid] = {"step": None}

    state = call_states[call_sid]

    # FIRST CALL
    if not user_input:
        gather = Gather(input="speech", action="/voice", timeout=5)
        gather.say("Hello! I am your AI assistant. How can I help you today?")
        response.append(gather)
        return response

    user_text = user_input.lower()

    # ================= FLOW =================
    if "appointment" in user_text and state["step"] is None:
        state["step"] = "name"
        reply = "Sure! Please tell me your name."

    elif state["step"] == "name":
        state["name"] = clean_name(user_input)
        state["step"] = "date"
        reply = "Got it. Please tell me the date for your appointment."

    elif state["step"] == "date":
        state["date"] = clean_date(user_input)
        state["step"] = "time"
        reply = "Great. What time would you prefer?"

    elif state["step"] == "time":
        state["time"] = clean_time(user_input)

        # ✅ SAVE LOCAL
        save_appointment(state["name"], state["date"], state["time"])

        # ✅ SAVE GOOGLE SHEETS
        save_to_google_sheets(
            state["name"],
            state["date"],
            state["time"]
        )

        reply = "Your appointment is booked successfully. Thank you!"
        state["step"] = None

    else:
        reply = ask_ai(user_input)

    # ================= SAVE LOG =================
    save_log(user_input, reply, datetime.now().strftime("%H:%M"))

    # ================= RESPONSE =================
    gather = Gather(input="speech", action="/voice", timeout=6)
    gather.say(reply)
    response.append(gather)

    return response