import cv2 as cv
import numpy as np
import yaml

class FrameStream():
    def __init__(self):

        video_source = None
        with open('setup.yaml') as file:
            setup_params = yaml.safe_load(file)
            video_source = setup_params['video_source']

        self.cap = cv.VideoCapture(video_source)

        if not self.cap.isOpened():
            raise RuntimeError('Failed to open video capture')

        self.pause = False
        self.last_frame = np.array([])

    def __del__(self):
        self.cap.release()

    def create_view(self):
        if self.last_frame.size != 0 and self.pause:
            return self.last_frame

        success, image = self.cap.read()

        if not success:
            raise RuntimeError('Failed read capture')

        return self.encode(image)

    def encode(self, image):
        ret, frame = cv.imencode('.jpg', image)
        self.last_frame = frame
        return frame
