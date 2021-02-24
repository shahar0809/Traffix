import tkinter as tk
import database.SQLiteDatabase as sql_db

class Screen(tk.Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        self.database = sql_db.SQLiteDatabase("../\\database\\traffixDB.db")

        tk.Frame.__init__(self, parent)
