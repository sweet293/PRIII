from flask import Flask, send_from_directory
import asyncio
import websockets

app = Flask(__name__)

connected_users = {}

@app.route('/')
def serve_client():
    return send_from_directory('.', 'client.html')  # Serve the HTML file

async def chat_handler(websocket, path):
    username = None
    try:
        while True:
            message = await websocket.recv()
            if message.startswith("join_room:"):
                username = message[len("join_room:"):].strip()
                connected_users[username] = websocket
                print(f"{username} has joined the chat.")
                for user, conn in connected_users.items():
                    if user != username:
                        await conn.send(f"{username} has joined the chat.")
                await websocket.send(f"Welcome {username}!")

            async for message in websocket:
                if message == "leave_room":
                    connected_users.pop(username, None)
                    for user, conn in connected_users.items():
                        await conn.send(f"{username} has left the chat.")
                    break
                elif message.startswith("send_msg:"):
                    chat_message = message[len("send_msg:"):].strip()
                    for user, conn in connected_users.items():
                        if user != username:
                            await conn.send(f"{username}: {chat_message}")
                    await websocket.send(f"{username}: {chat_message}")

    except websockets.ConnectionClosed:
        if username:
            connected_users.pop(username, None)
            print(f"{username} has disconnected.")


async def start_websocket_server():
    server = await websockets.serve(chat_handler, "localhost", 5001)
    print("Chat server started on ws://localhost:5000")
    await server.wait_closed()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_in_executor(None, app.run, "localhost", 5000)  # Run Flask on port 5000
    loop.run_until_complete(start_websocket_server())
