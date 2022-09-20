import MySQLdb

class FeaturePointsPositionDB:
    def __init__(self):
        self.connection = MySQLdb.connect(
            host='db',
            port=3306,
            user='docker',
            passwd='docker',
            db='feature_points_position'
            )
        self.connection.autocommit(False)
        self.cursor = self.connection.cursor()

        sql = "CREATE TABLE IF NOT EXISTS feature_points_position(id INT, x FLOAT, y FLOAT, z FLOAT)"
        self.cursor.execute(sql)

    def close(self):
        self.connection.commit()
        self.connection.close()

    def create(self, id, x, y, z):
        sql = "INSERT INTO feature_points_position(id, x, y, z) VALUES ({}, {}, {}, {})".format(id, x, y, z)
        self.cursor.execute(sql)
        self.connection.commit()

    def find(self, id):
        sql = "SELECT * FROM feature_points_position WHERE id={}".format(id)
        self.cursor.execute(sql)
        return self.cursor.fetchall()[0]
