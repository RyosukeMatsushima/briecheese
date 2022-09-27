from database.db_protocol import DBProtocol

"""
data format

feature_point_id
type: INT

keyframe_id
type: INT

x, y, z
type: FLOAT
unit vector to represent direction to featurepoint from keyframe
"""


class BundlesDB(DBProtocol):
    def __init__(self):
        table_name = "bundles"
        data_format = "(feature_point_id INT,\
                        keyframe_id INT,\
                        x FLOAT, y FLOAT, z FLOAT)"

        super().__init__(table_name, data_format)

    def create(self, fp_id, kf_id, x, y, z):
        sql = "INSERT INTO \
               {}(feature_point_id,\
                  keyframe_id,\
                  x, y, z) \
               VALUES ({}, {}, {}, {}, {})".format(
            self.table_name, fp_id, kf_id, x, y, z
        )
        super().create(sql)

    def find_by(self, feature_point_id):
        sql = "SELECT * FROM {} WHERE feature_point_id={}".format(
            self.table_name, feature_point_id
        )
        return super().find(sql)
