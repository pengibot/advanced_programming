import tkinter as tk

from LoggerFactory import LoggerFactory


class MeanMedianModeWindow:
    def __init__(self, update_log, master=None):
        LoggerFactory.get_logger().info("Inside Main Window!")
        self.window = tk.Toplevel(master)
        self.window.grab_set()
        self.window.title("Mean/Median/Mode")
