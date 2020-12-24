import sqlite3
import datetime as dt

MAX_DAY = 7


class SqliteDatabase:
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

    def get_traffic_data(self, day, hour):
        raise NotImplementedError

    def set_camera_details(self, focal_length, optical_center, camera_id):
        raise NotImplementedError

    def set_crosswalk_details(self, crosswalk_point, env_id):
        raise NotImplementedError

    def set_traffic_bars(self, env_id, traffic_bar):
        raise NotImplementedError

    def set_traffic_per_week(self, loads_list):
        raise NotImplementedError

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
                                                   priority ENUM('Low', 'Medium', 'High') NOT NULL,
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
            print(e)


class IDatabase(SqliteDatabase):

    def get_camera_details(self, camera_id):
        """
        return camera details
        :param camera_id: The id of the camera that we want to return
        :return: camera details
        """
        #select camera details
        sql_select = """SELECT * FROM cameras WHERE ID = ?"""
        cursor = self.conn.execute(sql_select, (camera_id,))
        return_select = cursor.fetchone()

        return return_select

    def get_crosswalk_details(self, env_id):
        """
        return crosswalk details
        :param env_id: Will indicate a relevant environment
        :return: crosswalk details
        """
        #select crosswalk details
        sql_select = "SELECT Crosswalk_point_1, Crosswalk_point_2, Crosswalk_point_3, Crosswalk_point_4 FROM environments WHERE ID = ?"
        cursor = self.conn.execute(sql_select, (env_id,))
        return_select = cursor.fetchone()

        return return_select

    def get_environment(self, env_id):
        """
           return environments details
           :param **kwargs:
           :param env_id: The id of the environments that we want to return
           :return: environments details
           """
        # select environments details
        sql_select = """SELECT * FROM environments WHERE ID = ?"""
        cursor = self.conn.execute(sql_select, (env_id,))
        return_select = cursor.fetchone()

        return return_select

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

    def set_camera_details(self, focal_length, optical_center, camera_id):
        """
           insert to the table cameras details
           :param focal_length: The focal length that we want to update to.
           :param  optical_center: A list of the information we want to update to.
           :param  camera_id: The place where we want to update.
           :return: true if the update works, false if doesn't.
           """
        cursor = self.conn.cursor()
        # update camera details
        sql_update = "UPDATE cameras SET focal_length= %d, optical_center_x = %d, optical_center_y = %d WHERE camera_id = %d"

        try:
            insert = cursor.execute(sql_update, (focal_length, optical_center[0], optical_center[1], camera_id))
            self.conn.commit()
            cursor.close()
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
        sql_update = "UPDATE environments SET crosswalk_point_1 = %d, crosswalk_point_2 = %d, crosswalk_point_3 = %d, crosswalk_point_4 = %d WHERE env_id = %d"

        try:
            cursor.execute(sql_update, (crosswalk_point[0], crosswalk_point[1], crosswalk_point[2], crosswalk_point[3], env_id))
            self.conn.commit()
            cursor.close()
            return True

        except sqlite3.Error as e:
            cursor.close()
            return e

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

    def set_traffic_per_week(self, hours):
        """
        delete old data and insert new.
        :param hours:
        :return: environments details
        """
        # delete loads data
        sql_delete = "DELETE FROM loads"
        cursor = self.conn.execute(sql_delete)
        d = cursor.fetchone()

        m = 1
        n = 0
        try:
            for i in range(1, 8):
                while n < 24:
                    self.get_traffic_data(m, hours[n])
                    n += 1
                m += 1
                n = 0

            return True

        except sqlite3.Error as e:
            cursor.close()
            return e


def main():
    database = r"C:/Users/משתמש/traffix/traffixDB.db"

    sqlite_database = SqliteDatabase()

    sqlite_database.create_connection(database)
    sqlite_database.sql_table(database)


if __name__ == '__main__':
    main()
