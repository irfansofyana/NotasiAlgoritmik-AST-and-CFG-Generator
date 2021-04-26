from src.frontend.pages.start_page import StartPage
from src.frontend.pages.generator_page import *


class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (
                StartPage,
                SpecificGenerator,
                BasicGenerator
        ):
            page_name = F.__name__

            frame = F(parent=self.container, controller=self)
            frame.configure(bg='#fffbf2')
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        return frame.tkraise()


if __name__ == "__main__":
    app = App()
    app.geometry('{}x{}'.format(1280, 720))
    app.title('AST&CFG Notal Generator')
    app.mainloop()
