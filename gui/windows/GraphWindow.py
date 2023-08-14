import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import MultipleLocator

from utils.LoggerFactory import LoggerFactory


class GraphWindow:

    data_manager = None
    graph_data_items = None

    def __init__(self, master, data_manager):
        self.data_manager = data_manager
        self.graph_data_items = self.data_manager.extract_graph_data()
        LoggerFactory.get_logger().info("Initialized Graph Window")
        self.window = tk.Toplevel(master)
        # self.window.grab_set()
        self.window.title("Graph")
        icon = tk.PhotoImage(file="gui/assets/graph.png")
        self.window.iconphoto(False, icon)

        fig = self.plot_graph()
        canvas = FigureCanvasTkAgg(fig, master=self.window)
        canvas_widget = canvas.get_tk_widget()
        canvas.draw()
        canvas_widget.grid(row=0, column=0, padx=10, pady=10)

    def plot_graph(self):

        data = []

        for graph_data_item in  self.graph_data_items:
            data.append([graph_data_item.eid, graph_data_item.site])

        columns = ["EID", "Site"]

        df = pd.DataFrame(data=data, columns=columns)

        # Real code below here

        fig, ax = plt.subplots(figsize=(10, 10), nrows=2, ncols=2)

        value_counts = df["EID"].value_counts()
        unique_values = value_counts.index.tolist()
        # Top Left
        ax[0, 0].barh(unique_values, value_counts)
        ax[0, 0].spines["right"].set_visible(False)
        ax[0, 0].spines["top"].set_visible(False)
        ax[0, 0].set_xlabel("Number of Sites", fontsize=8)
        ax[0, 0].set_ylabel("EID", fontsize=8)
        # Setting x-axis to display only whole numbers
        ax[0, 0].xaxis.set_major_locator(MultipleLocator(1))
        ax[0, 0].set_title("Site Distribution per EID")

        # Top Right
        ax[0, 1].barh(unique_values, value_counts)
        ax[0, 1].spines["right"].set_visible(False)
        ax[0, 1].spines["top"].set_visible(False)
        ax[0, 1].set_xlabel("Number of Sites", fontsize=8)
        ax[0, 1].set_ylabel("EID", fontsize=8)
        # Setting x-axis to display only whole numbers
        ax[0, 1].xaxis.set_major_locator(MultipleLocator(1))
        ax[0, 1].set_title("Graph 2")

        # Bottom Left
        ax[1, 0].barh(unique_values, value_counts)
        ax[1, 0].spines["right"].set_visible(False)
        ax[1, 0].spines["top"].set_visible(False)
        ax[1, 0].set_xlabel("Number of Sites", fontsize=8)
        ax[1, 0].set_ylabel("EID", fontsize=8)
        # Setting x-axis to display only whole numbers
        ax[1, 0].xaxis.set_major_locator(MultipleLocator(1))
        ax[1, 0].set_title("Graph 3")

        # Bottom Right
        ax[1, 1].barh(unique_values, value_counts)
        ax[1, 1].spines["right"].set_visible(False)
        ax[1, 1].spines["top"].set_visible(False)
        ax[1, 1].set_xlabel("Number of Sites", fontsize=8)
        ax[1, 1].set_ylabel("EID", fontsize=8)
        # Setting x-axis to display only whole numbers
        ax[1, 1].xaxis.set_major_locator(MultipleLocator(1))
        ax[1, 1].set_title("Graph 4")

        return fig


