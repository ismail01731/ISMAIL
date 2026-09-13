import asyncio
import os
import json
import websockets
async def main():
    token = os.environ.get("ISMAIL_TEST_TOKEN")
    if not token:
        print("ERROR: ISMAIL_TEST_TOKEN not set")
        return
    uri = "ws://127.0.0.1:8000/ws/voice"
    async with websockets.connect(uri) as ws:
        print("CONNECTED")
        await ws.send(json.dumps({
            "type": "auth",
            "token": token,
            "chat_id": "voice-test"
        }))
        reply = await ws.recv()
        print("SERVER_REPLY:", reply)
asyncio.run(main())
