#!/usr/bin/env python

from __future__ import print_function
import numpy as np
import cv2 as cv
import json
from database.descriptors_db import DescriptorsDB


class FeaturePointId:
    def __init__(self):
        flann_params = dict(
            algorithm=6, table_number=6, key_size=12, multi_probe_level=1
        )
        self.detector = cv.ORB_create(nfeatures=1000)
        self.matcher = cv.FlannBasedMatcher(flann_params, {})
        self.matcher_wit_latest = None
        self.db = DescriptorsDB()
        db_descriptors = self.db.get_all()
        descriptors = []
        for db_descriptor in db_descriptors:
            list_db_descriptor = json.loads(db_descriptor[1])
            descriptors.append(np.uint8(list_db_descriptor))
        if descriptors:
            self.matcher.add(np.asarray([descriptors]))

    def get_with_pixel(self, frame):
        keypoints, descriptors = self.detectAndCompute(frame)
        matches = self.matcher.knnMatch(descriptors, k=2)
        matches = [
            m[0] for m in matches if len(m) == 2 and m[0].distance < m[1].distance * 0.5
        ]
        response = []
        match_keypoints = []
        match_query_indexes = []

        for m in matches:
            feature_point_id_column = self.db.find_by_descriptor(
                json.dumps(self.matcher.getTrainDescriptors()[0][m.trainIdx].tolist())
            )
            response.append([keypoints[m.queryIdx].pt, feature_point_id_column[0]])
            match_keypoints.append(keypoints[m.queryIdx])

            match_query_indexes.append(m.queryIdx)

        unregistered_descriptors = np.delete(descriptors, match_query_indexes, 0)
        descriptors_to_regist = self.update_matcher_with_latest(unregistered_descriptors)

        for descriptor in descriptors_to_regist:
            feature_point_id_column = self.db.create(descriptor.tolist())
        if descriptors_to_regist:
            self.matcher.add(np.asarray([descriptors_to_regist]))

        keypoints, descriptors = self.detectAndCompute(frame)
        return response

    def update_matcher_with_latest(self, unregistered_descriptors):

        descriptors_to_regist = []

        if self.matcher_wit_latest:
            matches = self.matcher_wit_latest.knnMatch(unregistered_descriptors, k=2)
            matches = [
                m[0] for m in matches if len(m) == 2 and m[0].distance < m[1].distance * 0.5
            ]

            for m in matches:
                descriptors_to_regist.append(self.matcher_wit_latest.getTrainDescriptors()[0][m.trainIdx])

        flann_params = dict(
            algorithm=6, table_number=6, key_size=12, multi_probe_level=1
        )
        self.matcher_wit_latest = cv.FlannBasedMatcher(flann_params, {})
        self.matcher_wit_latest.add(np.asarray([unregistered_descriptors]))

        return descriptors_to_regist

    def detectAndCompute(self, frame):
        keypoints, descriptors = self.detector.detectAndCompute(frame, None)
        if descriptors is None:
            descriptors = []
        return keypoints, descriptors
