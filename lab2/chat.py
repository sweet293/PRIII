import json
from flask import Flask, render_template, request
from flask_socketio import SocketIO, join_room, leave_room, send, emit
from threading import Thread

# Initialize Flask app and SocketIO
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)

# Dictionary to store connected clients and their rooms
clients = {}

# HTTP route for the chat room web page
@app.route('/')
def index():
    return render_template('index.html')

# WebSocket event handlers
@socketio.on('connect')
def handle_connect():
    print('Client connected:', request.sid)

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected:', request.sid)
    if request.sid in clients:
        room = clients[request.sid]
        leave_room(room)
        del clients[request.sid]
        emit('user_left', {'user': request.sid}, room=room)

@socketio.on('join')
def handle_join(data):
    room = data['room']
    join_room(room)
    clients[request.sid] = room
    emit('user_joined', {'user': request.sid}, room=room)
    print(f'Client {request.sid} joined room {room}')

@socketio.on('message')
def handle_message(data):
    room = clients[request.sid]
    emit('message', data, room=room)
    print(f'Received message in room {room}: {data}')

if __name__ == '__main__':
    # Run the HTTP server and WebSocket handler on separate threads
    http_thread = Thread(target=app.run, kwargs={'host': '0.0.0.0', 'port': 5000})
    ws_thread = Thread(target=socketio.run, kwargs={'app': app, 'host': '0.0.0.0', 'port': 5001})

    http_thread.start()
    ws_thread.start()

    http_thread.join()
    ws_thread.join()