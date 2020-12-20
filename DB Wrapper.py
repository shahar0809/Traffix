import sqlite3


class sqlite_database():
    def create_connection(db_file):
        """
        create a database connection to the SQLite database specified by db_file
        :param db_file: database file
        :return: Connection object or None
        """
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            return conn
        except sqlite3.Error as e:
            print(e)

        return conn

    def create_table(conn, create_table_sql):
        """
        create a table from the create_table_sql statement
        :param conn: Connection object
        :param create_table_sql: a CREATE TABLE statement
        :return:
        """
        try:
            c = conn.cursor()
            c.execute(create_table_sql)
        except sqlite3.Error as e:
            print(e)

    def sql_table(database):
        sql_create_cameras_table = """CREATE TABLE IF NOT EXISTS cameras (
                                            id integer PRIMARY KEY,
                                            focal_length integer NOT NULL,
                                            optical_center_x integer NOY NULL,
                                            optical_center_y integer NOY NULL
                                        );"""

        sql_create_environments_table = """ CREATE TABLE IF NOT EXISTS environments (
                                               id integer PRIMARY KEY,
                                               camera_id integer NOT NULL,
                                               Crosswalk_point_1 point NOT NULL,
                                               Crosswalk_point_2 point NOT NULL,
                                               traffic_bar_low Numeric NOT NULL,
                                               traffic_bar_mid Numeric NOT NULL,
                                               traffic_bar_high Numeric NOT NULL,
                                               FOREIGN KEY (camera_id) REFERENCES cameras (id)
                                           ); """

        sql_create_loads_table = """ CREATE TABLE IF NOT EXISTS loads (
                                                   level integer PRIMARY KEY,
                                                   env_id integer NOT NULL,
                                                   hour Numeric NOT NULL,
                                                   day Numeric NOT NULL,
                                                   FOREIGN KEY (env_id) REFERENCES environments (id)
                                               ); """

        # create a database connection
        conn = IDatabase.create_connection(database)

        # create tables
        if conn is not None:
            # create cameras table
            IDatabase.create_table(conn, sql_create_cameras_table)

            # create environments table
            IDatabase.create_table(conn, sql_create_environments_table)

            # create loads table
            IDatabase.create_table(conn, sql_create_loads_table)

        else:
            print("Error! cannot create the database connection.")

    def get_camera_details(camera_id, conn):
        """
        return camera details
        :param conn: Connection object
        :param camera_id: The id of the camera that we want to return
        :return: camera details
        """
        #select camera details
        sql_select = """SELECT * FROM cameras WHERE ID = ?"""
        cursor = conn.execute(sql_select, (camera_id,))
        return_select = cursor.fetchone()

        return return_select

    def get_crosswalk_details(env_id, conn):
        """
        return crosswalk details
        :param conn: Connection object
        :param env_id:
        :return: crosswalk details
        """
        #select crosswalk details
        sql_select = """SELECT * FROM environments WHERE ID = ?"""
        cursor = conn.execute(sql_select, (env_id,))
        return_select = cursor.fetchone()

        return return_select

    def get_environment(env_id, conn):
        """
           return environments details
           :param conn: Connection object
           :param env_id: The id of the environments that we want to return
           :return: environments details
           """
        # select environments details
        sql_select = """SELECT * FROM environments WHERE ID = ?"""
        cursor = conn.execute(sql_select, (env_id,))
        return_select = cursor.fetchone()

        return return_select

    def set_camera_details(focal_length, optical_center_x, optical_center_y, conn):
        """
           insert to the table cameras details
           :param conn: Connection object
           :param focal_length, optical_center_x, optical_center_y: The details of the camera that we want to insert.
           :return: true if the insert works, false if doesn't.
           """
        cursor = conn.cursor()
        # select environments details
        sql_insert = "INSERT INTO cameras (focal_length, optical_center_x, optical_center_y) VALUES (%d, %d, %d)"

        try:
            insert = cursor.execute(sql_insert, (focal_length, optical_center_x, optical_center_y))
            conn.commit()
            cursor.close()
            return True

        except sqlite3.Error as e:
            cursor.close()
            return e


# Create a IDatabase class that inherits from sqlite_database
class IDatabase(sqlite_database):
    sqlite_database.sql_table()


def main():
    database = r"C:/Users/משתמש/traffix/traffixDB.db"

    # Create instance of idatabase
    idatabase = IDatabase()
    idatabase.sql_table(database)


if __name__ == '__main__':
    main()
