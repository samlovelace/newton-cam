import cv2
from fastapi import FastAPI, Request, Response
from fastapi.responses import StreamingResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
import os
import base64
import time

load_dotenv()

app = FastAPI()

USERNAME = os.environ.get("NEWTON_CAM_USER")
PASSWORD = os.environ.get("NEWTON_CAM_PSWD")

def find_camera() -> cv2.VideoCapture:
    for index in range(10):
        cap = cv2.VideoCapture(index)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                print(f"Camera found at index {index}")
                return cap
            cap.release()
    return None

def wait_for_camera() -> cv2.VideoCapture:
    while True:
        cap = find_camera()
        if cap is not None:
            return cap
        print("No camera found, retrying in 3 seconds...")
        time.sleep(3)

cap = wait_for_camera()

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
    global cap
    while True:
        success, frame = cap.read()
        if not success:
            print("Lost camera, attempting to reacquire...")
            cap.release()
            cap = wait_for_camera()
            continue
        _, buffer = cv2.imencode('.jpg', frame)
        yield (
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

app.mount("/static", StaticFiles(directory="static"), name="static")
