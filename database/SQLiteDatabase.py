import sqlite3
import utils
from measurements_calculations.math_classes import Point
from database.DB_Wrapper import IDatabase

AMOUNT_OF_DAYS = 7
AMOUNT_OF_HOURS = 24


class SQLiteDatabase(IDatabase):
    def get_traffic_bars(self, env_id):
        # select crosswalk details
        sql_select = "SELECT traffic_bar_low, traffic_bar_med, traffic_bar_high" \
                     "  FROM environments WHERE ID = ?"
        cursor = self.conn.execute(sql_select, (env_id,))

        record = cursor.fetchall()
        return record

    def __init__(self, file=None):
        super().__init__(file)
        self.create_connection()
        self.sql_table()

    def create_connection(self):
        """
        create a database connection to the SQLite database specified by db_file
        :return: Connection object or None
        """
        try:
            self.conn = sqlite3.connect(self.db_file)
            return self.conn
        except sqlite3.Error as e:
            print(e)

        return self.conn

    def sql_table(self):
        sql_create_cameras_table = """CREATE TABLE IF NOT EXISTS cameras (
                                            id integer PRIMARY KEY,
                                            name text NOT NULL,
                                            fps integer NOT NULL,
                                            camera_index integer NOT_NULL
                                        );"""

        sql_create_environments_table = """ CREATE TABLE IF NOT EXISTS environments (
                                                    id integer PRIMARY KEY,
                                                    name TEXT NOT NULL,
                                                    crosswalk_point_1 TEXT NOT NULL,
                                                    crosswalk_point_2 TEXT NOT NULL,
                                                    crosswalk_point_3 TEXT NOT NULL,
                                                    crosswalk_point_4 TEXT NOT NULL,
                                                    traffic_bar_low integer NOT NULL,
                                                    traffic_bar_med integer NOT NULL,
                                                    traffic_bar_high integer NOT NULL,
                                                    width integer NOT NULL,
                                                    length integer NOT NULL,
                                                    FOREIGN KEY (camera_id) REFERENCES cameras (id),
                                                    is_above BIT NOT NULL,
                                                    longitude INTEGER NOT NULL,
                                                    latitude INTEGER NOT NULL
                                               ); """

        sql_create_loads_table = """ CREATE TABLE IF NOT EXISTS loads (
                                                    env_id integer PRIMARY KEY,
                                                    level integer NOT NULL,
                                                    hour integer NOT NULL,
                                                    day integer NOT NULL,
                                                    FOREIGN KEY (env_id) REFERENCES environments (id)
                                               ); """

        # create a database connection
        self.conn = self.create_connection()

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
        # select camera details
        sql_select = """SELECT * FROM cameras WHERE ID = ?"""
        cursor = self.conn.execute(sql_select, (camera_id,))
        record = cursor.fetchall()

        if len(record) > 1:
            raise Exception

        camera_name = ""
        fps = 0
        opencv_index = 0

        for row in record:
            camera_id = row[0]
            camera_name = row[1]
            fps = row[2]
            opencv_index = row[3]

        return utils.CameraDetails(camera_name, fps, opencv_index, camera_id)

    def get_crosswalk_details(self, env_id):
        """
        return crosswalk details
        :param env_id: Will indicate a relevant environment
        :return: crosswalk details
        """
        # select crosswalk details
        sql_select = "SELECT Crosswalk_point_1, Crosswalk_point_2, Crosswalk_point_3, Crosswalk_point_4, width, length, is_above FROM environments WHERE ID = ?"
        cursor = self.conn.execute(sql_select, (env_id,))

        record = cursor.fetchall()
        crosswalk_points = []

        for row in record:
            for i in range(4):
                crosswalk_points += [Point.to_point(row[i])]
            width = row[4]
            length = row[5]
            is_above = row[6]

            return utils.CrosswalkDetails(crosswalk_points, width, length, is_above)

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

        crosswalk = self.get_crosswalk_details(env_id)

        for row in record:
            env_id = row[0]
            name = row[1]
            bars = [row[6], row[7], row[8]]
            camera_id = row[11]
            location = (row[13], row[14])

            return utils.Environment(name, camera_id, crosswalk, bars, location, env_id)

    def add_camera_details(self, name, fps, camera_index):
        """
        insert to the table cameras details
        :param name:
        :param fps:
        :param camera_index: The index of the camera in OPENCV devices table
        :return: true if the update works, false if doesn't.
        """
        cursor = self.conn.cursor()
        # insert camera details
        sql_insert = "INSERT INTO cameras (name, fps, camera_index)" \
                     "VALUES (?,?,?)"

        try:
            cursor.execute(sql_insert, (name, fps, camera_index))
            self.conn.commit()
            cursor.close()
            return True

        except sqlite3.Error as e:
            print(e)
            cursor.close()
            return e

    def set_crosswalk_details(self, crosswalk, env_id):
        """
        insert to the table cameras details
        :param crosswalk_points: A list of the information we want to update to.
        :param env_id: The id of the environment of the crosswalk
        :return: true if the update works, false if doesn't.
        """
        # Converting all crosswalk points to Point objects
        crosswalk_points = crosswalk.get_points()

        cursor = self.conn.cursor()
        # update crosswalk details
        sql_update = "UPDATE environments SET " \
                     "width = ?" \
                     "length = ?" \
                     "is_above = ?" \
                     "crosswalk_point_1 = ?, " \
                     "crosswalk_point_2 = ?, " \
                     "crosswalk_point_3 = ?, " \
                     "crosswalk_point_4 = ? " \
                     "WHERE id = ?"

        try:
            cursor.execute(sql_update,
                           (crosswalk.get_width(), crosswalk.get_length(), crosswalk.get_is_above(),
                            crosswalk_points[0], crosswalk_points[1],
                            crosswalk_points[2], crosswalk_points[3],
                            env_id))
            self.conn.commit()
            cursor.close()
            return True

        except sqlite3.Error as e:
            cursor.close()
            raise e

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

    def set_traffic_data(self, env_id, day, hour, data):
        """
        insert to the table cameras details
        :param data:
        :param day:
        :param hour:
        :param env_id: The place where we want to update.
        :return: true if the update works, false if doesn't.
        """
        cursor = self.conn.cursor()
        # update traffic bar details
        sql_update = "UPDATE loads SET level = ? WHERE env_id = ? and day = ? and hour = ?"

        try:
            cursor.execute(sql_update, (data, env_id, day, hour))
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
        sql_update = "UPDATE environments SET traffic_bar_low = ?, traffic_bar_med = ?, traffic_bar_high = ? WHERE id = ?"
        val = (traffic_bar[0], traffic_bar[1], traffic_bar[2], env_id)

        try:
            cursor.execute(sql_update, val)
            self.conn.commit()
            cursor.close()
            return True

        except sqlite3.Error as e:
            cursor.close()
            return e

    def set_traffic_per_week(self, env_id, traffic_data):
        for day in range(AMOUNT_OF_DAYS):
            for hour in range(AMOUNT_OF_HOURS):
                self.set_traffic_data(env_id, day, hour, traffic_data[day][hour])

    def add_environment(self, name, camera_id, crosswalk, bars):
        cursor = self.conn.cursor()
        crosswalk_points = crosswalk.get_points()

        # insert environment details
        crosswalk_points = [Point.to_string(crosswalk_points[i]) for i in range(4)]

        sql_insert = \
            "INSERT INTO environments (name, " \
            "crosswalk_point_1, crosswalk_point_2, crosswalk_point_3, crosswalk_point_4, " \
            "traffic_bar_low, traffic_bar_med, traffic_bar_high, " \
            "width, length, camera_id, is_above) " \
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"

        val = (name,
               crosswalk_points[0], crosswalk_points[1], crosswalk_points[2], crosswalk_points[3],
               bars[0], bars[1], bars[2],
               crosswalk.get_width(), crosswalk.get_length(),
               camera_id, int(crosswalk.get_is_above()))
        try:
            cursor.execute(sql_insert, val)
            self.conn.commit()
            cursor.close()
            return True

        except sqlite3.Error as e:
            cursor.close()
            return e


def main():
    database = SQLiteDatabase()
    database.create_connection()


if __name__ == '__main__':
    main()
