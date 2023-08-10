import tkinter as tk
from tkinter import filedialog, Label, PhotoImage

from LoggerFactory import LoggerFactory


class LoadDataSetWindow:
    def __init__(self, master=None):
        LoggerFactory.get_logger().info("Initialized Load Data Set Window")
        self.window = tk.Toplevel(master)
        self.window.grab_set()
        self.window.configure(bg='white')
        self.window.title("Load Data Set")
        self.window.geometry("544x271")
        self.window.resizable(False, False)
        photo = tk.PhotoImage(file="images/Load.png")
        self.window.iconphoto(False, photo)
        self.master = master
        self.filepath1 = tk.StringVar()
        self.filepath2 = tk.StringVar()

        self.tf = tk.Frame(self.window, bg='white')

        self.loadImage = PhotoImage(file='images/Load.png')
        self.img_label = Label(self.tf, image=self.loadImage, bg='white')
        self.img_label.grid(row=0, column=0, padx=(20, 5))

        self.label1 = tk.Label(self.tf, text="Select the two files with data on the broadcast info and\ntransmitter "
                                             "info. They must both be .csv files.",
                               font=('Aerial', 11), anchor="w", justify="left", bg='white')
        self.label1.grid(row=0, column=1, padx=(5, 0))

        # self.tf.columnconfigure(0, weight=1)
        # self.tf.columnconfigure(1, weight=5)
        self.tf.grid(row=0, column=0, sticky="NESW", pady=20)

        self.mf = tk.Frame(self.window, bg='white')

        folderImage1 = PhotoImage(file='images/Folder.png')
        folderImage2 = PhotoImage(file='images/Folder.png')
        # img_label = Label(image=folderImage)

        self.label2 = tk.Label(self.mf, text="Broadcast Info File:", font=('Aerial', 11), bg='white')
        self.label2.grid(row=0, column=0)

        self.entry1 = tk.Entry(self.mf, textvariable=self.filepath1, width=55)
        self.entry1.grid(row=0, column=1)

        self.button1 = tk.Button(self.mf, image=folderImage1, command=self.load_file1, borderwidth=0,
                                 highlightthickness=0, bg='white')
        self.button1.image = folderImage1
        self.button1.grid(row=0, column=2, padx=5, pady=10)

        self.label2 = tk.Label(self.mf, text="Transmitter Info File:", font=('Aerial', 11), bg='white')
        self.label2.grid(row=1, column=0)

        self.entry1 = tk.Entry(self.mf, textvariable=self.filepath2, width=55)
        self.entry1.grid(row=1, column=1)

        self.button2 = tk.Button(self.mf, image=folderImage2, command=self.load_file2, borderwidth=0,
                                 highlightthickness=0, bg='white')
        self.button2.image = folderImage2
        self.button2.grid(row=1, column=2, padx=5)

        self.mf.columnconfigure(0, weight=1)
        self.mf.rowconfigure(0, weight=1)
        self.mf.rowconfigure(1, weight=1)
        self.mf.grid(row=1, column=0, sticky="NESW", pady=10, padx=(10, 0))

        self.bf = tk.Frame(self.window, bg='white')

        self.cancel_button = tk.Button(self.bf, text="Cancel", command=self.window.destroy, padx=50, pady=5)
        self.cancel_button.grid(row=0, column=0)

        self.load_button = tk.Button(self.bf, text="Load", command=self.load, padx=50, pady=5)
        self.load_button.grid(row=0, column=1)

        self.bf.columnconfigure(0, weight=1)
        self.bf.rowconfigure(0, weight=1)
        self.bf.rowconfigure(1, weight=1)
        self.bf.grid(row=2, column=0, sticky="NESW", pady=20, padx=50)

    def load_file1(self):
        filename = filedialog.askopenfilename()
        self.filepath1.set(filename)

    def load_file2(self):
        filename = filedialog.askopenfilename()
        self.filepath2.set(filename)

    def load(self):
        print(f"File 1: {self.filepath1.get()}")
        print(f"File 2: {self.filepath2.get()}")
        self.window.destroy()
