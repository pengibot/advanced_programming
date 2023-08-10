import tkinter as tk
from tkinter import filedialog, Label, PhotoImage


class SaveDataSetWindow:
    def __init__(self, update_log, master=None):
        self.window = tk.Toplevel(master)
        self.window.configure(bg='white')
        self.window.grab_set()
        self.window.title("Save Data Set")
        self.window.geometry("544x219")
        self.window.resizable(False, False)
        self.master = master
        self.filepath = tk.StringVar()

        self.tf = tk.Frame(self.window, bg='white')

        self.loadImage = PhotoImage(file='Save.png')
        self.img_label = Label(self.tf, image=self.loadImage, bg='white')
        self.img_label.grid(row=0, column=0, padx=(20, 5))

        self.label1 = tk.Label(self.tf, text="Select a location to save the Data Set in .json format",
                               font=('Aerial', 11), anchor="w", justify="left", bg='white')
        self.label1.grid(row=0, column=1, padx=(5, 0))

        # self.tf.columnconfigure(0, weight=1)
        # self.tf.columnconfigure(1, weight=5)
        self.tf.grid(row=0, column=0, sticky="WENS", pady=(20, 5))

        self.mf = tk.Frame(self.window, bg='white')

        folderImage = PhotoImage(file='Folder.png')
        # img_label = Label(image=folderImage)

        self.label2 = tk.Label(self.mf, text="Save Location", font=('Aerial', 11), bg='white')
        self.label2.grid(row=0, column=0)

        self.entry1 = tk.Entry(self.mf, textvariable=self.filepath, width=55)
        self.entry1.grid(row=0, column=1)

        self.button1 = tk.Button(self.mf, image=folderImage, command=self.save_file, borderwidth=0,
                                 highlightthickness=0, bg='white')
        self.button1.image = folderImage
        self.button1.grid(row=0, column=2, padx=5, pady=10)

        self.mf.columnconfigure(0, weight=1)
        self.mf.rowconfigure(0, weight=1)
        self.mf.grid(row=1, column=0, sticky="WENS", pady=5, padx=(10, 0))

        self.bf = tk.Frame(self.window, bg='white')

        self.cancel_button = tk.Button(self.bf, text="Cancel", command=self.window.destroy, padx=50, pady=5, bg='white')
        self.cancel_button.grid(row=0, column=0)

        self.save_button = tk.Button(self.bf, text="Save", command=self.save, padx=50, pady=5, bg='white')
        self.save_button.grid(row=0, column=1)

        self.bf.columnconfigure(0, weight=1)
        self.bf.rowconfigure(0, weight=1)
        self.bf.rowconfigure(1, weight=1)
        self.bf.grid(row=2, column=0, sticky="WENS", pady=20, padx=50)

    def save_file(self):
        filename = filedialog.asksaveasfilename(defaultextension=".json",
                                                filetypes=(("JSON Files", "*.json"), ("All Files", "*.*"))
                                                , initialdir=".")
        self.filepath.set(filename)

    def save(self):
        print(f"File: {self.filepath.get()}")
        self.window.destroy()
