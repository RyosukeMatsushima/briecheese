from database.db_protocol import DBProtocol
import os


class FeaturePointDB(DBProtocol):
    def __init__(self):
        table_name = os.getenv("FEATURE_POINT_DB_TABLE", "feature_point")
        data_format = "(id INT AUTO_INCREMENT, position JSON, PRIMARY KEY (id))"

        super().__init__(table_name, data_format)

    def create(self, position):
        sql = "INSERT INTO {}(position) VALUES ('{}')".format(self.table_name, position)
        super().create(sql)

    def find(self, id):
        sql = "SELECT * FROM {} WHERE id={}".format(self.table_name, id)
        return super().find(sql)[0]
