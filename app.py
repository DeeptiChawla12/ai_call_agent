from flask import Flask, request, render_template
from services.call_service import handle_call
from database import init_db, get_logs, get_appointments

app = Flask(__name__)
init_db()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/logs")
def logs():
    return render_template("logs.html", logs=get_logs())

@app.route("/appointments")
def appointments():
    return render_template("appointments.html", appointments=get_appointments())

@app.route("/voice", methods=["POST"])
def voice():
    user_input = request.values.get("SpeechResult")
    call_sid = request.values.get("CallSid")

    response = handle_call(user_input, call_sid)
    return str(response)

if __name__ == "__main__":
    app.run(port=5000, debug=True)


    