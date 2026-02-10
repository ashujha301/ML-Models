from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from contextlib import asynccontextmanager
import threading
from pathlib import Path

from app.consumer import start_consumer
from app.websocket_manager import manager


@asynccontextmanager
async def lifespan(app: FastAPI):
    thread = threading.Thread(target=start_consumer)
    thread.daemon = True
    thread.start()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
def home():
    html_path = Path("app/templates/index.html")
    return HTMLResponse(html_path.read_text())


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except:
        manager.disconnect(websocket)
