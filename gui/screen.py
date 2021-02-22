import tkinter as tk
from database import SQLiteDatabase as sql_db

class Screen(tk.Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        self.database = sql_db.SQLiteDatabase()

        tk.Frame.__init__(self, parent)
