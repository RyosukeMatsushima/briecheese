import numpy as np
from collections import namedtuple


ObservedData = namedtuple('ObservedData', 'observed_position, observed_rotation')

class OnePiece:

    def __init__(self):

        self.feature_point_ids = (
            {}
        )  # { feature_point_id: [ [ keyframe_id, direction ], ... ], ... }
        self.keyframes = (
            {}
        )  # {keyframe_id: ObservedData}

        self.keyframe_number = 0
        self.last_keyframe_position = None
        self.distance_from_last_keyframe_threshold = 0.2
        self.available_feature_points_count_threshold = 4


    # observed_position: vector as numpy array
    # observed_rotation: rotation matrix as numpy array
    # feature_point_directions: [ [ feature_point_id, direction[x, y, z] ], ... ]
    def add_keyframe(
        self, observed_position, observed_rotation, feature_point_directions
    ):

        # check the keyframe is far enough from last keyframe.
        if self.keyframe_number > 0:
            distance = np.linalg.norm(observed_position - self.last_keyframe_position)

            if distance < self.distance_from_last_keyframe_threshold:
                return

        # check the keyframe has enough available_feature_points or not.
        related_feature_point_directions = []
        new_feature_point_directions = []

        for feature_point_direction in feature_point_directions:

            if feature_point_direction[0] in self.feature_point_ids:
                related_feature_point_directions.append(feature_point_direction)
            else:
                new_feature_point_directions.append(feature_point_direction)

        if self.keyframe_number > 0 \
            and len(related_feature_point_directions) < self.available_feature_points_count_threshold:
            return

        for related_feature_point_direction in related_feature_point_directions:
            self.feature_point_ids[related_feature_point_direction[0]].append([self.keyframe_number, related_feature_point_direction[1]])

        for new_feature_point_direction in new_feature_point_directions:
            self.feature_point_ids.update({new_feature_point_direction[0]: [[self.keyframe_number, new_feature_point_direction[1]]]})

        self.keyframes.update({self.keyframe_number: ObservedData(observed_position=observed_position, observed_rotation=observed_rotation)})

        self.keyframe_number += 1
        self.last_keyframe_position = observed_position


