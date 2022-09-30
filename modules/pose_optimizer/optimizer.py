import numpy as np
import cv2 as cv

from modules.pose_optimizer.datastore.keyframe import Keyframe

class Optimizer:

    def __init__(self):

        self.feature_points_position = np.array([])
        self.keyframes = []
        self.last_id = 0

        self.position_bundle_constant = 0.5
        self.rotation_bundle_constant = 0.5
        self.position_constant = 0.1
        self.rotation_constant = 0.1

        self.feature_points_force_threshold = 0.0001
        self.keyframe_force_threshold = 0.0000001
        self.keyframe_moment_threshold = 0.0000001


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
    def optimize(self, max_trial, callback, optimize_feature_point=True):

        is_enough = False

        trial = 0

        while not is_enough:
            feature_points_force = np.zeros(np.shape(self.feature_points_position))
            is_keyframes_enough = True
            for keyframe in self.keyframes:
                output1, output2 = self.calculate(keyframe)
                feature_points_force += output1
                is_keyframes_enough = is_keyframes_enough and output2

            if optimize_feature_point:
                self.feature_points_position += feature_points_force

            evaluate_value = np.linalg.norm(np.sum(feature_points_force, axis=0)) / np.shape(self.feature_points_position)[0]
            is_enough = evaluate_value < self.feature_points_force_threshold\
                        and is_keyframes_enough

            callback(trial, evaluate_value)

            if trial >= max_trial:
                break
            trial += 1


    def calculate(self, keyframe):

        keyframe_force = np.zeros(3)
        keyframe_moment = np.identity(3)
        feature_points_force = np.zeros(np.shape(self.feature_points_position))
        keyframe_force_constant = self.position_constant / len(keyframe.feature_points_bundle)
        keyframe_moment_constant = self.rotation_constant / len(keyframe.feature_points_bundle)

        for feature_point_bundle in keyframe.feature_points_bundle:

            feature_point_id = feature_point_bundle[0]
            current_feature_point_position = self.feature_points_position[feature_point_id]

            vector_to_feature_point = current_feature_point_position - keyframe.position
            vector_size = np.linalg.norm(vector_to_feature_point)
            vector_to_feature_point /= vector_size

            feature_point_bundle = keyframe.rotation @ feature_point_bundle[1]

            moment = np.cross(vector_to_feature_point, feature_point_bundle)
            force = np.cross(moment, feature_point_bundle) * vector_size

            keyframe_force -= force * keyframe_force_constant
            keyframe_moment = cv.Rodrigues( - moment * keyframe_moment_constant)[0] @ keyframe_moment
            feature_points_force[feature_point_id] += force * self.position_constant


        if keyframe.position_bundle.size != 0:
            keyframe_force -= ( keyframe.position - keyframe.position_bundle ) * self.position_bundle_constant

        if keyframe.rotation_bundle.size != 0:
            m = cv.Rodrigues( keyframe.rotation @ np.linalg.inv(keyframe.rotation_bundle) )[0].T[0] * self.rotation_bundle_constant
            keyframe_moment = cv.Rodrigues( -m )[0] @ keyframe_moment


        keyframe.position += keyframe_force
        keyframe.rotation = keyframe_moment @ keyframe.rotation

        is_keyframe_enough = np.linalg.norm(keyframe_force) < self.keyframe_force_threshold \
                         and np.linalg.norm(keyframe_moment) < self.keyframe_moment_threshold
        return feature_points_force, is_keyframe_enough


