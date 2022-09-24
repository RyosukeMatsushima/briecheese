import MySQLdb
from database.db_protocol import DBProtocol

class DescriptorsDB(DBProtocol):
    def __init__(self):
        table_name = "descriptors"
        data_format = "(id INT AUTO_INCREMENT, descriptor JSON, PRIMARY KEY (id))"
        super().__init__(table_name, data_format)

    def create(self, descriptor):
        sql = 'INSERT INTO {}(id, descriptor) VALUES ({}, \'{}\')'.format(self.table_name, descriptor)
        super().create(sql)
        self.find_by_descriptor(descriptor)

    def find_by_descriptor(self, descriptor):
        sql = "SELECT * FROM {} WHERE descriptor -> \"$\" = CAST(\'{}\' AS JSON)".format(self.table_name, descriptor)
        return super().find(sql)[0]
    
    def get_all(self):
        sql = "SELECT * FROM {}".format(self.table_name)
        return super().find(sql)
