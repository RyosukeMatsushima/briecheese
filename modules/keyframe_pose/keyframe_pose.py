import numpy as np

from modules.pose_optimizer.optimizer import Optimizer
from modules.pose_optimizer.optimizer import Keyframe
from database.feature_points_position_db import FeaturePointsPositionDB


class KeyframePose:
    def __init__(self):
        self.max_trial = 500
        self.last_keyframe_position = np.array([1.0, 0.0, 0.0])
        self.last_keyframe_rotation = np.identity(3)

    def get_pose(self, feature_point_directions):
        optimizer = Optimizer()
        optimizer.position_bundle_constant = 0.9
        optimizer.rotation_bundle_constant = 0.9
        optimizer.position_constant = 0.5
        optimizer.rotation_constant = 0.5

        feature_point_position_directions = []
        for direction in feature_point_directions:
            try:
                _, x, y, z = FeaturePointsPositionDB().find(direction[0])
            except IndexError as err:
                print("unknown descriptor")
                print(err)
                continue

            feature_point_number = optimizer.add_feature_point(np.array([x, y, z]))
            feature_point_position_directions.append(
                [feature_point_number, direction[1]]
            )

        keyframe = Keyframe(
            self.last_keyframe_position,
            self.last_keyframe_rotation,
            np.array([]),
            np.array([]),
            feature_point_position_directions,
        )

        optimizer.add_keyframe(keyframe)

        optimizer.optimize(self.max_trial, optimize_feature_point=False)

        keyframe_position = optimizer.keyframes[0].position
        keyframe_rotation = optimizer.keyframes[0].rotation

        self.last_keyframe_position = keyframe_position
        self.last_keyframe_rotation = keyframe_rotation

        return keyframe_position, keyframe_rotation
