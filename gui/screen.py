import tkinter as tk
import database.SQLite_Database as sql_db


class Screen(tk.Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        self.sql = sql_db.SQLiteDatabase()
        self.database = self.sql.create_connection()

        tk.Frame.__init__(self, parent)
