import MySQLdb
from database.db_protocol import DBProtocol

class FeaturePointsPositionDB(DBProtocol):
    def __init__(self):
        db_name = 'feature_points_position'
        create_db_sql = "CREATE TABLE IF NOT EXISTS feature_points_position(id INT, x FLOAT, y FLOAT, z FLOAT)"

        super().__init__(db_name, create_db_sql)

    def create(self, fp_id, x, y, z):
        sql = "INSERT INTO feature_points_position(id, x, y, z) VALUES ({}, {}, {}, {})".format(fp_id, x, y, z)
        super().create(sql)

    def find(self, fp_id):
        sql = "SELECT * FROM feature_points_position WHERE id={}".format(fp_id)
        return super().find(sql)
