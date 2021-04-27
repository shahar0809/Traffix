# TODO: Reformat code according to conventions


class IDatabase:
    # TODO: Add documentation about the classes and the code
    """

    """
    auto_file = "C:/Users/משתמש/traffix/database/traffixDB.db"

    def __init__(self, file=None):
        if file is not None:
            self.db_file = file
        else:
            self.db_file = self.auto_file

        self.hours = [i for i in range(1, 25)]
        self.conn = None

    def create_connection(self):
        raise NotImplementedError

    def get_camera_details(self, camera_id):
        raise NotImplementedError

    def get_crosswalk_details(self, env_id):
        raise NotImplementedError

    def get_environment(self, env_id):
        raise NotImplementedError

    def set_crosswalk_details(self, crosswalk_point, env_id):
        raise NotImplementedError

    def set_traffic_bars(self, env_id, traffic_bar):
        raise NotImplementedError

    def get_traffic_bars(self, env_id):
        raise NotImplementedError

    def get_traffic_data(self, day, hour, env_id):
        raise NotImplementedError

    def set_traffic_data(self, env_id, day, hour, data):
        return NotImplementedError

    def set_traffic_per_week(self, env_id, loads_list):
        raise NotImplementedError

    def add_environment(self, name, camera_id, crosswalk, bars, location):
        raise NotImplementedError

    def get_cameras(self):
        raise NotImplementedError

    def get_environments(self):
        raise NotImplementedError
