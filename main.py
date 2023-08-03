import numpy as np
import pandas as pd
from fastapi import FastAPI, Request, WebSocket
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import json
import asyncio

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Global variables to store the chart data
x_data = []
y_data = []

def read_json_data(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            x_data.extend(data.get('x', []))
            y_data.extend(data.get('y', []))
    except Exception as e:
        print("Error reading JSON file:", e)

@app.websocket("/ws/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    while True:
        # Prepare the chart data
        chart_data = {
            'x': x_data,
            'y': y_data
        }

        await websocket.send_text(json.dumps(chart_data))
        await asyncio.sleep(2)

@app.on_event("startup")
async def startup_event():
    # Read JSON data from the file (modify the file path as needed)
    read_json_data("data.json")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
