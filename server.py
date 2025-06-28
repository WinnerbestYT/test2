# server.py
import asyncio
import socketio
from aiohttp import web

sio = socketio.AsyncServer(async_mode='aiohttp')
app = web.Application()
sio.attach(app)

waiting_players = []

@sio.event
async def connect(sid, environ):
    print(f"Client connected: {sid}")

@sio.event
async def disconnect(sid):
    print(f"Client disconnected: {sid}")
    if sid in waiting_players:
        waiting_players.remove(sid)

@sio.event
async def find_match(sid):
    print(f"Player {sid} wants to find a match")
    if waiting_players:
        # Match found: pair current sid with the first waiting player
        opponent_sid = waiting_players.pop(0)
        room = f"room_{sid}_{opponent_sid}"
        await sio.save_session(sid, {'room': room})
        await sio.save_session(opponent_sid, {'room': room})
        sio.enter_room(sid, room)
        sio.enter_room(opponent_sid, room)

        # Notify both players
        await sio.emit('match_found', {'room': room, 'players': [sid, opponent_sid]}, room=room)
        print(f"Match created: {room} between {sid} and {opponent_sid}")
    else:
        # No waiting players, add current player to queue
        waiting_players.append(sid)
        await sio.emit('waiting', {'message': 'Waiting for an opponent...'}, to=sid)

if __name__ == '__main__':
    web.run_app(app, host='0.0.0.0', port=8000)
