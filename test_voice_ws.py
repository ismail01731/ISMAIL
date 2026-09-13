import asyncio
import websockets
async def main():
    uri = "ws://127.0.0.1:8000/ws/voice"
    async with websockets.connect(uri) as ws:
        print("CONNECTED")
        await ws.send('{"type":"ping"}')
        reply = await ws.recv()
        print("SERVER_REPLY:", reply)
asyncio.run(main())
