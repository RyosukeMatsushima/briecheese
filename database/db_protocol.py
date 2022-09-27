import MySQLdb


class DBProtocol:
    def __init__(self, table_name, data_format):

        self.connection = MySQLdb.connect(
            host="db", port=3306, user="docker", passwd="docker", db="briecheese"
        )
        self.connection.autocommit(False)
        self.cursor = self.connection.cursor()

        self.table_name = table_name
        sql = "CREATE TABLE IF NOT EXISTS {} {}".format(table_name, data_format)
        self.cursor.execute(sql)

    def close(self):
        self.connection.commit()
        self.connection.close()

    def create(self, sql):
        self.cursor.execute(sql)
        self.connection.commit()

    def find(self, sql):
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def delete_all(self):
        sql = "TRUNCATE TABLE {}".format(self.table_name)
        self.cursor.execute(sql)
        self.connection.commit()
