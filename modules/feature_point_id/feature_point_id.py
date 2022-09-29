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
        for m in matches:
            feature_point_id_column = self.db.find_by_descriptor(
                json.dumps(self.matcher.getTrainDescriptors()[0][m.trainIdx].tolist())
            )
            response.append([keypoints[m.queryIdx].pt, feature_point_id_column[0]])
            match_keypoints.append(keypoints[m.queryIdx])

        all_descriptors = list(zip(keypoints, descriptors))
        add_matcher_descriptors = []
        for descriptors in all_descriptors:
            if not descriptors[0] in match_keypoints:
                feature_point_id_column = self.db.create(descriptors[1].tolist())
                response.append([descriptors[0].pt, feature_point_id_column[0]])
                add_matcher_descriptors.append(np.uint8(descriptors[1]))
        if add_matcher_descriptors:
            self.matcher.add(np.asarray([add_matcher_descriptors]))

        return response

    def detectAndCompute(self, frame):
        keypoints, descriptors = self.detector.detectAndCompute(frame, None)
        if descriptors is None:
            descriptors = []
        return keypoints, descriptors
