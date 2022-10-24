from flask import Response
from flask import Flask
from flask import render_template, request
import cv2
import numpy as np

HOST = "192.168.1.10"
PORT = 3395

app = Flask(__name__)

def combine_imgs(img1, img2):
    width = img1.shape[1] 
    spacer = np.ones((100, width, 3), dtype=np.uint8)*255
    img = cv2.vconcat((img1, spacer))
    img = cv2.vconcat((img, img2))
    return img


def setup_cap(id = 0, width=1024, height=576):
    cap = cv2.VideoCapture(id)
    #cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    return cap

def post_helper(req):
    if req.get("turnOn") == "ON":
            print("Turn on")
    elif req.get("turnOff") == "OFF":
            print("turn off")
    print(req)
    print("post")

@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        post_helper(request.form)

    return render_template("index.html")
        

def GetImage():
    cap = setup_cap()
    while True:
        ret, frame = cap.read()
        if not ret:
            print("CAMERA ERROR")
            break
        frame = combine_imgs(frame, frame)
        (flag, encodedImage) = cv2.imencode(".jpg", frame)
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodedImage) + b'\r\n')


@app.route("/stream")
def stream():
    return Response(GetImage(), mimetype = "multipart/x-mixed-replace; boundary=frame")


if(__name__ == "__main__"):
    app.run(debug = True, threaded = True, use_reloader = False, host=HOST, port=PORT)