import tkinter as tk

from LoggerFactory import LoggerFactory


class MeanMedianModeWindow:
    def __init__(self, master=None):
        LoggerFactory.get_logger().info("Initialized Mean/Median/Mode Window")
        self.window = tk.Toplevel(master)
        self.window.grab_set()
        self.window.title("Mean/Median/Mode")
