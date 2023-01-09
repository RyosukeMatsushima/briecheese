from flask import Flask, render_template, Response, request

from briecheese_interface import BriecheeseInterface

from random import randint
import time

app = Flask(__name__)
frame_stream = BriecheeseInterface()

@app.route("/")
def index():
    return "Hello World!"

@app.route("/stream", methods=['GET', 'POST'])
def stream():
    if request.method == 'GET':
        return render_template("stream.html")

    if request.method == 'POST':
        command_dict = {
            '0': 'pause',
            '1': 'break',
        }

        command = request.form['command']

        if command_dict[command] == 'pause':
            frame_stream.pause = True
        elif command_dict[command] == 'break':
            frame_stream.pause = False

        return render_template("stream.html")

def gen():
    while True:
        frame = frame_stream.do_next_frame()

        if frame is not None:
            yield (b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" + frame.tobytes() + b"\r\n")
        else:
            print("frame is none")
        time.sleep(0.2)

@app.route("/video_feed")
def video_feed():
    return Response(gen(),
            mimetype="multipart/x-mixed-replace; boundary=frame")

if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port=8000)
