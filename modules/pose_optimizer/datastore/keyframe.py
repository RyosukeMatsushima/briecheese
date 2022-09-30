
class Keyframe:

    def __init__(self, init_position, init_rotation, position_bundle, rotation_bundle, feature_points_bundle):

        self.position = init_position
        self.rotation = init_rotation

        # set np.array([]) (empty array) if no bundle
        self.position_bundle = position_bundle
        self.rotation_bundle = rotation_bundle

        # [id of feature_point, np.array([unit_vector to feature_point in the keyframe coordinate])]
        self.feature_points_bundle = feature_points_bundle

