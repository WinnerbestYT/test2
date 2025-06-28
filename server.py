import asyncio
import websockets
import json

connected = set()
lobby = []

async def handler(websocket):
    connected.add(websocket)
    try:
        async for message in websocket:
            data = json.loads(message)
            if data['action'] == 'join_lobby':
                lobby.append(websocket)
                # broadcast lobby count or players list
                info = json.dumps({"players": len(lobby)})
                await asyncio.wait([conn.send(info) for conn in lobby])
            elif data['action'] == 'start_game':
                # Matchmaking logic - e.g. group 2 players and assign room
                pass
    finally:
        connected.remove(websocket)
        if websocket in lobby:
            lobby.remove(websocket)

async def main():
    async with websockets.serve(handler, "0.0.0.0", 8765):
        await asyncio.Future()  # run forever

asyncio.run(main())
