import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from utils.LoggerFactory import LoggerFactory


class GraphWindow:
    def __init__(self, master, data_manager):
        LoggerFactory.get_logger().info("Initialized Graph Window")
        self.window = tk.Toplevel(master)
        self.window.grab_set()
        self.window.title("Graph")
        icon = tk.PhotoImage(file="gui/assets/graph.png")
        self.window.iconphoto(False, icon)

        import matplotlib.pyplot as plt

        fig = self.plot_graph()
        canvas = FigureCanvasTkAgg(fig, master=self.window)
        canvas_widget = canvas.get_tk_widget()
        canvas.draw()
        canvas_widget.grid(row=0, column=0, padx=10, pady=10)

    def plot_graph(self):
        # Sample data
        x = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        y = np.array([1, 4, 2, 8, 6, 3, 5, 8, 7, 9])

        # Create a figure and axis
        fig, ax = plt.subplots(figsize=(5, 4))

        # Plot data
        ax.plot(x, y, '-b', label='Data Series', marker='o')
        ax.set_title('Sample Data Plot')
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Distance (m)')
        ax.grid(True)
        ax.legend()

        return fig


