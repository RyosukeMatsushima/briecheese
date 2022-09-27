import cv2 as cv


class ARMarker:
    def __init__(self, aruco_dict_type, matrix_coefficients, distortion_coefficients):
        self.aruco_dict = cv.aruco.Dictionary_get(aruco_dict_type)
        self.matrix_coefficients = matrix_coefficients
        self.distortion_coefficients = distortion_coefficients

    def detect_marker(self, frame):
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        _ = cv.aruco.DetectorParameters_create()

        corners, _, _ = cv.aruco.detectMarkers(gray, self.aruco_dict)

        # If only one marker is detected. Now reject multi makers.
        if len(corners) != 1:
            self.current_frame_pose = None
            raise ValueError(
                "Detection Error: {} markers are detecred.".format(len(corners))
            )

        rvec, tvec, markerpoints = cv.aruco.estimatePoseSingleMarkers(
            corners[0], 0.1, self.matrix_coefficients, self.distortion_coefficients
        )

        return rvec, tvec, corners
