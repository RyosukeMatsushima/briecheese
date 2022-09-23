import MySQLdb
from database.db_protocol import DBProtocol

class KeyframesPoseDB(DBProtocol):
    def __init__(self):
        table_name = "keyframes_pose"
        data_format = "(id INT,\
                        x FLOAT, y FLOAT, z FLOAT,\
                        rot_x FLOAT, rot_y FLOAT, rot_z FLOAT)"

        super().__init__(table_name, data_format)

    def create(self, kf_id, x, y, z, rot_x, rot_y, rot_z):
        sql = "INSERT INTO \
                {}(id, x, y, z, rot_x, rot_y, rot_z) \
               VALUES ({}, {}, {}, {}, {}, {}, {})".format(self.table_name, kf_id, x, y, z, rot_x, rot_y, rot_z)
        super().create(sql)

    def find(self, kf_id):
        sql = "SELECT * FROM {} WHERE id={}".format(self.table_name, kf_id)
        #TODO: add fetched data size check.
        return super().find(sql)[0]
