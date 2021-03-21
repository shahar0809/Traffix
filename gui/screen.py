import tkinter as tk
import os
import database.SQLiteDatabase as sql_db


class Screen(tk.Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        self.default_font = "Consolas"
        ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        path = os.path.join(ROOT_DIR, os.path.join('database', 'traffixDB.db'))
        self.database = sql_db.SQLiteDatabase(path)
        tk.Frame.__init__(self, parent)
        self.pack_propagate(0)

    def destroy_screen(self):
        self.grid_forget()
        self.destroy()
