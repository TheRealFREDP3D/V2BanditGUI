# from asyncio import run  # Import specific function for asynchronous operations
# from subprocess import run as subprocess_run  # Import specific function for subprocess operations
import sys
import threading
import time

import paramiko
from fastapi import FastAPI, Request, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

from app.config import settings
from app.mentor import ask_mentor

app = FastAPI()
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(429, _rate_limit_exceeded_handler)

app.mount("/static", StaticFiles(directory="static"), name="static")


# ---------- Health ----------
@app.get("/ping/ollama")
async def ping():
    return {"status": "ok"}


# ---------- Mentor ----------
@app.post("/ask-a-pro")
@limiter.limit(settings.rate_limit)
async def ask(request: Request):
    data = await request.json()
    level = data.get("level", "bandit0")
    history = data.get("history", "")
    advice = await ask_mentor(level, history)
    return {"advice": advice}


# ---------- WebSocket PTY ----------
class SSHManager:
    def __init__(self):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.channel = None

    def connect(self):
        # amazonq-ignore-next-line
        self.client.connect(
            "bandit.labs.overthewire.org",
            username="bandit0",
            # amazonq-ignore-next-line
            password="bandit0",
            port=2220,
        )
        self.channel = self.client.invoke_shell(term="xterm", width=80, height=24)
        self.channel.settimeout(0)

    def read(self):
        if self.channel.recv_ready():
            return self.channel.recv(65535).decode(errors="ignore")
        return ""

    def write(self, data: str):
        self.channel.send(data)

    def close(self):
        self.channel.close()
        self.client.close()


@app.websocket("/pty")
# Import asyncio.run to properly handle coroutines in the event loop
# This is needed to ensure proper closure of the event loop
import asyncio

async def pty_ws(ws: WebSocket):
    await ws.accept()
    mgr = SSHManager()
    try:
        # Use asyncio.run to properly manage the event loop
        loop = asyncio.get_running_loop()
        # Wait for the first message to check for special command
        data = await ws.receive_text()
        if data == "__SHOW_TITLE__":

            # Run the title screen script and stream output
            proc = subprocess.Popen(
                [sys.executable, "app/bandit_title_screen.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                bufsize=1,
                universal_newlines=True,
            )
            for line in proc.stdout:
                await ws.send_text(line)
            proc.communicate()  # Replace proc.wait() with proc.communicate()
            # After showing the title, wait for the next message to continue
            data = await ws.receive_text()
        mgr.connect()


        # Thread to pump SSH -> WS
        def pump():
            while True:
                data = mgr.read()
                if data:
                    asyncio.run_coroutine_threadsafe(ws.send_text(data), loop)
                else:
                    # Use asyncio.sleep() instead of time.sleep()
                    asyncio.run_coroutine_threadsafe(asyncio.sleep(0.01), loop)

        threading.Thread(target=pump, daemon=True).start()
        # WS -> SSH

        while True:
            mgr.write(data)
            data = await ws.receive_text()
    except Exception:
        await ws.close()
    finally:
        mgr.close()


# ---------- Serve index ----------
@app.get("/", response_class=HTMLResponse)
async def index():
    return open("static/index.html").read()
