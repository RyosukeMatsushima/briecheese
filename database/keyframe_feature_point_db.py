import os
from database.db_protocol import DBProtocol
from database.keyframe_db import KeyframeDB
from database.feature_point_db import FeaturePointDB


class KeyframeFeaturePointDB(DBProtocol):
    def __init__(self):
        table_name = os.getenv(
            "KEYFRAME_FEATURE_POINT_DB_TABLE", "keyframe_feature_point"
        )
        data_format = "(keyframe_id INT, feature_point_id INT, direction JSON)"
        self.keyframe_db = KeyframeDB()
        self.feature_point_db = FeaturePointDB()

        super().__init__(table_name, data_format)

    def create(self, keyframe_id, feature_point_id, direction):
        sql = "INSERT INTO {}(keyframe_id, feature_point_id, direction) VALUES ({}, {}, '{}')".format(
            self.table_name, keyframe_id, feature_point_id, direction
        )
        super().create(sql)

    def get_all(self):
        sql = "SELECT * FROM {}".format(self.table_name)
        all_data = super().find(sql)
        response = []
        for data in all_data:
            keyframe = KeyframeDB().find(data[0])
            feature_point = FeaturePointDB().find(data[1])
            response.append([keyframe, feature_point, data[2]])
        return response
