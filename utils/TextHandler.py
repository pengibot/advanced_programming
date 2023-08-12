import logging
import tkinter as tk


class TextHandler(logging.Handler):
    """
        This class logs to a Text widget
    """

    def __init__(self, text):
        # run the regular Handler
        logging.Handler.__init__(self)
        # Store a reference to the Text it will log to
        self.text = text

    def emit(self, record):
        msg = self.format(record)

        def append():
            self.text.configure(state='normal')
            self.text.insert(tk.END, msg + '\n')
            self.text.configure(state='disabled')
            self.text.yview(tk.END)  # Autoscroll to the bottom

        # This is necessary as cannot modify Text from other threads
        self.text.after(0, append)
