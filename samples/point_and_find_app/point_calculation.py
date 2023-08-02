from modules.pose_optimizer.optimizer import Optimizer, Keyframe

class PointCalculation:

    def __init__(self):
        self.optimizer = Optimizer()
        self.added_point = False

    def set_frame(self, frame_position, frame_rotation, bundle):
        print("bundle")
        print(bundle)
        keyframe = Keyframe(
            frame_position,
            frame_rotation,
            frame_position,
            frame_rotation,
            [[0, bundle]],
        )

        self.optimizer.add_keyframe(keyframe)

        if not self.added_point:
            self.optimizer.add_feature_point(frame_position + bundle * 10)
            self.added_point = True

    def get_position(self):
        self.optimizer.optimize(10000)
        return self.optimizer.feature_points_position
