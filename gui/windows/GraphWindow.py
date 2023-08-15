import tkinter as tk

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import MultipleLocator

from utils.LoggerFactory import LoggerFactory


class GraphWindow:
    """
        Responsible for displaying multiple graphs
        Bar chart, Site Distribution per EID
        Column chart, Freq. at each Site
    """

    data_manager = None  # Used to retrieve relevant data to be shown in Graphs
    graph_data_items = None  # Holds the data needed to display the Graphs

    def __init__(self, master, data_manager):
        self.data_manager = data_manager
        # Calling DataManager to extract needed Graph Data
        LoggerFactory.get_logger().info("Requesting graph data from Data Manager")
        self.graph_data_items = self.data_manager.extract_graph_data()
        LoggerFactory.get_logger().info("Initialized Graph Window")
        self.window = tk.Toplevel(master)  # Constructs a top level widget from the master
        self.window.title("Graph")
        self.window.grab_set()  # Grabs all events for the application
        icon = tk.PhotoImage(file="gui/assets/graph.png")
        self.window.iconphoto(False, icon)  # Adding icon to Window

        LoggerFactory.get_logger().info("Plotting Graph")
        figure = self.plot_graph()  # Call to plot the graphs

        # Preparing Matplotlib figure to be embedded and displayed in Tkinter window
        canvas = FigureCanvasTkAgg(figure, master=self.window)
        canvas_widget = canvas.get_tk_widget()  # Extracting Tkinter Canvas widget

        LoggerFactory.get_logger().info("Drawing Canvas")
        canvas.draw()  # Renders the figure
        canvas_widget.grid(row=0, column=0, padx=10, pady=10)  # Assigning to Grid, giving some padding

    def plot_graph(self):
        """
            Responsible for plotting the Graphs using a matrix
        """

        # Setup Figure size, specifying rows and columns
        LoggerFactory.get_logger().info("Creating figure and axes")
        figure, axes = plt.subplots(figsize=(10, 6), nrows=1, ncols=2)

        # Code for Top Left Site Distribution per EID
        LoggerFactory.get_logger().info("Creating Site Distribution per EID Graph")

        data = []
        for graph_data_item in self.graph_data_items:  # Looping through the graph data
            data.append([graph_data_item.eid, graph_data_item.site])  # Assigning data values to list

        # Columns to be displayed in the Graph
        columns = ["EID", "Site"]

        # Creating the Panda Data Frame
        df = pd.DataFrame(data=data, columns=columns)

        # Setting the axes values
        value_counts = df["EID"].value_counts()
        unique_values = value_counts.index.tolist()
        axes[0].barh(unique_values, value_counts)  # Specifying a horizontal bar chart
        # Removing top and right spines
        axes[0].spines["right"].set_visible(False)
        axes[0].spines["top"].set_visible(False)
        # Setting the axes labels
        axes[0].set_xlabel("Number of Sites", fontsize=8)
        axes[0].set_ylabel("EID", fontsize=8)
        axes[0].xaxis.set_major_locator(MultipleLocator(1))  # Setting x-axis to display only whole numbers
        axes[0].set_title("Site Distribution per EID")

        # Code for Top Right Freq. at each Site
        LoggerFactory.get_logger().info("Creating Freq. at each Site Graph")

        data = []
        for graph_data_item in self.graph_data_items:  # Looping through the graph data
            data.append([graph_data_item.site, graph_data_item.freq])  # Assigning data values to list

        # Columns to be displayed in the Graph
        columns = ["Site", "Freq."]

        # Creating the Panda Data Frame
        df = pd.DataFrame(data=data, columns=columns)

        # Setting the axes values
        axes[1].bar(df["Site"], df["Freq."])  # Specifying a vertical (default) bar chart
        # Removing top and right spines
        axes[1].spines["right"].set_visible(False)
        axes[1].spines["top"].set_visible(False)
        # Setting the axes labels
        axes[1].set_xlabel("Site", fontsize=8)
        axes[1].set_ylabel("Freq.", fontsize=8)
        axes[1].set_xticks(df["Site"])  # Need to set before adding a label to avoid warnings
        axes[1].set_xticklabels(df["Site"], rotation=90)  # Rotate labels so they do not cross over each other
        axes[1].set_title("Freq. at each Site")

        # Automatically adjusts the parameters of the plot to minimize the padding
        plt.tight_layout()

        LoggerFactory.get_logger().info("Finished creating graphs")

        # returning figure to be displayed on canvas
        return figure
