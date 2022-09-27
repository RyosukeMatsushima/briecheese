from database.db_protocol import DBProtocol
import os

class DescriptorsDB(DBProtocol):
    def __init__(self):
        table_name = os.getenv("DESCRIPTORS_DB_TABLE", "descriptors")
        data_format = "(id INT AUTO_INCREMENT, descriptor JSON, PRIMARY KEY (id))"
        super().__init__(table_name, data_format)

    def create(self, json_descriptor):
        sql = "INSERT INTO {}(descriptor) VALUES ('{}')".format(
            self.table_name, json_descriptor
        )
        super().create(sql)
        return self.find_by_descriptor(json_descriptor)

    def find_by_descriptor(self, json_descriptor):
        sql = "SELECT * FROM {} WHERE descriptor -> \"$\" = CAST('{}' AS JSON)".format(
            self.table_name, json_descriptor
        )
        return super().find(sql)[0]

    def get_all(self):
        sql = "SELECT * FROM {}".format(self.table_name)
        return super().find(sql)
