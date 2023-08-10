import tkinter as tk
from tkinter import filedialog, Label, PhotoImage

from LoggerFactory import LoggerFactory


class LoadDataSetWindow:
    """
        Window to load in the data sets. It is responsible for validating the files
    """

    # TODO: Add Validation of files to ensure they can be parsed.

    def __init__(self, master=None):
        LoggerFactory.get_logger().info("Initialized Load Data Set Window")
        self.window = tk.Toplevel(master)  # Used to display dialog on top of Main Window
        self.window.grab_set()  # Grabs all events for the application
        self.window.configure(bg='white')
        self.window.title("Load Data Set")
        self.window.geometry("544x271")
        self.window.resizable(False, False)  # Prevent the user from resizing the window
        self.photo = tk.PhotoImage(file="images/Load.png")
        self.window.iconphoto(False, self.photo)  # Add icon for dialog
        self.master = master

        # Using StringVar to set text values and retrieve them
        self.filepath1 = tk.StringVar()
        self.filepath2 = tk.StringVar()

        # Created a frame to group components at the top of the dialog
        self.top_frame = tk.Frame(self.window, bg='white')

        # Adding Load image to top frame
        self.load_image = PhotoImage(file='images/Load.png')
        self.image_label = Label(self.top_frame, image=self.load_image, bg='white')
        self.image_label.grid(row=0, column=0, padx=(20, 5))

        # Adding Instructions label to top frame
        self.instructions_label = tk.Label(self.top_frame,
                                           text="Select the two files with data on the broadcast info and\ntransmitter "
                                                "info. They must both be .csv files.",
                                           font=('Aerial', 11), anchor="w", justify="left", bg='white')
        self.instructions_label.grid(row=0, column=1, padx=(5, 0))

        # Adding top frame to first row in grid
        self.top_frame.grid(row=0, column=0, sticky="NESW", pady=10, padx=(10, 0))

        # Created a frame to group components at the middle of the dialog
        self.middle_frame = tk.Frame(self.window, bg='white')

        # Adding description to file 1 input (Broadcast Info File)
        self.file_1_description = tk.Label(self.middle_frame, text="Broadcast Info File:", font=('Aerial', 11),
                                           bg='white')
        self.file_1_description.grid(row=0, column=0)

        # Adding Entry component for file 1 input (Broadcast Info File)
        self.file_1_text_entry = tk.Entry(self.middle_frame, textvariable=self.filepath1, width=55)
        self.file_1_text_entry.grid(row=0, column=1)

        # Adding Button component to select file 1 input (Broadcast Info File)
        self.folder_image_1 = PhotoImage(file='images/Folder.png')
        self.load_file_1_button = tk.Button(self.middle_frame, image=self.folder_image_1, command=self.select_file_1,
                                            borderwidth=0,
                                            highlightthickness=0, bg='white')
        self.load_file_1_button.image = self.folder_image_1
        self.load_file_1_button.grid(row=0, column=2, padx=5, pady=10)

        # Adding description to file 2 input (Transmitter Info File)
        self.file_2_description = tk.Label(self.middle_frame, text="Transmitter Info File:", font=('Aerial', 11),
                                           bg='white')
        self.file_2_description.grid(row=1, column=0)

        # Adding Entry component for file 2 input (Transmitter Info File)
        self.file_2_text_entry = tk.Entry(self.middle_frame, textvariable=self.filepath2, width=55)
        self.file_2_text_entry.grid(row=1, column=1)

        # Adding Button component to select file 2 input (Transmitter Info File)
        self.folder_image_2 = PhotoImage(file='images/Folder.png')
        self.load_file_2_button = tk.Button(self.middle_frame, image=self.folder_image_2, command=self.select_file_2,
                                            borderwidth=0,
                                            highlightthickness=0, bg='white')
        self.load_file_2_button.image = self.folder_image_2
        self.load_file_2_button.grid(row=1, column=2, padx=5)

        # Adding middle frame to second row in grid
        self.middle_frame.columnconfigure(0, weight=1)
        self.middle_frame.rowconfigure(0, weight=1)
        self.middle_frame.rowconfigure(1, weight=1)
        self.middle_frame.grid(row=1, column=0, sticky="NESW", pady=10, padx=(10, 0))

        # Created a frame to group components at the bottom of the dialog
        self.bottom_frame = tk.Frame(self.window, bg='white')

        # Adding Button component to cancel dialog
        self.cancel_button = tk.Button(self.bottom_frame, text="Cancel", command=self.cancel, padx=50, pady=5)
        self.cancel_button.grid(row=0, column=0)

        # Adding Button component to load files
        self.load_button = tk.Button(self.bottom_frame, text="Load", command=self.load, padx=50, pady=5)
        self.load_button.grid(row=0, column=1)

        # Adding bottom frame to third row in grid
        self.bottom_frame.columnconfigure(0, weight=1)
        self.bottom_frame.rowconfigure(0, weight=1)
        self.bottom_frame.rowconfigure(1, weight=1)
        self.bottom_frame.grid(row=2, column=0, sticky="NESW", pady=20, padx=50)

    def select_file_1(self):
        """
            Action to select file 1 and set the filepath
        """
        filename = filedialog.askopenfilename()
        LoggerFactory.get_logger().info(f"Selected files 1 as {filename}")
        self.filepath1.set(filename)

    def select_file_2(self):
        """
            Action to select file 2 and set the filepath
        """
        filename = filedialog.askopenfilename()
        LoggerFactory.get_logger().info(f"Selected file 2 as {filename}")
        self.filepath2.set(filename)

    def load(self):
        """
            Action to load both files, perform validation TODO: Perform validation here
        """
        LoggerFactory.get_logger().info(f"Loading file 1 as {self.filepath1.get()}")
        LoggerFactory.get_logger().info(f"Loading file 2 as {self.filepath2.get()}")
        self.window.destroy()

    def cancel(self):
        """
            Action to cancel loading files
        """
        LoggerFactory.get_logger().info("Cancelling Load Data Set Window")
        self.window.destroy()
