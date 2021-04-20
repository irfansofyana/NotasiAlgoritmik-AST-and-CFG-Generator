import tkinter as tk
import json
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
            width=15,
            height=1,
        )
        self.ast_generator_button.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

        self.visualize_ast_button = tk.Button(
            self,
            bg='white',
            fg='black',
            text='Visualize AST!',
            command=lambda: self.visualize_ast(),
            width=15,
            height=1,
        )
        self.visualize_ast_button.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

        self.cfg_generator_button = tk.Button(
            self,
            bg='white',
            fg='black',
            text='Generate CFG!',
            command=lambda: self.generate_cfg(),
            width=15,
            height=1,
        )
        self.cfg_generator_button.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

        self.visualize_cfg_button = tk.Button(
            self,
            bg='white',
            fg='black',
            text='Visualize CFG!',
            command=lambda: self.visualize_cfg(),
            width=15,
            height=1,
        )
        self.visualize_cfg_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        ver_sb = tk.Scrollbar(self, orient=tk.VERTICAL)
        ver_sb.pack(side=tk.LEFT, fill=tk.Y)
        hor_sb = tk.Scrollbar(self, orient=tk.HORIZONTAL)
        hor_sb.pack(side=tk.BOTTOM, fill=tk.X)

        ver_sb_1 = tk.Scrollbar(self, orient=tk.VERTICAL)
        ver_sb_1.pack(side=tk.RIGHT, fill=tk.Y)
        hor_sb_1 = tk.Scrollbar(self, orient=tk.HORIZONTAL)
        hor_sb_1.pack(side=tk.BOTTOM, fill=tk.X)

        self.src_area = tk.Text(
            self,
            width=67,
            height=50,
            wrap="none",
            yscrollcommand=ver_sb.set,
            xscrollcommand=hor_sb.set
        )
        self.src_area.pack(side=tk.LEFT)

        self.res_area = tk.Text(
            self,
            width=67,
            height=50,
            wrap="none",
            yscrollcommand=ver_sb_1.set,
            xscrollcommand=hor_sb_1.set
        )
        self.res_area.pack(side=tk.RIGHT)

        ver_sb.config(command=self.src_area.yview)
        hor_sb.config(command=self.src_area.xview)
        ver_sb_1.config(command=self.res_area.yview)
        hor_sb_1.config(command=self.res_area.xview)

        self.back_button = tk.Button(
            self,
            bg='white',
            fg='black',
            text='Back',
            command=lambda: self.controller.show_frame("StartPage"),
            width=6,
            height=1,
        )
        self.back_button.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

    def generate_ast(self):
        try:
            ast = get_ast(NotalSrcDir.src_dir)

            self.res_area.configure(state='normal')
            self.res_area.delete(1.0, tk.END)
            self.res_area.insert(tk.END, json.dumps(ast, indent=1))
            self.res_area.configure(state='disabled')

            output_path = "../output/ast.gv"
            visualize_ast(ast, output_path)

            messagebox.showinfo("Generate AST", "AST is generated Successfully!")
        except Exception as err:
            messagebox.showerror("Generate AST", f"{err}")
            print(err)

    def generate_cfg(self):
        print('dummy')

    def visualize_ast(self):
        try:
            output_path = "../output/ast.gv.png"
            image = Image.open(output_path)
            image.show()
        except Exception as err:
            messagebox.showerror("Visualize AST", f"{err}")
            print(err)

    def visualize_cfg(self):
        print('Dummy')


class UploadFile(WriteFile):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.show_src_button = tk.Button(
            self,
            bg='white',
            fg='black',
            text='Show Source!',
            command=lambda: self.show_src(),
            width=15,
            height=1,
        )
        self.show_src_button.place(relx=0.5, rely=0.1, anchor=tk.CENTER)
        self.src_area.configure(state='disabled')

    def show_src(self):
        src_input = read_src(NotalSrcDir.src_dir)
        self.src_area.configure(state='normal')
        self.src_area.delete(1.0, tk.END)
        self.src_area.insert(tk.END, src_input)
        self.src_area.configure(state='disabled')
