import tkinter as tk

from utils.LoggerFactory import LoggerFactory


class GraphWindow:
    def __init__(self, master=None):
        LoggerFactory.get_logger().info("Initialized Graph Window")
        self.window = tk.Toplevel(master)
        self.window.grab_set()
        self.window.title("Graph")
        icon = tk.PhotoImage(file="gui/assets/graph.png")
        self.window.iconphoto(False, icon)
