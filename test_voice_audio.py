import asyncio
import os
import sys
import json
import base64
import subprocess
import websockets

M4A_FILE = r"D:\ISMAIL\Recording (6).m4a"

ENV = sys.argv[1].lower() if len(sys.argv) > 1 else "local"

if ENV == "prod":
    WS_URI = "wss://ismail-ai-api.onrender.com/ws/voice"
else:
    WS_URI = "ws://127.0.0.1:8000/ws/voice"

def convert_m4a_to_pcm():
    command = [
        "ffmpeg",
        "-y",
        "-i", M4A_FILE,
        "-ac", "1",
        "-ar", "16000",
        "-f", "s16le",
        "pipe:1",
    ]

    result = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    if result.returncode != 0:
        print("FFMPEG ERROR:")
        print(result.stderr.decode(errors="ignore"))
        return None

    return result.stdout


import sys

ENV = sys.argv[1].lower() if len(sys.argv) > 1 else "local"

if ENV == "prod":
    WS_URI = "wss://ismail-ai-api.onrender.com/ws/voice"
else:
    WS_URI = "ws://127.0.0.1:8000/ws/voice"


async def main():

    if ENV == "prod":
        session_url = "https://ismail-ai-api.onrender.com/api/session"
    else:
        session_url = "http://127.0.0.1:8000/api/session"
    import urllib.request
    request = urllib.request.Request(
        session_url,
        data=b"",
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        session_data = json.loads(response.read().decode("utf-8"))
    token = session_data.get("token")
    if not token:
        print("ERROR: Could not create test session")
        return
    pcm_bytes = convert_m4a_to_pcm()

    if not pcm_bytes:
        return

    audio_b64 = base64.b64encode(pcm_bytes).decode("ascii")

    print("PCM_BYTES:", len(pcm_bytes))
    print("BASE64_CHARS:", len(audio_b64))

    uri = WS_URI

    async with websockets.connect(uri) as ws:

        print("CONNECTED")

        await ws.send(json.dumps({
            "type": "auth",
            "token": token,
            "chat_id": "voice-test"
        }))

        print("AUTH_REPLY:", await ws.recv())

        await ws.send(json.dumps({
            "type": "audio_start",
            "format": "pcm16",
            "sample_rate": 16000,
            "channels": 1
        }))

        print("START_REPLY:", await ws.recv())

        await ws.send(json.dumps({
            "type": "audio",
            "format": "pcm16",
            "sample_rate": 16000,
            "channels": 1,
            "data": audio_b64
        }))

        print("AUDIO_REPLY:", await ws.recv())

        await ws.send(json.dumps({
            "type": "audio_end"
        }))

        print("COMMIT_REPLY:", await ws.recv())

        print("TRANSCRIPT_REPLY:", await ws.recv())


asyncio.run(main())







