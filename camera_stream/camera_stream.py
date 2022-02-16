from picamera import PiCamera
from flask import Flask, send_file

app = Flask(__name__)

camera = None


@app.route("/grab_frame", methods=["GET"])
def grab_frame():
    camera.capture("test.jpg")
    return send_file("test.jpg")


if __name__ == "__main__":
    camera = PiCamera()
    camera.resolution = (1024, 768)
    app.run(host="0.0.0.0", port=8000, threaded=True, debug=True)
