import cv2 as cv
import numpy as np
import yaml


class FrameStream:
    def __init__(self):
        video_source = None
        with open("setup.yaml") as file:
            setup_params = yaml.safe_load(file)
            video_source = setup_params["video_source"]

        self.cap = cv.VideoCapture(video_source)

        if not self.cap.isOpened():
            raise RuntimeError("Failed to open video capture")

        self.pause = False
        self.last_frame = np.array([])

    def __del__(self):
        self.cap.release()

    def next_frame(self):
        success, frame = self.cap.read()

        if not success:
            raise RuntimeError("Failed read capture")

        return frame
