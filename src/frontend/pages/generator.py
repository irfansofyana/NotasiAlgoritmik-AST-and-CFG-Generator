import tkinter as tk
from tkinter import messagebox
from src.frontend.pages.start_page import NotalSrcDir
from src.api.functions import *
from src.api.visualize_ast import visualize_ast
from PIL import ImageTk, Image


class WriteFile(tk.Frame, NotalSrcDir):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.ast_generator_button = tk.Button(
            self,
            bg='white',
            fg='black',
            text='Generate AST!',
            command=lambda: self.generate_ast(),
            width=25,
            height=1,
        )
        self.ast_generator_button.place(relx=0.6, rely=0.4, anchor=tk.CENTER)

        self.cfg_generator_button = tk.Button(
            self,
            bg='white',
            fg='black',
            text='Generate CFG!',
            command=lambda: self.generate_cfg(),
            width=25,
            height=1,
        )
        self.cfg_generator_button.place(relx=0.6, rely=0.5, anchor=tk.CENTER)

        ver_sb = tk.Scrollbar(self, orient=tk.VERTICAL)
        ver_sb.pack(side=tk.RIGHT, fill=tk.BOTH)

        hor_sb = tk.Scrollbar(self, orient=tk.HORIZONTAL)
        hor_sb.pack(side=tk.BOTTOM, fill=tk.BOTH)

        self.src_area = tk.Text(self, width=80, height=50)
        self.src_area.pack(side=tk.LEFT)

        self.src_area.config(yscrollcommand=ver_sb.set)
        ver_sb.config(command=self.src_area.yview)

        self.src_area.config(xscrollcommand=hor_sb.set)
        hor_sb.config(command=self.src_area.xview)

        self.back_button = tk.Button(
            self,
            bg='white',
            fg='black',
            text='Back',
            command=lambda: self.controller.show_frame("StartPage"),
            width=12,
            height=1,
        )
        self.back_button.place(relx=0.6, rely=0.6, anchor=tk.CENTER)

    def generate_ast(self):
        try:
            ast = get_ast(NotalSrcDir.src_dir)
            visualize_ast(ast, "../output/ast.gv")
            messagebox.showinfo("Generate AST", "AST is generated Successfully!")
        except Exception as err:
            messagebox.showerror("Generate AST", f"{err}")
            print(err)

    def generate_cfg(self):
        print('dummy')


class UploadFile(WriteFile):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.show_src_button = tk.Button(
            self,
            bg='white',
            fg='black',
            text='Show Source!',
            command=lambda: self.show_src(),
            width=25,
            height=1,
        )
        self.show_src_button.place(relx=0.6, rely=0.3, anchor=tk.CENTER)
        self.src_area.configure(state='disabled')

    def show_src(self):
        src_input = read_src(NotalSrcDir.src_dir)
        self.src_area.configure(state='normal')
        self.src_area.delete(1.0, tk.END)
        self.src_area.insert(tk.END, src_input)
        self.src_area.configure(state='disabled')