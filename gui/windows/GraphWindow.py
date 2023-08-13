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

        result = self.data_manager.extract_graph_data()
        print(result)

    def plot_graph(self):

        data = []

        for graph_data_item in  self.graph_data_items:
            data.append([graph_data_item.eid, graph_data_item.site])

        columns = ["EID", "Site"]

        df = pd.DataFrame(data=data, columns=columns)

        # Real code below here

        fig, ax = plt.subplots(figsize=(6, 4))

        value_counts = df["EID"].value_counts()
        unique_values = value_counts.index.tolist()

        ax.barh(unique_values, value_counts)
        ax.spines["right"].set_visible(False)
        ax.spines["top"].set_visible(False)
        ax.set_xlabel("Number of Sites", fontsize=12)
        ax.set_ylabel("EID", fontsize=12)
        # Setting x-axis to display only whole numbers
        ax.xaxis.set_major_locator(MultipleLocator(1))

        fig.text(.15, .9, "Site Distribution per EID", fontsize=15)

        return fig


