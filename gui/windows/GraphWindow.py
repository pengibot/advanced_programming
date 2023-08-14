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
        self.window.title("Graph")
        icon = tk.PhotoImage(file="gui/assets/graph.png")
        self.window.iconphoto(False, icon)

        fig = self.plot_graph()
        canvas = FigureCanvasTkAgg(fig, master=self.window)
        canvas_widget = canvas.get_tk_widget()
        canvas.draw()
        canvas_widget.grid(row=0, column=0, padx=10, pady=10)

    def plot_graph(self):

        # Real code below here

        fig, ax = plt.subplots(figsize=(10, 6), nrows=1, ncols=2)

        # Top Left

        # Code for Top Left Site Distribution per EID
        data = []
        for graph_data_item in self.graph_data_items:
            data.append([graph_data_item.eid, graph_data_item.site])
        columns = ["EID", "Site"]
        df = pd.DataFrame(data=data, columns=columns)

        value_counts = df["EID"].value_counts()
        unique_values = value_counts.index.tolist()
        ax[0].barh(unique_values, value_counts)
        ax[0].spines["right"].set_visible(False)
        ax[0].spines["top"].set_visible(False)
        ax[0].set_xlabel("Number of Sites", fontsize=8)
        ax[0].set_ylabel("EID", fontsize=8)
        # Setting x-axis to display only whole numbers
        ax[0].xaxis.set_major_locator(MultipleLocator(1))
        ax[0].set_title("Site Distribution per EID")

        # Top Right

        # Code for Top Left Site Distribution per EID
        data = []
        for graph_data_item in self.graph_data_items:
            data.append([graph_data_item.site, graph_data_item.freq])
        columns = ["Site", "Freq."]
        df = pd.DataFrame(data=data, columns=columns)

        ax[1].bar(df["Site"], df["Freq."])
        ax[1].spines["right"].set_visible(False)
        ax[1].spines["top"].set_visible(False)
        ax[1].set_xlabel("Site", fontsize=8)
        ax[1].set_ylabel("Freq.", fontsize=8)
        ax[1].set_xticklabels(df["Site"], rotation=90)
        ax[1].set_title("Freq. at each Site")

        plt.tight_layout()


        return fig


