import tkinter as tk


class GraphWindow:
    def __init__(self, update_log, master=None):
        self.window = tk.Toplevel(master)
        self.window.grab_set()
        self.window.title("Graph")
