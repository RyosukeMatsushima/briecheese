from modules.pose_optimizer.optimizer import Optimizer
from modules.pose_optimizer.optimizer import Keyframe
from database.feature_points_position import FeaturePointPositionsDB


class FeatuePointPositions:
    def __init__(self):

        self.max_trial = 5000
        self.optimize_feature_point = True

        self.keyframes = []

        self.available_feature_point_ids = []
        self.feature_point_positions = np.array([])
        self.pending_feature_point_ids = (
            {}
        )  # { feature_point_id: [ [ keyframe_index, direction ], ... ], ... }

        self.last_keyframe_position = None
        self.distance_from_last_keyframe_threshold = 0.2
        self.available_feature_points_count_threshold = 10

    # observed_position: vector as numpy array
    # observed_roattion: rotation matrix as numpy array
    # feature_point_directions: [ [ feature_point_id, direction[x, y, z] ], ... ]
    def add_keyframe(
        self, observed_position, observed_roattion, feature_point_directions
    ):

        # check the keyframe is far enough from last keyframe.
        if self.last_keyframe_position:
            distance = np.linalg.norm(observed_position - self.last_keyframe_position)

            if distance < self.distance_from_last_keyframe_threshold:
                return

        # select available feature points.
        available_feature_point_direcations = []
        pending_feature_point_directions = []
        for feature_points_direction in feature_points_directions:
            feature_point_id = feature_points_direction[0]
            direction = feature_points_direction[1]

            feature_point_index = get_feature_point_index(feature_point_id)

            if feature_point_index:
                available_feature_point_direcations.append(
                    [feature_point_index, direction]
                )
            else:
                pending_feature_point_directions.append([feature_point_id, direction])

        if len(
            available_feature_point_direcations
            < self.available_feature_points_count_threshold
        ):
            return

        # add pending_feature_point_directions.
        for pending_feature_point_direction in pending_feature_point_directions:
            feature_point_id = pending_feature_point_direction[0]
            direction = pending_feature_point_direction[1]
            keyframe_index = len(self.keyframes)
            self.pending_feature_point_ids[feature_point_id] = [
                keyframe_index,
                direction,
            ]

        # add keyframe.
        new_keyframe = Keyframe(
            observed_position,
            observed_rotation,
            observed_position,
            observed_rotation,
            available_feature_point_direcations,
        )
        self.keyframes.append(new_keyframe)

        # optimize after interval.
        self.keyframes_interval += 1

        if self.keyframes_interval > self.optimize_keyframes_interval:
            feature_point_positions = Optimizer().optimize_feature_point_positions(
                self.max_trial,
                True,
                self.keyframes,
                self.init_featrue_point_positions(),
            )

            db = FeaturePointsPositionDB()

            for i, feature_point_id in enumerate(self.available_feature_point_ids):
                feature_point_position = feature_point_positions[i]

                db.create(
                    feature_point_id,
                    feature_point_position[0],
                    feature_point_position[1],
                    feature_point_position[2],
                )

    def init_featrue_point_positions(self):
        return np.zeros([len(self.available_feature_point_ids), 3])

    def get_feature_point_index(self, feature_point_id):

        if feature_point_id in self.available_feature_point_ids:
            return self.available_feature_point_ids.index(feature_point_id)
        if feature_point_id in self.pending_feature_point_ids:
            return self.pop_pending_feature_point(feature_point_id)

        return None

    def pop_pending_feature_point(self, feature_point_id):

        feature_point_index = len(self.available_feature_point_ids)
        self.available_feature_point_ids.append(feature_point_id)

        keyframe_direction = self.pending_feature_point_ids.pop(feature_point_id)
        keyframe_index = keyframe_index[0]
        direction = keyframe_direction[1]

        self.keyframes[keyframe_index].direction.append(
            [feature_point_index, direction]
        )

        return feature_point_index
