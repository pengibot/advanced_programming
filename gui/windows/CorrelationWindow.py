import tkinter as tk

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from utils.LoggerFactory import LoggerFactory


class CorrelationWindow:
    """
        Displays a correlation matrix for a set of Data
        Freq., Block, Serv Label1, Serv Label2, Serv Label3, Serv Label4, Serv Label10
    """
    data_manager = None  # Reference to the Data Manager to query for Data

    def __init__(self, master, data_manager):
        self.data_manager = data_manager
        LoggerFactory.get_logger().info("Initialized Correlation Window")
        self.window = tk.Toplevel(master)  # Used to display dialog on top of Main Window
        self.window.configure(bg='white')
        self.window.grab_set()  # Grabs all events for the application
        self.window.title("Correlation")
        icon = tk.PhotoImage(file="gui/assets/correlation.png")
        self.window.iconphoto(False, icon)  # Add icon for dialog
        self.master = master

        # Created a frame to group components at the top of the dialog
        self.top_frame = tk.Frame(self.window, bg="white")
        self.top_frame.columnconfigure(0, weight=1)
        self.top_frame.rowconfigure(0, weight=1)

        # Adding Correlation image to top frame
        self.correlationImage = tk.PhotoImage(file='gui/assets/correlation.png')
        self.img_label = tk.Label(self.top_frame, image=self.correlationImage, anchor="w", justify="left", bg="white")
        self.img_label.image = self.correlationImage
        self.img_label.grid(row=0, column=0, padx=(20, 5), sticky='w')

        # Title to be shown at top of frame
        self.title = tk.Label(self.top_frame, text="Correlation Matrix",
                              font=('Aerial', 18), anchor="w", justify="left", bg="white")
        self.title.grid(row=0, column=1, padx=(5, 0), sticky='w')

        # Adding top frame to first row in grid
        self.top_frame.grid(row=0, column=0, sticky="w")

        self.frame = tk.Frame(self.window, bg='white')
        self.frame.grid(row=1, column=0)

        corr_matrix = self.creat_correlation_matrix()

        LoggerFactory.get_logger().info("Plotting Graph")
        figure = self.plot_graph(corr_matrix)  # Call to plot the graphs

        # Preparing Matplotlib figure to be embedded and displayed in Tkinter window
        canvas = FigureCanvasTkAgg(figure, master=self.window)
        canvas_widget = canvas.get_tk_widget()  # Extracting Tkinter Canvas widget

        LoggerFactory.get_logger().info("Drawing Canvas")
        canvas.draw()  # Renders the figure
        canvas_widget.grid(row=1, column=0, padx=(30, 0), pady=(5, 0))  # Assigning to Grid, giving some padding

        # Created a frame to group components at the bottom of the dialog
        self.bottom_frame = tk.Frame(self.window, bg='white')

        # Adding Button component to load files
        self.close_button = tk.Button(self.bottom_frame, text="Close", command=self.close_window, padx=50, pady=5)
        self.close_button.grid(row=0, column=0)

        # Adding bottom frame to third row in grid
        self.bottom_frame.columnconfigure(0, weight=1)
        self.bottom_frame.rowconfigure(0, weight=1)
        self.bottom_frame.grid(row=2, column=0, sticky="NESW", pady=(0, 20), padx=50)

    def creat_correlation_matrix(self):
        """
            Gets data from Data Manager and builds a correlation matrix
        """

        # Load the data to be correlated
        LoggerFactory.get_logger().info("Calling Data Manager to extract needed data")
        graph_data_items = self.data_manager.extract_graph_data()  # Returns list of GraphData items

        data_list = []  # Storing the data items
        for graph_data_item in graph_data_items:  # Looping over all items that are needed for the Pandas DataFrame
            data_list.append([graph_data_item.freq, graph_data_item.block, graph_data_item.serv_label_1,
                              graph_data_item.serv_label_2, graph_data_item.serv_label_3, graph_data_item.serv_label_4,
                              graph_data_item.serv_label_10])

        # Columns in the Data Frame
        columns = ["Freq.", "Block", "Serv Label1", "Serv Label2", "Serv Label3", "Serv Label4",
                   "Serv Label10"]

        # Creating new DataFrame with a subset of the data inside it
        LoggerFactory.get_logger().info("Creating Pandas DataFrame of data to be correlated")
        data = pd.DataFrame(data=data_list, columns=columns)

        LoggerFactory.get_logger().info("Cleaning Data")
        data_cleaned = self.clean_data(data)  # Call to method which cleans the data

        # Calculate the correlation matrix
        LoggerFactory.get_logger().info("Creating Correlation Matrix")
        correlation_matrix = data_cleaned.corr()  # Call to pandas function which creates a correlation matrix

        return correlation_matrix  # Return Correlation Data to be displayed in a graph

    def clean_data(self, data):
        """
            Responsible for cleaning the Pandas DataFrame
            Drops data which has NaN numbers in
            Creates category codes for non-numeric data
        """

        # Drop the rows with missing values
        LoggerFactory.get_logger().info("Cleaning NaN values")
        data_cleaned = data.dropna()
        # Assigning codes to string categories in order to create a correlation Matrix
        LoggerFactory.get_logger().info("Creating Category codes for DataFrame non numeric items")
        data_cleaned["Block"] = data_cleaned["Block"].astype("category").cat.codes
        data_cleaned["Serv Label1"] = data_cleaned["Serv Label1"].astype("category").cat.codes
        data_cleaned["Serv Label2"] = data_cleaned["Serv Label2"].astype("category").cat.codes
        data_cleaned["Serv Label3"] = data_cleaned["Serv Label3"].astype("category").cat.codes
        data_cleaned["Serv Label4"] = data_cleaned["Serv Label4"].astype("category").cat.codes
        data_cleaned["Serv Label10"] = data_cleaned["Serv Label10"].astype("category").cat.codes

        return data_cleaned  # Returning cleaned data

    def plot_graph(self, correlation_matrix):
        """
            Given the Correlation Matrix, it plots the data given
        """

        # Create a new figure for the plot
        figure, axes = plt.subplots(figsize=(5, 5))

        # Create a colormap
        cmap = mpl.colormaps['coolwarm']  # Using a colour map to accentuate the correlation between values

        # Create a mask for the diagonal (where variables are compared with themselves)
        mask = np.eye(correlation_matrix.shape[0], dtype=bool)

        # Apply the mask to the correlation matrix
        masked_corr_matrix = np.ma.array(correlation_matrix, mask=mask)

        # Create a matrix plot
        correlation_matrix_axes = axes.matshow(masked_corr_matrix, cmap=cmap)

        # Create colour bar
        figure.colorbar(correlation_matrix_axes, label='Correlation coefficient')

        # Show the plot with labels
        plt.xticks(np.arange(len(correlation_matrix.columns)), correlation_matrix.columns, rotation=90)
        plt.yticks(np.arange(len(correlation_matrix.columns)), correlation_matrix.columns)

        # Add text to each cell
        for (i, j), z in np.ndenumerate(masked_corr_matrix):
            if ~np.ma.getmask(masked_corr_matrix)[i, j]:  # Only add text to cells that are not masked
                axes.text(j, i, '{:0.2f}'.format(z), ha='center', va='center')

        # Set title
        plt.title('Correlation Matrix of Selected Variables', pad=90)

        return figure  # return figure to be displayed on canvas

    def close_window(self):
        """
            Action to close Correlation Window
        """
        LoggerFactory.get_logger().info("Closing Correlation Window")
        self.window.destroy()
