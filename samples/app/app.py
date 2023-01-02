from flask import Flask, render_template, Response

from frame_stream import FrameStream

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello World!"

@app.route("/stream")
def stream():
    return render_template("stream.html")

def gen(frame_stream):
    while True:
        frame = frame_stream.create_view()

        if frame is not None:
            yield (b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" + frame.tobytes() + b"\r\n")
        else:
            print("frame is none")

@app.route("/video_feed")
def video_feed():
    return Response(gen(FrameStream()),
            mimetype="multipart/x-mixed-replace; boundary=frame")

if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port=8000)
