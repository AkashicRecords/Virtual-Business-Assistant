from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('start_listening')
def handle_listening():
    # Your voice assistant logic here
    pass 