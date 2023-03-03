#!/usr/bin/env python

from modules.feature_point_id.feature_point_id import FeaturePointId
from modules.feature_point_direction.feature_point_direction import (
    FeaturePointDirection,
)
from modules.feature_point_positions.feature_point_positions import (
    FeaturePointPositions,
)
from modules.keyframe_pose.keyframe_pose import KeyframePose


class Main:
    def __init__(self, fx, fy, cx, cy):
        self.featurePointId = FeaturePointId()
        self.featurePointDirection = FeaturePointDirection(fx, fy, cx, cy)
        self.featurePointPositions = FeaturePointPositions()
        self.keyframePose = KeyframePose()

    def add_frame(self, frame, observed_position, observed_rotation):
        feature_point_directions = self.get_feature_point_directions(frame, True)
        self.featurePointPositions.add_keyframe(
            observed_position, observed_rotation, feature_point_directions
        )

    def get_pose(self, frame):
        feature_point_directions = self.get_feature_point_directions(frame, False)
        position, rotation = self.keyframePose.get_pose(feature_point_directions)
        return position, rotation

    def get_feature_point_directions(self, frame, in_create_map):
        feature_point_pixels = self.featurePointId.get_with_pixel(frame, in_create_map)

        feature_point_directions = []

        for feature_point_pixel in feature_point_pixels:
            feature_point_direction = self.featurePointDirection.get(
                feature_point_pixel[0][0], feature_point_pixel[0][1]
            )

            feature_point_directions.append(
                [feature_point_pixel[1], feature_point_direction]
            )

        return feature_point_directions
