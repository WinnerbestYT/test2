import asyncio
import websockets

connected = set()

async def handler(websocket):
    # Register new client
    connected.add(websocket)
    try:
        async for message in websocket:
            print(f"Received: {message}")
            # Echo back to all clients
            for conn in connected:
                if conn != websocket:
                    await conn.send(f"Echo: {message}")
    except websockets.exceptions.ConnectionClosedOK:
        print("Connection closed")
    finally:
        connected.remove(websocket)

async def main():
    async with websockets.serve(handler, "0.0.0.0", 8765):
        print("Server started on ws://0.0.0.0:8765")
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
