import tkinter as tk
from tkinter import filedialog, Label, PhotoImage

from utils.LoggerFactory import LoggerFactory


class SaveDataSetWindow:
    """
        Window to save the data set to a specific file.
    """

    def __init__(self, master, data_manager):
        LoggerFactory.get_logger().info("Initialized Save Data Set Window")
        self.window = tk.Toplevel(master)  # Used to display dialog on top of Main Window
        self.window.configure(bg='white')
        self.window.grab_set()  # Grabs all events for the application
        self.window.title("Save Data Set")
        self.window.geometry("544x219")
        self.window.resizable(False, False)  # Prevent the user from resizing the window
        self.save_icon_image = tk.PhotoImage(file="gui/assets/save.png")
        self.window.iconphoto(False, self.save_icon_image)  # Add icon for dialog
        self.master = master

        # Using StringVar to set text value to be able to retrieve
        self.save_file_path = tk.StringVar()

        # Created a frame to group components at the top of the dialog
        self.top_frame = tk.Frame(self.window, bg='white')

        # Adding Save image to top frame
        self.save_photo_image = PhotoImage(file='gui/assets/save.png')
        self.image_label = Label(self.top_frame, image=self.save_photo_image, bg='white')
        self.image_label.grid(row=0, column=0, padx=(20, 5))

        # Adding Instructions label to top frame
        self.instructions_label = tk.Label(self.top_frame,
                                           text="Select a location to save the Data Set in .json format",
                                           font=('Aerial', 11), anchor="w", justify="left", bg='white')
        self.instructions_label.grid(row=0, column=1, padx=(5, 0))

        # Adding top frame to first row in grid
        self.top_frame.grid(row=0, column=0, sticky="NESW", pady=(20, 5))

        # Created a frame to group components at the middle of the dialog
        self.middle_frame = tk.Frame(self.window, bg='white')

        # Adding description to output (.json File)
        self.save_location_label = tk.Label(self.middle_frame, text="Save Location", font=('Aerial', 11), bg='white')
        self.save_location_label.grid(row=0, column=0)

        # Adding Entry component for file output (.json File)
        self.file_text_entry = tk.Entry(self.middle_frame, textvariable=self.save_file_path, width=55)
        self.file_text_entry.grid(row=0, column=1)

        # Adding Button component to select file output name and path (.json File)
        self.folderImage = PhotoImage(file='gui/assets/folder.png')
        self.save_file_location_button = tk.Button(self.middle_frame, image=self.folderImage,
                                                   command=self.select_file_save_location, borderwidth=0,
                                                   highlightthickness=0, bg='white')
        self.save_file_location_button.image = self.folderImage
        self.save_file_location_button.grid(row=0, column=2, padx=5, pady=10)

        # Adding middle frame to second row in grid
        self.middle_frame.columnconfigure(0, weight=1)
        self.middle_frame.rowconfigure(0, weight=1)
        self.middle_frame.grid(row=1, column=0, sticky="NESW", pady=5, padx=(10, 0))

        # Created a frame to group components at the bottom of the dialog
        self.bottom_frame = tk.Frame(self.window, bg='white')

        # Adding Button component to cancel dialog
        self.cancel_button = tk.Button(self.bottom_frame, text="Cancel", command=self.window.destroy, padx=50, pady=5,
                                       bg='white')
        self.cancel_button.grid(row=0, column=0)

        # Adding Button component to save .json file
        self.save_button = tk.Button(self.bottom_frame, text="Save", command=self.save, padx=50, pady=5, bg='white')
        self.save_button.grid(row=0, column=1)

        # Adding bottom frame to third row in grid
        self.bottom_frame.columnconfigure(0, weight=1)
        self.bottom_frame.rowconfigure(0, weight=1)
        self.bottom_frame.rowconfigure(1, weight=1)
        self.bottom_frame.grid(row=2, column=0, sticky="NESW", pady=20, padx=50)

    def select_file_save_location(self):
        """
            Action to select file name and filepath
        """
        file_name = filedialog.asksaveasfilename(defaultextension=".json",
                                                 filetypes=(("JSON Files", "*.json"), ("All Files", "*.*")),
                                                 initialdir=".")
        LoggerFactory.get_logger().info(f"Selected save file location as {file_name}")
        self.save_file_path.set(file_name)

    def save(self):
        """
            Action to save file, perform validation TODO: Perform validation here
        """

        LoggerFactory.get_logger().info(f"Saving file as {self.save_file_path.get()}")
        self.window.destroy()

    def cancel(self):
        """
            Action to cancel saving file
        """

        LoggerFactory.get_logger().info("Cancelling Save Data Set Window")
        self.window.destroy()
