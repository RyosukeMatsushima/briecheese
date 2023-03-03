import cv2 as cv


class VideoStreamer:
    def __init__(self, src):
        self.cap = cv.VideoCapture(src)
        self.paused = False

        cv.namedWindow("plane")

    def create_view(self, frame):
        vis = frame.copy()
        return vis

    def get_commands(self, key):
        if key == ord("p"):
            self.paused = not self.paused

    def run(self):
        while True:
            key = cv.waitKey(100)
            self.get_commands(key)
            if self.paused:
                continue

            ret, frame = self.cap.read()
            if not ret:
                continue

            vis = self.create_view(frame)

            cv.imshow("plane", vis)
