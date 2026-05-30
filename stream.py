from fastapi import FastAPI, Request, Response
from fastapi.responses import StreamingResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles 
import cv2
import base64

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

import os
from dotenv import load_dotenv
load_dotenv()

USERNAME = os.environ.get("NEWTON_CAM_USER")
PASSWORD = os.environ.get("NEWTON_CAM_PSWD")

def check_auth(request: Request) -> bool:
    
    auth = request.headers.get("Authorization")
    if not auth or not auth.startswith("Basic "):
        return False

    decoded = base64.b64decode(auth[6:]).decode()
    user, pw = decoded.split(":", 1)
    return user == USERNAME and pw == PASSWORD

def require_auth(request: Request):
    return Response(
       status_code=401, 
       headers={"WWW-Authenticate": 'Basic realm="Rover"'}
    )

def generate_frames(): 
    cap = cv2.VideoCapture(0)
    while True:
        success, frame = cap.read()
        if not success:
            continue
        _, buffer = cv2.imencode('.jpg', frame)

        yield(
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + 
            buffer.tobytes() +
            b'\r\n'
        )

@app.get("/stream")
def stream(request: Request):
    if not check_auth(request):
        return require_auth(request)
    return StreamingResponse(
            generate_frames(), 
            media_type="multipart/x-mixed-replace; boundary=frame"
    )

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    if not check_auth(request):
        return require_auth(request)
    with open("static/index.html") as f: 
        return f.read()
