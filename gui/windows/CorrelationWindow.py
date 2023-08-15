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

        # Load the data
        graph_data_items = self.data_manager.extract_graph_data()

        data_list = []

        for graph_data_item in graph_data_items:
            data_list.append([graph_data_item.freq, graph_data_item.block, graph_data_item.serv_label_1,
                              graph_data_item.serv_label_2, graph_data_item.serv_label_3, graph_data_item.serv_label_4,
                              graph_data_item.serv_label_10])

        columns = ["Freq.", "Block", "Serv Label1", "Serv Label2", "Serv Label3", "Serv Label4",
                   "Serv Label10"]
        data = pd.DataFrame(data=data_list, columns=columns)

        # Drop the rows with missing values
        data_cleaned = data.dropna()

        data_cleaned["Block"] = data_cleaned["Block"] .astype("category").cat.codes
        data_cleaned["Serv Label1"] = data_cleaned["Serv Label1"] .astype("category").cat.codes
        data_cleaned["Serv Label2"] = data_cleaned["Serv Label2"] .astype("category").cat.codes
        data_cleaned["Serv Label3"] = data_cleaned["Serv Label3"] .astype("category").cat.codes
        data_cleaned["Serv Label4"] = data_cleaned["Serv Label4"] .astype("category").cat.codes
        data_cleaned["Serv Label10"] = data_cleaned["Serv Label10"] .astype("category").cat.codes

        # Calculate the correlation matrix
        corr_matrix = data_cleaned.corr()

        # Create a new figure for the plot
        fig, ax = plt.subplots(figsize=(5, 5))

        # Create a colormap
        cmap = mpl.colormaps['coolwarm']

        # Create a mask for the diagonal (where variables are compared with themselves)
        mask = np.eye(corr_matrix.shape[0], dtype=bool)

        # Apply the mask to the correlation matrix
        masked_corr_matrix = np.ma.array(corr_matrix, mask=mask)

        # Create a matrix plot
        cax = ax.matshow(masked_corr_matrix, cmap=cmap)

        # Create colour bar
        fig.colorbar(cax, label='Correlation coefficient')

        # Show the plot with labels
        plt.xticks(np.arange(len(corr_matrix.columns)), corr_matrix.columns, rotation=90)
        plt.yticks(np.arange(len(corr_matrix.columns)), corr_matrix.columns)

        # Add text to each cell
        for (i, j), z in np.ndenumerate(masked_corr_matrix):
            if ~np.ma.getmask(masked_corr_matrix)[i, j]:  # Only add text to cells that are not masked
                ax.text(j, i, '{:0.2f}'.format(z), ha='center', va='center')

        # Set title
        plt.title('Correlation Matrix of Selected Variables', pad=90)


        # Display the plot in the Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=self.window)
        canvas.draw()
        canvas.get_tk_widget().grid(row=1, column=0, padx=(30, 0), pady=(5, 0))

        self.bottom_frame = tk.Frame(self.window, bg='white')

        self.close_button = tk.Button(self.bottom_frame, text="Close", command=self.window.destroy, padx=50, pady=5)
        self.close_button.grid(row=0, column=0)

        self.bottom_frame.columnconfigure(0, weight=1)
        self.bottom_frame.rowconfigure(0, weight=1)
        self.bottom_frame.grid(row=2, column=0, sticky="NESW", pady=(0, 20), padx=50)
