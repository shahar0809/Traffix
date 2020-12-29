import sqlite3
import datetime as dt
from abc import ABC

MAX_DAY = 7


class IDatabase:
    """

    """
    hours = [i for i in range(1, 25)]
    conn = None

    def get_camera_details(self, camera_id):
        raise NotImplementedError

    def get_crosswalk_details(self, env_id):
        raise NotImplementedError

    def get_environment(self, env_id):
        raise NotImplementedError

    def set_camera_details(self, focal_length, optical_center):
        raise NotImplementedError

    def set_crosswalk_details(self, crosswalk_point, env_id):
        raise NotImplementedError

    def set_traffic_bars(self, env_id, traffic_bar):
        raise NotImplementedError

    def get_traffic_data(self, day, hour):
        raise NotImplementedError

    def set_traffic_per_week(self, loads_list):
        raise NotImplementedError


class SqliteDatabase(IDatabase):
    def create_connection(self, db_file):
        """
        create a database connection to the SQLite database specified by db_file
        :param db_file: database file
        :return: Connection object or None
        """
        try:
            self.conn = sqlite3.connect(db_file)
            return self.conn
        except sqlite3.Error as e:
            print(e)

        return self.conn

    def sql_table(self, db_file):
        sql_create_cameras_table = """CREATE TABLE IF NOT EXISTS cameras (
                                                id integer PRIMARY KEY,
                                                focal_length integer NOT NULL,
                                                optical_center_x integer NOY NULL,
                                                optical_center_y integer NOY NULL
                                            );"""

        sql_create_environments_table = """ CREATE TABLE IF NOT EXISTS environments (
                                                   id integer PRIMARY KEY,
                                                   camera_id integer NOT NULL,
                                                   crosswalk_point_1 point NOT NULL,
                                                   crosswalk_point_2 point NOT NULL,
                                                   crosswalk_point_3 point NOT NULL,
                                                   crosswalk_point_4 point NOT NULL,
                                                   traffic_bar_low integer NOT NULL,
                                                   traffic_bar_mid integer NOT NULL,
                                                   traffic_bar_high integer NOT NULL,
                                                   FOREIGN KEY (camera_id) REFERENCES cameras (id)
                                               ); """

        sql_create_loads_table = """ CREATE TABLE IF NOT EXISTS loads (
                                                       env_id integer PRIMARY KEY,
                                                       priority ENUM NOT NULL,
                                                       hour integer NOT NULL,
                                                       day integer NOT NULL,
                                                       FOREIGN KEY (env_id) REFERENCES environments (id)
                                                   ); """

        # create a database connection
        self.conn = self.create_connection(db_file)

        # create tables
        if self.conn is not None:
            # create cameras table
            self.create_table(sql_create_cameras_table)

            # create environments table
            self.create_table(sql_create_environments_table)

            # create loads table
            self.create_table(sql_create_loads_table)

        else:
            print("Error! cannot create the database connection.")

    def create_table(self, create_table_sql):
        """
        create a table from the create_table_sql statement
        :param conn: Connection object
        :param create_table_sql: a CREATE TABLE statement
        :return:
        """
        try:
            c = self.conn.cursor()
            c.execute(create_table_sql)
        except sqlite3.Error as e:
            return e

    def get_camera_details(self, camera_id):
        """
        return camera details
        :param camera_id: The id of the camera that we want to return
        :return: camera details
        """
        #select camera details
        sql_select = "SELECT * FROM cameras WHERE ID = ?"
        cursor = self.conn.execute(sql_select, (camera_id,))
        record = cursor.fetchall()

        for row in record:
            print("id = ", row[0])
            print("focal_length = ", row[1])
            print("optical_center_x = ", row[2])
            print("optical_center_y  = ", row[3])

    def get_crosswalk_details(self, env_id):
        """
        return crosswalk details
        :param env_id: Will indicate a relevant environment
        :return: crosswalk details
        """
        #select crosswalk details
        sql_select = "SELECT Crosswalk_point_1, Crosswalk_point_2, Crosswalk_point_3, Crosswalk_point_4 FROM environments WHERE ID = ?"
        cursor = self.conn.execute(sql_select, (env_id,))
        record = cursor.fetchall()

        for row in record:
            print("Crosswalk_point_1 = ", row[0])
            print("Crosswalk_point_2 = ", row[1])
            print("Crosswalk_point_3 = ", row[2])
            print("Crosswalk_point_4  = ", row[3])

    def get_environment(self, env_id):
        """
           return environments details
           :param env_id: The id of the environments that we want to return
           :return: environments details
           """
        # select environments details
        sql_select = """SELECT * FROM environments WHERE ID = ?"""
        cursor = self.conn.execute(sql_select, (env_id,))
        record = cursor.fetchall()

        for row in record:
            print("camera_id integer ", row[0])
            print("crosswalk_point_1 = ", row[1])
            print("Crosswalk_point_2 = ", row[2])
            print("Crosswalk_point_3 = ", row[3])
            print("Crosswalk_point_4  = ", row[4])
            print("traffic_bar_low  = ", row[5])
            print("traffic_bar_mid  = ", row[6])
            print("traffic_bar_high  = ", row[7])

    def set_camera_details(self, focal_length, optical_center):
        """
           insert to the table cameras details
           :param focal_length: The focal length that we want to update to.
           :param  optical_center: A list of the information we want to update to.
           :return: true if the update works, false if doesn't.
           """
        cursor = self.conn.cursor()
        # insert camera details
        sql_insert = "INSERT INTO cameras (focal_length, optical_center_x, optical_center_y)" \
                     "VALUES (?, ?, ?)"
        val = (focal_length, optical_center[0], optical_center[1])
        try:
            cursor.execute(sql_insert, val)
            self.conn.commit()
            cursor.close()
            print("The details inserts")
            return True

        except sqlite3.Error as e:
            cursor.close()
            return e

    def set_crosswalk_details(self, crosswalk_point, env_id):
        """
        insert to the table cameras details
        :param crosswalk_point: A list of the information we want to update to.
        :param env_id: The place where we want to update.
        :return: true if the update works, false if doesn't.
        """
        cursor = self.conn.cursor()
        # update crosswalk details
        sql_update = "UPDATE environments SET crosswalk_point_1 = ?, crosswalk_point_2 = ?, crosswalk_point_3 = ?, crosswalk_point_4 = ? WHERE env_id = ?"

        try:
            cursor.execute(sql_update, (crosswalk_point[0], crosswalk_point[1], crosswalk_point[2], crosswalk_point[3], env_id))
            self.conn.commit()
            cursor.close()
            return "The details inserts"

        except sqlite3.Error as e:
            cursor.close()
            return e

    def get_traffic_data(self, day, hour):
        """
        return traffic data
        :param day: Will indicate a relevant environment
        :param hour: Will indicate a relevant environment
        :return: crosswalk details
        """
        # select crosswalk details
        sql_select = "SELECT level FROM loads WHERE day = %d AND hour = %d"
        cursor = self.conn.execute(sql_select, (day, hour))
        return_select = cursor.fetchone()

        return return_select

    def set_traffic_bars(self, env_id, traffic_bar):
        """
        insert to the table cameras details
        :param env_id: The place where we want to update.
        :param traffic_bar: A list of the information we want to update to.
        :return: true if the update works, false if doesn't.
        """
        cursor = self.conn.cursor()
        # update traffic bar details
        sql_update = "UPDATE environments SET traffic_bar_low = %d, traffic_bar_mid = %d, traffic_bar_high = %d WHERE env_id = %d"

        try:
            cursor.execute(sql_update, (traffic_bar[0], traffic_bar[1], traffic_bar[2], env_id))
            self.conn.commit()
            cursor.close()
            return True

        except sqlite3.Error as e:
            cursor.close()
            return e


def main():
    database = r"C:/Users/משתמש/traffix/traffixDB.db"

    sqlite_database = SqliteDatabase()

    sqlite_database.create_connection(database)
    sqlite_database.sql_table(database)
    try:
        focal_length = int(input("Enter the focal_length you want to insert to the cameras table: "))
        optical_center_x = int(input("Enter the optical_center_x you want to insert to the cameras table: "))
        optical_center_y = int(input("Enter the optical_center_y you want to insert to the cameras table: "))
        optical_center = [optical_center_x, optical_center_y]
        sqlite_database.set_camera_details(focal_length, optical_center)

        camera_id = int(input("\nEnter the ID of the camera from which you want details: "))
        sqlite_database.get_camera_details(camera_id)

        env_id = int(input("\nEnter the ID of the environment from which you want details: "))
        print(sqlite_database.get_environment(env_id))

        env_id = int(input("\nEnter the ID of the environment from which you want the crosswalk details: "))
        print(sqlite_database.get_crosswalk_details(env_id))

    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
