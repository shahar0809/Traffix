import tkinter as tk
import database.SQLiteDatabase as sql_db
from tkinter import font

class Screen(tk.Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        self.default_font = "Consolas"
        self.database = sql_db.SQLiteDatabase("../\\database\\traffixDB.db")
        tk.Frame.__init__(self, parent)
        self.pack_propagate(0)

    def destroy_screen(self):
        self.grid_forget()
        self.destroy()
