import tkinter as tk
from tkinter import filedialog, Label, PhotoImage, messagebox

from utils.LoggerFactory import LoggerFactory


class ImportCSVFilesWindow:
    """
        Window to import the CSV files. It is responsible for validating the files
    """

    data_manager = None
    set_state_of_buttons = None

    def __init__(self, master, data_manager, set_state_of_buttons):
        self.data_manager = data_manager
        # function that will allow the MainWindow to enable buttons once there is a DataFrame to act upon
        self.set_state_of_buttons = set_state_of_buttons
        LoggerFactory.get_logger().info("Initialized Import CSV Files Window")
        self.window = tk.Toplevel(master)  # Used to display dialog on top of Main Window
        self.window.grab_set()  # Grabs all events for the application
        self.window.configure(bg='white')
        self.window.title("Import CSV Files")
        self.window.geometry("544x271")
        self.window.resizable(False, False)  # Prevent the user from resizing the window
        self.import_photo_image = tk.PhotoImage(file="gui/assets/import.png")
        self.window.iconphoto(False, self.import_photo_image)  # Add icon for dialog
        self.master = master

        # Using StringVar to set text values and retrieve them
        self.file_path_1 = tk.StringVar()
        self.file_path_2 = tk.StringVar()

        # Created a frame to group components at the top of the dialog
        self.top_frame = tk.Frame(self.window, bg='white')

        # Adding Import image to top frame
        self.import_image = PhotoImage(file='gui/assets/import.png')
        self.image_label = Label(self.top_frame, image=self.import_image, bg='white')
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
        self.file_1_text_entry = tk.Entry(self.middle_frame, textvariable=self.file_path_1, width=55)
        self.file_1_text_entry.grid(row=0, column=1)

        # Adding Button component to select file 1 input (Broadcast Info File)
        self.folder_image_1 = PhotoImage(file='gui/assets/folder.png')
        self.import_file_1_button = tk.Button(self.middle_frame, image=self.folder_image_1, command=self.select_file_1,
                                              borderwidth=0,
                                              highlightthickness=0, bg='white')
        self.import_file_1_button.image = self.folder_image_1
        self.import_file_1_button.grid(row=0, column=2, padx=5, pady=10)

        # Adding description to file 2 input (Transmitter Info File)
        self.file_2_description = tk.Label(self.middle_frame, text="Transmitter Info File:", font=('Aerial', 11),
                                           bg='white')
        self.file_2_description.grid(row=1, column=0)

        # Adding Entry component for file 2 input (Transmitter Info File)
        self.file_2_text_entry = tk.Entry(self.middle_frame, textvariable=self.file_path_2, width=55)
        self.file_2_text_entry.grid(row=1, column=1)

        # Adding Button component to select file 2 input (Transmitter Info File)
        self.folder_image_2 = PhotoImage(file='gui/assets/folder.png')
        self.import_file_2_button = tk.Button(self.middle_frame, image=self.folder_image_2, command=self.select_file_2,
                                              borderwidth=0,
                                              highlightthickness=0, bg='white')
        self.import_file_2_button.image = self.folder_image_2
        self.import_file_2_button.grid(row=1, column=2, padx=5)

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
        self.import_button = tk.Button(self.bottom_frame, text="Import", command=self.load, padx=50, pady=5)
        self.import_button.grid(row=0, column=1)

        # Adding bottom frame to third row in grid
        self.bottom_frame.columnconfigure(0, weight=1)
        self.bottom_frame.rowconfigure(0, weight=1)
        self.bottom_frame.rowconfigure(1, weight=1)
        self.bottom_frame.grid(row=2, column=0, sticky="NESW", pady=20, padx=50)

    def select_file_1(self):
        """
            Action to select file 1 and set the filepath
        """

        # Opens a dialog to select a CSV file
        filename = filedialog.askopenfilename(defaultextension=".csv",
                                              filetypes=(("CSV Files", "*.csv"), ("All Files", "*.*")),
                                              initialdir=".")
        LoggerFactory.get_logger().info(f"Selected files 1 as {filename}")
        self.file_path_1.set(filename)

    def select_file_2(self):
        """
            Action to select file 2 and set the filepath
        """

        # Opens a dialog to select a CSV file
        file_name = filedialog.askopenfilename(defaultextension=".csv",
                                               filetypes=(("CSV Files", "*.csv"), ("All Files", "*.*")),
                                               initialdir=".")
        LoggerFactory.get_logger().info(f"Selected file 2 as {file_name}")
        self.file_path_2.set(file_name)

    def load(self):
        """
            Action to import both files
        """
        LoggerFactory.get_logger().info(f"Importing file 1 as {self.file_path_1.get()}")
        LoggerFactory.get_logger().info(f"Importing file 2 as {self.file_path_2.get()}")
        result = self.data_manager.read_in_csv_data(self.file_path_1.get(), self.file_path_2.get())
        if result:
            self.set_state_of_buttons()
            self.window.destroy()
        else:
            messagebox.showerror('Error', 'Could not load files')

    def cancel(self):
        """
            Action to cancel importing files
        """
        LoggerFactory.get_logger().info("Cancelling Import CSV Files Window")
        self.window.destroy()
