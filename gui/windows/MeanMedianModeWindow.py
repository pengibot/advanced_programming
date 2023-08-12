import tkinter as tk

from utils.LoggerFactory import LoggerFactory


class MeanMedianModeWindow:
    def __init__(self, master, data_manager):
        LoggerFactory.get_logger().info("Initialized Mean/Median/Mode Window")
        self.window = tk.Toplevel(master)
        self.window.grab_set()
        self.window.title("Mean/Median/Mode")
        icon = tk.PhotoImage(file="gui/assets/mean_median_mode.png")
        self.window.iconphoto(False, icon)
