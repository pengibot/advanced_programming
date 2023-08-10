import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

from LoggerFactory import LoggerFactory


class CorrelationWindow:
    def __init__(self, master=None):
        LoggerFactory.get_logger().info("Initialized Correlation Window")
        self.window = tk.Toplevel(master)
        self.window.configure(bg='white')
        self.window.grab_set()
        self.window.title("Correlation")
        icon = tk.PhotoImage(file="images/Correlation.png")
        self.window.iconphoto(False, icon)
        self.master = master

        self.tf = tk.Frame(self.window, bg="white")
        self.tf.columnconfigure(0, weight=1)
        self.tf.rowconfigure(0, weight=1)

        self.correlationImage = tk.PhotoImage(file='images/Correlation.png')
        self.img_label = tk.Label(self.tf, image=self.correlationImage, anchor="w", justify="left", bg="white")
        self.img_label.image = self.correlationImage
        self.img_label.grid(row=0, column=0, padx=(20, 5), sticky='w')

        self.label1 = tk.Label(self.tf, text="Correlation Matrix",
                               font=('Aerial', 18), anchor="w", justify="left", bg="white")
        self.label1.grid(row=0, column=1, padx=(5, 0), sticky='w')

        self.tf.grid(row=0, column=0, sticky="w")

        self.frame = tk.Frame(self.window, bg='white')
        # self.frame.pack(fill=tk.BOTH, expand=1)
        self.frame.grid(row=1, column=0)

        # Load the data
        data = pd.read_csv('TESTING1.csv')

        # Select the columns of interest
        columns_of_interest = ["Freq.", "Block", "Serv Label1", "Serv Label2", "Serv Label3", "Serv Label4",
                               "Serv Label10"]
        data_subset = data[columns_of_interest]

        # Drop the rows with missing values
        data_subset_clean = data_subset.dropna()

        # Calculate the correlation matrix
        corr_matrix = data_subset_clean.corr()

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

        # Show the plot
        # plt.show()
        # Display the plot in the Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=self.window)
        canvas.draw()
        canvas.get_tk_widget().grid(row=1, column=0, padx=(30, 0), pady=(5, 0))

        self.bf = tk.Frame(self.window, bg='white')

        self.close_button = tk.Button(self.bf, text="Close", command=self.window.destroy, padx=50, pady=5)
        self.close_button.grid(row=0, column=0)

        self.bf.columnconfigure(0, weight=1)
        self.bf.rowconfigure(0, weight=1)
        self.bf.grid(row=2, column=0, sticky="NESW", pady=(0, 20), padx=50)
