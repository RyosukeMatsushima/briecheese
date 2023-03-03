import numpy as np
from scipy.spatial.transform import Rotation as scipy_R
import pathlib
import os

from tests.tools.state_logger import StateLogger


class DataManager:
    def __init__(
        self, feature_points_position, cameras_position, cameras_rotation, log_file_name
    ):
        self.feature_points_true_position = feature_points_position
        self.cameras_true_position = cameras_position
        self.cameras_true_rotation = cameras_rotation

        self.related_feature_points_position = (
            self.get_related_feature_points_position()
        )

        (
            self.feature_points_trajectory_log,
            self.keyframe_trajectory_log,
        ) = self._setup_logger(log_file_name)

    def get_keyframes_bundle(self, noise_scale):
        keyframes_bundle = []

        for fp, t, R in zip(
            self.related_feature_points_position,
            self.cameras_true_position,
            self.cameras_true_rotation,
        ):
            noise = np.random.normal(0, noise_scale, 3)
            bundle = [
                [i, (point + noise) / np.linalg.norm(point)]
                for i, point in enumerate(fp)
            ]

            keyframes_bundle += [bundle]

        return keyframes_bundle

    def noised_position(self, points, noise_scale):
        return [np.random.normal(0, noise_scale, 3) + p for p in points]

    def get_noised_feature_points_position(self, noise_scale):
        return self.noised_position(self.feature_points_true_position, noise_scale)

    def get_noised_keyframe_position(self, noise_scale):
        return self.noised_position(self.cameras_true_position, noise_scale)

    def get_noised_keyframe_rotaion(self, noise_scale):
        noise = [
            np.random.normal(0, noise_scale, 3) for p in self.cameras_true_rotation
        ]
        noise = [scipy_R.from_euler("xyz", n).as_matrix() for n in noise]
        return [
            noise[i] @ rotation for i, rotation in enumerate(self.cameras_true_rotation)
        ]

    def logging_trajectory(self, fp_data, kf_data):
        self.feature_points_trajectory_log.add_data(fp_data)
        self.keyframe_trajectory_log.add_data(kf_data)

    def finish(self):
        self.feature_points_trajectory_log.finish()
        self.keyframe_trajectory_log.finish()

    def translate_points(self, points, t, R):
        return [np.linalg.inv(R) @ (point - t) for point in points]

    def get_related_feature_points_position(self):
        return [
            self.translate_points(self.feature_points_true_position, t, R)
            for t, R in zip(self.cameras_true_position, self.cameras_true_rotation)
        ]

    def _setup_logger(self, file_name):
        current_dir = pathlib.Path(__file__).resolve().parent
        log_dir = str(current_dir) + "/log/" + file_name + "/"
        os.makedirs(log_dir, exist_ok=True)

        labels = []
        for i, fp in enumerate(self.feature_points_true_position):
            labels += ["fp_" + str(i) + axis for axis in "XYZ"]

        fp_trajectory_log = StateLogger(log_dir + "fp_trajectory.csv", tuple(labels))
        fp_true_position_log = StateLogger(
            log_dir + "fp_true_position.csv", tuple(labels)
        )

        data = []
        for fp in self.feature_points_true_position:
            data += fp.tolist()
        fp_true_position_log.add_data(data)
        fp_true_position_log.finish()

        labels = []
        for i, fp in enumerate(self.cameras_true_position):
            labels += ["kf_" + str(i) + axis for axis in "XYZ"]

        kf_trajectory_log = StateLogger(log_dir + "kf_trajectory.csv", tuple(labels))
        kf_true_position_log = StateLogger(
            log_dir + "kf_true_position.csv", tuple(labels)
        )

        data = []
        for kf in self.cameras_true_position:
            data += kf.tolist()
        kf_true_position_log.add_data(data)
        kf_true_position_log.finish()

        return fp_trajectory_log, kf_trajectory_log
