import numpy as np

from modules.pose_optimizer.optimizer import Optimizer
from modules.pose_optimizer.optimizer import Keyframe
from modules.feature_point_positions.one_piece import OnePiece
from database.feature_points_position_db import FeaturePointsPositionDB


class FeaturePointPositions:
    def __init__(self):
        self.onePiece = OnePiece()
        self.one_piece_length_threshold_to_optimize = 5

    # observed_position: vector as numpy array
    # observed_roattion: rotation matrix as numpy array
    # feature_point_directions: [ [ feature_point_id, direction[x, y, z] ], ... ]
    def add_keyframe(
        self, observed_position, observed_roattion, feature_point_directions
    ):
        self.onePiece.add_keyframe(
            observed_position, observed_roattion, feature_point_directions
        )

        if self.onePiece.keyframe_number < self.one_piece_length_threshold_to_optimize:
            return

        print("calculate feature point position")
        feature_point_positions = self.calculate_feature_point_positions(self.onePiece)

        db = FeaturePointsPositionDB()

        for feature_point_id in feature_point_positions:
            feature_point_position = feature_point_positions[feature_point_id]
            db.create(
                feature_point_id,
                feature_point_position[0],
                feature_point_position[1],
                feature_point_position[2],
            )
        self.onePiece = OnePiece()

    def calculate_feature_point_positions(self, one_piece):
        optimizer = Optimizer()

        keyframe_ids_and_numbers = {}

        for keyframe_id in one_piece.keyframes:
            keyframe_number = optimizer.add_keyframe(
                Keyframe(
                    np.array(one_piece.keyframes[keyframe_id].observed_position),
                    np.array(one_piece.keyframes[keyframe_id].observed_rotation),
                    np.array(one_piece.keyframes[keyframe_id].observed_position),
                    np.array(one_piece.keyframes[keyframe_id].observed_rotation),
                    [],
                )
            )
            keyframe_ids_and_numbers.update({keyframe_id: keyframe_number})

        feature_point_ids_and_numbers = {}

        for feature_point_id in one_piece.feature_point_ids:
            # reject feature point observed by only one keyframe.
            if len(one_piece.feature_point_ids[feature_point_id]) < 2:
                continue

            feature_point_number = optimizer.add_feature_point(np.zeros(3))
            feature_point_ids_and_numbers.update(
                {feature_point_number: feature_point_id}
            )

            for direction in one_piece.feature_point_ids[feature_point_id]:
                keyframe_id = direction[0]
                keyframe_number = keyframe_ids_and_numbers[keyframe_id]
                bundle = direction[1]

                optimizer.keyframes[keyframe_number].feature_points_bundle.append(
                    [feature_point_number, bundle]
                )

        optimizer.position_bundle_constant = 0.9
        optimizer.rotation_bundle_constant = 0.9
        optimizer.position_constant = 0.05
        optimizer.rotation_constant = 0.05

        optimizer.optimize(2000)

        feature_point_positions = {}  # {feature_point_id: position}
        for feature_point_number, position in enumerate(
            optimizer.feature_points_position
        ):
            feature_point_id = feature_point_ids_and_numbers[feature_point_number]
            feature_point_positions.update({feature_point_id: position})

        return feature_point_positions
