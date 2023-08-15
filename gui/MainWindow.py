import tkinter as tk
from tkinter import scrolledtext

from business_logic.DataManager import DataManager
from gui.windows.CorrelationWindow import CorrelationWindow
from gui.windows.GraphWindow import GraphWindow
from gui.windows.ImportCSVFilesWindow import ImportCSVFilesWindow
from gui.windows.LoadDataSetWindow import LoadDataSetWindow
from gui.windows.MeanMedianModeWindow import MeanMedianModeWindow
from gui.windows.SaveDataSetWindow import SaveDataSetWindow

from utils import LoggerFactory
from utils import TextHandler


class MainWindow:
    """
        Main window that will allow the user to load certain functions and see the logs
    """

    # Flag that gets set to true once a dataset is successfully loaded, to enable/disable buttons
    data_manager = DataManager()

    def __init__(self, master):
        # Setting master window to be able to navigate
        self.master = master
        self.master.configure(bg='white')

        # Frame to hold logs
        logs_frame = tk.LabelFrame(self.master, text="Log", bg='white')
        logs_frame.columnconfigure(0, weight=1)
        logs_frame.rowconfigure(0, weight=1)
        logs_frame.grid(row=0, column=0, padx=5, sticky="NESW")

        # Component to hold logs visible to the user
        self.scrolled_text = scrolledtext.ScrolledText(logs_frame, wrap=tk.WORD, width=60, height=20, borderwidth=0,
                                                       font="Arial 10")
        self.scrolled_text.grid(column=0, row=0, sticky="NESW")

        # Create a Text Handler to display logs to the user and add it to the Logger
        logs_scrolled_text_handler = TextHandler(self.scrolled_text)
        LoggerFactory.get_logger().addHandler(logs_scrolled_text_handler)

        # Frame to hold buttons to load up different Functions
        functions_frame = tk.LabelFrame(self.master, text='Functions', bg='white')
        functions_frame.grid(row=0, column=1, pady=5, padx=10, sticky=tk.E)

        # Create button and set command to Import CSV Files
        self.import_csv_files_button = tk.Button(functions_frame, text='Load & Clean Data Set', width=25, pady=5,
                                                 command=self.initialize_import_csv_files_window)
        self.import_csv_files_button.grid(row=0, column=0, pady=7.5, padx=7.5)

        # Create button and set command to Load Data Sets
        self.load_data_set_button = tk.Button(functions_frame, text='Load Prepared Data Set', width=25, pady=5,
                                              command=self.initialize_load_data_set_window)
        self.load_data_set_button.grid(row=1, column=0, pady=7.5, padx=7.5)

        # Create button and set command to Save Data Set
        self.save_data_set_button = tk.Button(functions_frame, text='Save Data Set', width=25, pady=5,
                                              command=self.initialize_save_data_set_window)
        self.save_data_set_button.grid(row=2, column=0, pady=7.5, padx=7.5)

        # Create button and set command to display Mean/Median/Mode
        self.load_mean_median_mode_button = tk.Button(functions_frame, text='Mean/Mode/Median', width=25, pady=5,
                                                      command=self.initialize_mean_median_mode_window)
        self.load_mean_median_mode_button.grid(row=3, column=0, pady=7.5, padx=7.5)

        # Create button and set command to Display Graph
        self.display_graph_button = tk.Button(functions_frame, text='Display Graph', width=25, pady=5,
                                              command=self.initialize_graph_window)
        self.display_graph_button.grid(row=4, column=0, pady=7.5, padx=7.5)

        # Create button and set command to Display Correlation
        self.display_correlation_button = tk.Button(functions_frame, text='Display Correlation', width=25, pady=5,
                                                    command=self.initialize_correlation_window)
        self.display_correlation_button.grid(row=5, column=0, pady=10, padx=(7.5, 0))

        self.set_state_of_buttons()

    def set_state_of_buttons(self):
        """
            Method that will allow/disallow certain action based on whether the DataSet has been loaded
        """

        # Check if the data set has been loaded
        dataset_loaded = self.data_manager.get_data_frame() is not None

        LoggerFactory.get_logger().debug(f"Setting buttons state to {'normal' if dataset_loaded else 'disabled'}")
        # Setting the state of buttons that should only be enabled when there is data to act upon
        self.save_data_set_button["state"] = "normal" if dataset_loaded else "disabled"
        self.load_mean_median_mode_button["state"] = "normal" if dataset_loaded else "disabled"
        self.display_graph_button["state"] = "normal" if dataset_loaded else "disabled"
        self.display_correlation_button["state"] = "normal" if dataset_loaded else "disabled"

    def initialize_import_csv_files_window(self):
        """
            Action used to load the Import CSV Files Window
        """

        LoggerFactory.get_logger().info("Initializing Import CSV Files Window")
        ImportCSVFilesWindow(self.master, self.data_manager, self.set_state_of_buttons)

    def initialize_load_data_set_window(self):
        """
            Action used to load the Data Set Window
        """

        LoggerFactory.get_logger().info("Initializing Load Data Set Window")
        LoadDataSetWindow(self.master, self.data_manager, self.set_state_of_buttons)
        self.set_state_of_buttons()

    def initialize_save_data_set_window(self):
        """
            Action used to load the Save Data Set Window
        """

        LoggerFactory.get_logger().info("Initializing Save Data Set Window")
        SaveDataSetWindow(self.master, self.data_manager)

    def initialize_mean_median_mode_window(self):
        """
            Action used to load the Mean/Median/Mode Window
        """

        LoggerFactory.get_logger().info("Initializing Mean/Median/Mode Window")
        MeanMedianModeWindow(self.master, self.data_manager)

    def initialize_graph_window(self):
        """
            Action used to load the Graph Window
        """

        LoggerFactory.get_logger().info("Initializing Graph Window")
        GraphWindow(self.master, self.data_manager)

    def initialize_correlation_window(self):
        """
            Action used to load the Correlation Window
        """

        LoggerFactory.get_logger().info("Initializing correlation window")
        CorrelationWindow(self.master, self.data_manager)
