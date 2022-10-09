import numpy as np

class KeyframesStore:

    def __init__(self):
        self.keyframes = {}
        self.last_observed_position = None
        self.last_observed_rotation = None
        self.observed_position_count = 0
        self.observed_rotation_count = 0

    def add(self, keyframe_id, bundles, observed_position, observed_rotation):

        # create new keyframe.
        # about position
        new_keyframe_position = np.array([])
        if observed_position.size != 0:
            self.observed_position_count += 1

            if not self.last_observed_position:
                [ self.keyframes[keyframe_id].position = observed_position
                        for keyframe_id in self.keyframes ]

            self.last_observed_position = observed_position

        elif self.observed_positions_count >= 1 and self.last_observed_position:
            new_keyframe_position = self.last_observed_position


        # about rotation
        new_keyframe_rotation = np.array([])
        if observed_rotation.size != 0:
            self.observed_rotation_count += 1

            if not self.last_observed_rotation:
                [ self.keykeyframes[keyframe_id].rotation = observed_rotation
                        for keyframe_id in self.keyframes ]

            self.last_observed_rotation = observed_rotation

        elif self.observed_rotations_count >= 1 and self.last_observed_rotation:
            new_keyframe_rotation = self.last_observed_rotation

        new_keyframe = Keyframe(observed_position,
                                observed_rotation,
                                observed_position,
                                observed_rotation,
                                bundles)

        self.keyframes.update({keyframe_id, new_keyframe})

        return new_keyframe


