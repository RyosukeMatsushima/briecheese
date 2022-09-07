import numpy as np
import cv2 as cv


class Optimizer:

    def __init__(self):

        self.feature_points_position = np.array([])
        self.keyframes = []
        self.last_id = 0

        self.position_bundle_constant = 0.5
        self.rotation_bundle_constant = 0.5
        self.position_constant = 0.5
        self.rotation_constant = 0.01

        self.feature_points_force_threshold = 0.000001
        self.keyframe_force_threshold = 0.01
        self.keyframe_moment_threshold = 0.001


    def add_keyframe(self, keyframe):
        self.keyframes += [keyframe]


    def add_feature_point(self, init_position):

        if self.feature_points_position.any():
            self.feature_points_position = np.append(self.feature_points_position, [init_position], axis=0)
        else:
            self.feature_points_position = np.array([init_position])

        current_id = self.last_id
        self.last_id += 1
        return current_id


    #TODO: return or callbackoptimize result
    def optimize(self, max_trial, callback):

        is_enough = False

        trial = 0

        while not is_enough:
            feature_points_force = np.zeros(np.shape(self.feature_points_position))
            is_keyframes_enough = True
            for keyframe in self.keyframes:
                output1, output2 = self.calculate(keyframe)
                feature_points_force += output1
                is_keyframes_enough = is_keyframes_enough and output2

            self.feature_points_position += feature_points_force

            evaluate_value = np.linalg.norm(np.sum(feature_points_force, axis=0)) / np.shape(self.feature_points_position)[0]
            is_enough = evaluate_value < self.feature_points_force_threshold

            callback(trial, evaluate_value)

            if trial >= max_trial:
                break
            trial += 1


    def calculate(self, keyframe):

        keyframe_force = np.zeros(3)
        keyframe_moment = np.zeros(3)
        feature_points_force = np.zeros(np.shape(self.feature_points_position))
        keyframe_force_constant = self.position_constant / len(keyframe.feature_points_bundle)

        for feature_point_bundle in keyframe.feature_points_bundle:

            feature_point_id = feature_point_bundle[0]
            current_feature_point_position = self.feature_points_position[feature_point_id]

            vector_to_feature_point = current_feature_point_position - keyframe.position
            vector_size = np.linalg.norm(vector_to_feature_point)
            vector_to_feature_point /= vector_size

            feature_point_bundle = keyframe.rotation @ feature_point_bundle[1]

            moment = np.cross(vector_to_feature_point, feature_point_bundle)
            force = np.cross(moment, feature_point_bundle) * vector_size

            keyframe_force += force * keyframe_force_constant
            keyframe_moment -= moment * self.rotation_constant
            feature_points_force[feature_point_id] += force * self.position_constant


        if keyframe.position_bundle.size != 0:
            keyframe_force -= ( keyframe.position - keyframe.position_bundle ) * self.position_bundle_constant

        if keyframe.rotation_bundle.size != 0:
            keyframe_moment -= cv.Rodrigues( keyframe.rotation @ np.linalg.inv(keyframe.rotation_bundle) )[0].T[0] * self.rotation_bundle_constant

        keyframe.position += keyframe_force
        keyframe.rotation = cv.Rodrigues(keyframe_moment)[0] @ keyframe.rotation

        is_keyframe_enough = np.linalg.norm(keyframe_force) < self.keyframe_force_threshold \
                         and np.linalg.norm(keyframe_moment) < self.keyframe_moment_threshold
        return feature_points_force, is_keyframe_enough


class Keyframe:

    def __init__(self, init_position, init_rotation, position_bundle, rotation_bundle, feature_points_bundle):

        self.position = init_position
        self.rotation = init_rotation

        # set np.array([]) (empty array) if no bundle
        self.position_bundle = position_bundle
        self.rotation_bundle = rotation_bundle

        # [id of feature_point, np.array([unit_vector to feature_point in the keyframe coordinate])]
        self.feature_points_bundle = feature_points_bundle

