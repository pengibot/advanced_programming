import tkinter as tk

from gui.MainWindow import MainWindow


def main():
    """
        The execution point for the program file
    """

    window = tk.Tk()  # Display the root window and manage all other components
    window.configure(bg='white')
    window.title("Advanced Programming")
    window.geometry("675x350")
    window.resizable(False, False)  # Preventing windows from being resized
    photo = tk.PhotoImage(file="gui/assets/logo.png")
    window.iconphoto(False, photo)  # Adding icon for window
    window.protocol("WM_DELETE_WINDOW", lambda: [window.destroy(), window.quit()])  # Call functions on close
    MainWindow(window)
    window.mainloop()


# Execute code when the file is run as a script, but not when it's imported
if __name__ == '__main__':
    main()
