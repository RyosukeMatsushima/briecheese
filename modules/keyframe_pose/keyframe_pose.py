from modules.pose_optimizer.optimizer import Optimizer
from database.feature_points_position import FeaturePointPositionsDB


class KeyframePose:
    def __init__(self):
        self.max_trial = 5
        self.optimize_feature_point = False

    def get_pose(self, feature_point_directions):
        feature_point_position_directions = []
        for direction in feature_point_directions:
            position = FeaturePointPositionDB.find(direction[0])
            feature_point_position_directions.append([position, direction[1]])

        keyframe_pose = Optimizer.optimize_keyframe_pose(
            self.max_trial,
            self.optimize_feature_point,
            feature_point_position_directions,
        )
        return keyframe_pose
