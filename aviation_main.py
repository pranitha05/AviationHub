from flask import Flask, render_template, request, redirect, session, jsonify
import os
import secrets
from flask_apscheduler import APScheduler
from datetime import datetime
from dotenv import load_dotenv
import google.generativeai as genai
import warnings

app = Flask(__name__)
PORT = int(os.getenv('PORT', 3000))

# Load environment variables from .env file
load_dotenv()

# Set a secure secret key for session management
app.secret_key = secrets.token_hex(16)

# Configure Google Generative AI
warnings.filterwarnings('ignore')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

def generate_response(prompt):
    model = genai.GenerativeModel('gemini-1.0-pro-latest')
    response = model.generate_content(prompt)
    text = response.text
    return text

@app.route('/ask', methods=['POST'])
def ask():
    print("Request received at /ask endpoint")
    try:
        question = request.json.get('question')
        if not question:
            return jsonify({'error': 'No question provided'}), 400
        print(f"Question received: {question}")

        answer = generate_response(question)
        return jsonify({'answer': answer})
    except Exception as e:
        print("Error:", e)
        return jsonify({'error': 'Internal server error'}), 500

# APScheduler configuration for periodic tasks
class Config:
    SCHEDULER_API_ENABLED = True

app.config.from_object(Config())

scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

@app.route('/')
def index():
    """
    The main entry point of the application. This route is responsible for rendering the landing or homepage,
    depending on whether the user is logged in.
    """
    if 'username' not in session:
        return render_template('landingpage.html')
    else:
        username_c = session.get('username').title()  # Capitalize the username
        return render_template('homepage.html', username=username_c)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handles the user login process using Firebase Authentication.
    """
    if request.method == 'GET':
        return render_template('login.html')

    elif request.method == 'POST':
        # Redirect to Firebase Authentication for handling
        return redirect('/login')

@app.route('/logout')
def logout():
    """
    Logs the user out by clearing the session data and redirecting them to the landing page.
    """
    session.clear()
    return redirect('/landingpage')

@app.route('/landingpage')
def landingpage():
    """
    Renders the landing page for users who are not logged in.
    """
    return render_template('landingpage.html')

@app.route('/homepage')
def homepage():
    """
    Renders the homepage for logged-in users.
    """
    return render_template('homepage.html')

@app.route('/aichatbot')
def aichatbot():
    """
    Renders the AI Chatbot page.
    """
    return render_template('aichatbot.html')

@app.route('/dgcaresource')
def dgcaresource():
    """
    Renders the DGCA Resources page.
    """
    return render_template('dgcaresource.html')

@app.route('/pilotcontact')
def pilotcontact():
    """
    Renders the Pilot Contacts page.
    """
    return render_template('pilotcontact.html')

@app.route('/flyingschool')
def flyingschool():
    """
    Renders the Flying Schools page.
    """
    return render_template('flyingschool.html')

@app.route('/flightsimulator')
def flightsimulator():
    """
    Renders the Flight Simulator page.
    """
    return render_template('flightsimulator.html')

@app.route('/contact')
def contact():
    """
    Renders the Contact Us page.
    """
    return render_template('contact.html')

@app.route('/about')
def about():
    """
    Renders the About Us page.
    """
    return render_template('about.html')

@app.route('/pilotinstruction')
def pilotinstruction():
    """
    Renders the Pilot Instruction page.
    """
    return render_template('pilotinstruction.html')

@app.route('/pilot')
def pilot():
    """
    Renders the Pilot page.
    """
    return render_template('pilot.html')

if __name__ == '__main__':
    try:
        app.run(host='localhost', port=8888, debug=True, use_reloader=False)
    except Exception as e:
        print(f"Error starting the server: {e}")
