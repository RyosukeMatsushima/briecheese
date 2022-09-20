import MySQLdb

class DBProtocol:
    def __init__(self, db_name, create_db_sql):

        self.connection = MySQLdb.connect(
            host='db',
            port=3306,
            user='docker',
            passwd='docker',
            db=db_name
            )
        self.connection.autocommit(False)
        self.cursor = self.connection.cursor()

        self.cursor.execute(create_db_sql)

    def close(self):
        self.connection.commit()
        self.connection.close()

    def create(self, sql):
        self.cursor.execute(sql)
        self.connection.commit()

    def find(self, sql):
        self.cursor.execute(sql)
        return self.cursor.fetchall()[0]
