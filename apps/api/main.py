import asyncio
import json
import logging
from typing import Dict, List

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Aether OS API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ProjectCreate(BaseModel):
    name: str
    description: str
    repo_url: str = None

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async library_connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_json(message)

manager = ConnectionManager()

@app.get("/")
async def root():
    return {"message": "Welcome to Aether OS API"}

@app.post("/projects")
async def create_project(project: ProjectCreate):
    logger.info(f"Creating project: {project.name}")
    # Here we would initialize the LangGraph workflow
    return {"status": "success", "project": project.name}

@app.websocket("/ws/execution/{project_id}")
async def websocket_endpoint(websocket: WebSocket, project_id: str):
    await manager.library_connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Echo back for now
            await manager.broadcast({"type": "status", "data": f"Project {project_id} received: {data}"})
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        logger.info(f"Client disconnected from project {project_id}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
