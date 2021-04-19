import tkinter as tk
import tkinter.filedialog as fd


class NotalSrcDir(object):
    src_dir = ''


class StartPage(tk.Frame, NotalSrcDir):
    def do_nothing(self):
        file_win = tk.Toplevel(self.master)
        button = tk.Button(file_win, text="Do nothing button")
        button.pack()

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.notal_dir = tk.StringVar()
        self.notal_dir.set('')

        heading = tk.Label(
            self,
            bg="#fffbed",
            fg="black",
            text='AST & CFG Notasi Algoritmik(Notal) Generator',
            font='none 12 bold'
        )
        heading.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

        text_and_button_action = {
            "Upload Notal File": lambda: self.load_notal_file(),
            "Write Notal File": lambda: self.controller.show_frame("WriteFile")
        }

        for i, text in enumerate(text_and_button_action):
            button = tk.Button(
                self,
                bg='white',
                fg='black',
                text=text,
                command=text_and_button_action[text],
                width=50,
                height=3
            )
            button.place(relx=0.5, rely=0.2 * (i + 3), anchor=tk.CENTER)

    def load_notal_file(self):
        self.notal_dir.set(fd.askopenfilename())
        NotalSrcDir.src_dir = self.notal_dir.get()
        self.controller.show_frame('UploadFile')
