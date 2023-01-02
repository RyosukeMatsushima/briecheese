import cv2 as cv
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

    def __del__(self):
        self.cap.release()

    def create_view(self):
        success, image = self.cap.read()

        if not success:
            raise RuntimeError('Failed read capture')

        ret, frame = cv.imencode('.jpg', image)
        return frame


