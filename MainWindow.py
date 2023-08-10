import tkinter as tk
from tkinter import scrolledtext

from CorrelationWindow import CorrelationWindow
from GraphWindow import GraphWindow
from LoadDataSetWindow import LoadDataSetWindow
from LoggerFactory import LoggerFactory
from MeanMedianModeWindow import MeanMedianModeWindow
from SaveDataSetWindow import SaveDataSetWindow
from TextHandler import TextHandler


class MainWindow:
    LoggerFactory.get_logger().info("Initializing Main Window")

    def __init__(self, master=None):
        self.master = master
        self.master.configure(bg='white')

        label_frame = tk.LabelFrame(self.master, text="Log", bg='white')

        self.scrolled_text = scrolledtext.ScrolledText(label_frame, wrap=tk.WORD, width=42, height=17, borderwidth=0)
        self.scrolled_text.grid(column=0, row=0, sticky="NESW")

        # Create textLogger
        text_handler = TextHandler(self.scrolled_text)
        LoggerFactory.get_logger().addHandler(text_handler)

        label_frame.columnconfigure(0, weight=1)
        label_frame.rowconfigure(0, weight=1)
        label_frame.grid(row=0, column=0, padx=5, sticky="NESW")

        rf = tk.LabelFrame(self.master, text='Functions', bg='white')
        rf.grid(row=0, column=1, pady=5, padx=10, sticky=tk.E)

        self.load_data_set_button = tk.Button(rf, text='Load Data Set', width=25, pady=5,
                                              command=self.initialize_load_data_set_window)
        self.load_data_set_button.grid(row=0, column=0, pady=7.5, padx=7.5)
        self.save_data_set_button = tk.Button(rf, text='Save Data Set', width=25, pady=5,
                                              command=self.initialize_save_data_set_window)
        self.save_data_set_button.grid(row=1, column=0, pady=7.5, padx=7.5)
        self.load_mean_median_mode_button = tk.Button(rf, text='Mean/Mode/Median', width=25, pady=5,
                                                      command=self.initialize_mean_median_mode_window)
        self.load_mean_median_mode_button.grid(row=2, column=0, pady=7.5, padx=7.5)
        self.display_graph_button = tk.Button(rf, text='Display Graph', width=25, pady=5,
                                              command=self.initialize_graph_window)
        self.display_graph_button.grid(row=3, column=0, pady=7.5, padx=7.5)
        self.display_correlation_button = tk.Button(rf, text='Display Correlation', width=25, pady=5,
                                                    command=self.initialize_correlation_window)
        self.display_correlation_button.grid(row=4, column=0, pady=10, padx=(7.5, 0))

    def initialize_load_data_set_window(self):
        LoggerFactory.get_logger().info("Initializing Load Data Set Window")
        LoadDataSetWindow(self.master)

    def initialize_save_data_set_window(self):
        LoggerFactory.get_logger().info("Initializing Save Data Set Window")
        SaveDataSetWindow(self.master)

    def initialize_mean_median_mode_window(self):
        LoggerFactory.get_logger().info("Initializing Mean/Median/Mode Window")
        MeanMedianModeWindow(self.master)

    def initialize_graph_window(self):
        LoggerFactory.get_logger().info("Initializing Graph Window")
        GraphWindow(self.master)

    def initialize_correlation_window(self):
        LoggerFactory.get_logger().info("Initializing correlation window")
        CorrelationWindow(self.master)


def main():
    window = tk.Tk()
    window.configure(bg='white')
    window.title("Interactive GUI")
    window.geometry("593x300")
    window.resizable(False, False)
    MainWindow(window)
    window.mainloop()
    print("END")


if __name__ == '__main__':
    main()
