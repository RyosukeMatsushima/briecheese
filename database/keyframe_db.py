from database.db_protocol import DBProtocol
import os


class KeyframeDB(DBProtocol):
    def __init__(self):
        table_name = os.getenv("KEYFRAME_DB_TABLE", "keyframe")
        data_format = "(id INT, position JSON, rotation JSON, observed_position JSON, observed_rotation JSON)"

        super().__init__(table_name, data_format)

    def create(self, id, position, rotation, observed_position, observed_rotation):
        sql = "INSERT INTO {}(id, position, rotation, observed_position, observed_rotation) VALUES ({}, '{}', '{}', '{}', '{}')".format(
            self.table_name, id, position, rotation, observed_position, observed_rotation
        )
        super().create(sql)

    def find(self, id):
        sql = "SELECT * FROM {} WHERE id={}".format(self.table_name, id)
        return super().find(sql)[0]
