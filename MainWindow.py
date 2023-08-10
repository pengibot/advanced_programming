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
    """
        Main window that will allow the user to load certain functions and see the logs
    """

    def __init__(self, master=None):
        LoggerFactory.get_logger().info("Starting Application")

        # Setting master window to be able to navigate
        self.master = master
        self.master.configure(bg='white')

        # Frame to hold logs
        logs_frame = tk.LabelFrame(self.master, text="Log", bg='white')
        logs_frame.columnconfigure(0, weight=1)
        logs_frame.rowconfigure(0, weight=1)
        logs_frame.grid(row=0, column=0, padx=5, sticky="NESW")

        # Component to hold logs visible to the user
        self.scrolled_text = scrolledtext.ScrolledText(logs_frame, wrap=tk.WORD, width=42, height=17, borderwidth=0)
        self.scrolled_text.grid(column=0, row=0, sticky="NESW")

        # Create a Text Handler to display logs to the user and add it to the Logger
        logs_scrolled_text_handler = TextHandler(self.scrolled_text)
        LoggerFactory.get_logger().addHandler(logs_scrolled_text_handler)

        # Frame to hold buttons to load up different Functions
        functions_frame = tk.LabelFrame(self.master, text='Functions', bg='white')
        functions_frame.grid(row=0, column=1, pady=5, padx=10, sticky=tk.E)

        # Create button and set command to Load Data Set
        self.load_data_set_button = tk.Button(functions_frame, text='Load Data Set', width=25, pady=5,
                                              command=self.initialize_load_data_set_window)
        self.load_data_set_button.grid(row=0, column=0, pady=7.5, padx=7.5)

        # Create button and set command to Save Data Set
        self.save_data_set_button = tk.Button(functions_frame, text='Save Data Set', width=25, pady=5,
                                              command=self.initialize_save_data_set_window)
        self.save_data_set_button.grid(row=1, column=0, pady=7.5, padx=7.5)

        # Create button and set command to display Mean/Median/Mode
        self.load_mean_median_mode_button = tk.Button(functions_frame, text='Mean/Mode/Median', width=25, pady=5,
                                                      command=self.initialize_mean_median_mode_window)
        self.load_mean_median_mode_button.grid(row=2, column=0, pady=7.5, padx=7.5)

        # Create button and set command to Display Graph
        self.display_graph_button = tk.Button(functions_frame, text='Display Graph', width=25, pady=5,
                                              command=self.initialize_graph_window)
        self.display_graph_button.grid(row=3, column=0, pady=7.5, padx=7.5)

        # Create button and set command to Display Correlation
        self.display_correlation_button = tk.Button(functions_frame, text='Display Correlation', width=25, pady=5,
                                                    command=self.initialize_correlation_window)
        self.display_correlation_button.grid(row=4, column=0, pady=10, padx=(7.5, 0))

    def initialize_load_data_set_window(self):
        """
            Action used to load the Data Set Window
        """

        LoggerFactory.get_logger().info("Initializing Load Data Set Window")
        LoadDataSetWindow(self.master)

    def initialize_save_data_set_window(self):
        """
            Action used to load the Save Data Set Window
        """

        LoggerFactory.get_logger().info("Initializing Save Data Set Window")
        SaveDataSetWindow(self.master)

    def initialize_mean_median_mode_window(self):
        """
            Action used to load the Mean/Median/Mode Window
        """

        LoggerFactory.get_logger().info("Initializing Mean/Median/Mode Window")
        MeanMedianModeWindow(self.master)

    def initialize_graph_window(self):
        """
            Action used to load the Graph Window
        """

        LoggerFactory.get_logger().info("Initializing Graph Window")
        GraphWindow(self.master)

    def initialize_correlation_window(self):
        """
            Action used to load the Correlation Window
        """

        LoggerFactory.get_logger().info("Initializing correlation window")
        CorrelationWindow(self.master)


def main():
    window = tk.Tk()
    window.configure(bg='white')
    window.title("Advanced Programming")
    window.geometry("593x300")
    window.resizable(False, False)
    photo = tk.PhotoImage(file ="images/Logo.png")
    window.iconphoto(False, photo)
    MainWindow(window)
    window.mainloop()
    LoggerFactory.get_logger().info("Exiting Application")


if __name__ == '__main__':
    main()
