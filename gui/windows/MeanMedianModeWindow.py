import tkinter as tk

from utils.LoggerFactory import LoggerFactory


class MeanMedianModeWindow:
    """
         Window to save the data set to a specific file.
    """

    data_manager = None

    def __init__(self, master, data_manager):
        self.data_manager = data_manager
        LoggerFactory.get_logger().info("Initialized Mean/Median/Mode Window")
        self.window = tk.Toplevel(master)  # Used to display dialog on top of Main Window
        self.window.configure(bg='white')
        self.window.grab_set()  # Grabs all events for the application
        self.window.title("Mean/Median/Mode")
        self.window.geometry("544x300")
        self.window.resizable(False, False)  # Prevent the user from resizing the window
        self.save_icon_image = tk.PhotoImage(file="gui/assets/mean_median_mode.png")
        self.window.iconphoto(False, self.save_icon_image)  # Add icon for dialog
        self.master = master

        # Using StringVar to set text values and retrieve them
        self.height = tk.StringVar()
        self.year = tk.StringVar()

        # Using StringVar to set text value to be able to retrieve
        self.mean_value = tk.StringVar()
        self.median_value = tk.StringVar()
        self.mode_value = tk.StringVar()

        # Created a frame to group components at the top of the dialog
        self.top_frame = tk.Frame(self.window, bg='white')

        # Adding Save image to top frame
        self.calculate_photo_image = tk.PhotoImage(file='gui/assets/mean_median_mode.png')
        self.image_label = tk.Label(self.top_frame, image=self.calculate_photo_image, bg='white')
        self.image_label.grid(row=0, column=0, padx=(20, 5))

        # Adding Instructions label to top frame
        self.instructions_label = tk.Label(self.top_frame,
                                           text="Producing the mean, median and mode for the 'In-Use ERP Total' from "
                                                "the extracted DAB multiplexes extracted earlier: C18A, C18F and C188",
                                           font=('Aerial', 11), anchor="w", justify="left", bg='white',
                                           wraplength=400)
        self.instructions_label.grid(row=0, column=1, columnspan=5, padx=(5, 10))

        # Adding description to height input
        self.height_description = tk.Label(self.top_frame, text="Height greater than:", font=('Aerial', 11),
                                           bg='white')
        self.height_description.grid(row=1, column=1)

        # Adding Entry component for height input
        self.height_text_entry = tk.Entry(self.top_frame, textvariable=self.height, width=10)
        self.height_text_entry.insert(0, "75")
        self.height_text_entry.grid(row=1, column=2)

        # Adding description to year input
        self.year_description = tk.Label(self.top_frame, text="Year from:", font=('Aerial', 11),
                                         bg='white')
        self.year_description.grid(row=1, column=3)

        # Adding Entry component for height input
        self.year_text_entry = tk.Entry(self.top_frame, textvariable=self.year, width=10)
        self.year_text_entry.insert(0, "2001")
        self.year_text_entry.grid(row=1, column=4)

        # Adding top frame to first row in grid
        self.top_frame.grid(row=0, column=0, sticky="NESW", pady=(10, 5))

        # Created a frame to group components at the middle of the dialog
        self.middle_frame = tk.Frame(self.window, bg='white')

        # Adding label for Mean Label
        self.mean_label = tk.Label(self.middle_frame, text="Mean", font=('Aerial', 20), bg='white')
        self.mean_label.grid(row=0, column=0)

        # Adding label for Median Label
        self.median_label = tk.Label(self.middle_frame, text="Median", font=('Aerial', 20), bg='white')
        self.median_label.grid(row=1, column=0)

        # Adding label for Mode Label
        self.mode_label = tk.Label(self.middle_frame, text="Mode", font=('Aerial', 20), bg='white')
        self.mode_label.grid(row=2, column=0)

        # Adding Entry component for file output (.json File)
        self.mean_entry = tk.Label(self.middle_frame, textvariable=self.mean_value, width=10, font=('Aerial', 20),
                                   bg='white')
        self.mean_entry.grid(row=0, column=1)

        # Adding Entry component for file output (.json File)
        self.median_entry = tk.Label(self.middle_frame, textvariable=self.median_value, width=10, font=('Aerial', 20),
                                     bg='white')
        self.median_entry.grid(row=1, column=1)

        # Adding Entry component for file output (.json File)
        self.mode_entry = tk.Label(self.middle_frame, textvariable=self.mode_value, width=10, font=('Aerial', 20),
                                   bg='white')
        self.mode_entry.grid(row=2, column=1)

        # Adding middle frame to second row in grid
        self.middle_frame.columnconfigure(0, weight=1)
        self.middle_frame.rowconfigure(0, weight=1)
        self.middle_frame.grid(row=1, column=0, sticky="NESW", pady=5, padx=(10, 10))

        # Created a frame to group components at the bottom of the dialog
        self.bottom_frame = tk.Frame(self.window, bg='white')

        # Adding Button component to exit dialog
        self.exit_button = tk.Button(self.bottom_frame, text="Exit", command=self.exit, padx=50, pady=5,
                                     bg='white')
        self.exit_button.grid(row=0, column=0)

        # Adding Button component to start calculation
        self.calculate_button = tk.Button(self.bottom_frame, text="Calculate", command=self.calculate, padx=50, pady=5,
                                          bg='white')
        self.calculate_button.grid(row=0, column=1)

        # Adding bottom frame to third row in grid
        self.bottom_frame.columnconfigure(0, weight=1)
        self.bottom_frame.rowconfigure(0, weight=1)
        self.bottom_frame.rowconfigure(1, weight=1)
        self.bottom_frame.grid(row=2, column=0, sticky="NESW", pady=20, padx=50)

    def calculate(self):
        """
            Action to start calculations
        """

        LoggerFactory.get_logger().info(f"Calculating Mean/Median/Mode")

        try:
            height_value = int(self.height.get())
        except ValueError as error:
            LoggerFactory.get_logger().info(
                f"Unable to convert {self.height.get()} to Height Value, defaulting to 75: {error}")
            height_value = 75

        try:
            year_value = int(self.year.get())
        except ValueError as error:
            LoggerFactory.get_logger().info(
                f"Unable to convert {self.year.get()} to Height Value, defaulting to 75: {error}")
            year_value = 2001

        mean, median, mode = self.data_manager.generate_data_for_in_use_erp_total(height_value, year_value)
        self.mean_value.set(mean)
        self.median_value.set(median)
        self.mode_value.set(mode)

    def exit(self):
        """
            Action to exit
        """

        LoggerFactory.get_logger().info("Exiting Mean/Median/Mode Window")
        self.window.destroy()
