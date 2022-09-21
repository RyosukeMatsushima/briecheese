import MySQLdb
from database.db_protocol import DBProtocol

class KeyframesPoseDB(DBProtocol):
    def __init__(self):
        create_db_sql = "CREATE TABLE IF NOT EXISTS \
                         keyframes_pose(id INT,\
                         x FLOAT, y FLOAT, z FLOAT, rot_x FLOAT, rot_y FLOAT, rot_z FLOAT)"

        super().__init__(create_db_sql)

    def create(self, kf_id, x, y, z, rot_x, rot_y, rot_z):
        sql = "INSERT INTO \
               keyframes_pose(id, x, y, z, rot_x, rot_y, rot_z) \
               VALUES ({}, {}, {}, {}, {}, {}, {})".format(kf_id, x, y, z, rot_x, rot_y, rot_z)
        super().create(sql)

    def find(self, kf_id):
        sql = "SELECT * FROM keyframes_pose WHERE id={}".format(kf_id)
        return super().find(sql)[0]
