from modules.pose_optimizer.optimizer import Optimizer, Keyframe

class PointCalculation:

    def __init__(self):
        self.optimizer = Optimizer()
        self.added_point = False

        self.optimizer.position_bundle_constant = 0.9
        self.optimizer.rotation_bundle_constant = 0.9
        self.optimizer.position_constant = 0.05
        self.optimizer.rotation_constant = 0.05
        self.optimizer.keyframe_force_threshold = 0.01
        self.optimizer.keyframe_moment_threshold = 0.01

    def set_frame(self, frame_position, frame_rotation, bundle):
        keyframe = Keyframe(
            frame_position,
            frame_rotation,
            frame_position,
            frame_rotation,
            [[0, bundle]],
        )

        self.optimizer.add_keyframe(keyframe)

        if not self.added_point:
            self.optimizer.add_feature_point(frame_position + bundle * 1)
            self.added_point = True

    def get_position(self):
        try:
            self.optimizer.optimize(10000, optimize_keyframes=False)
        except RuntimeError as e:
            print(e)

        return self.optimizer.feature_points_position
