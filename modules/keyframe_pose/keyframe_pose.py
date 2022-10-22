from modules.pose_optimizer.optimizer import Optimizer

class KeyframePose:




    # keyframeの位置を知るために必要なこと
    # - 位置が既知のfeature points
    # - それらを含むbundles

    def __init__(self):
        self.max_trial = 5
        self.optimize_feature_point = False

    # bundles: [ [ feature_point_id, direction ], ... ]
    def get_pose(self, feature_point_directions):
        feature_point_direction_positions = []
        for direction in feature_point_directions:
            position = FeaturePointPositionDB.find(direction[0])
            feature_point_direction_positions.append([position, direction[1]])
        # feature_point_direction_positions: [[position, direction],[position, direction]]

        keyframe_pose = Optimizer.optimize_keyframe_pose(self.max_trial, self.optimize_feature_point, feature_point_direction_positions)
        return keyframe_pose


        # optimizer に位置が既知のfeature points をセット
        # optimizer にfeature point directions をセット
        # optimiser.optimise(self.print_a)

        # db [feature_point_id, position]

        # 







