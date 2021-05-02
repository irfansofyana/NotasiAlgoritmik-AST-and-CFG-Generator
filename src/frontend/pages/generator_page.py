import tkinter as tk
import json
from tkinter import messagebox
from src.frontend.pages.start_page import NotalSrcDir
from src.api.visualize_ast import *
from src.api.visualize_cfg import *
from PIL import Image


class BasicGenerator(tk.Frame, NotalSrcDir):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.render_generate_ast_button()
        self.render_visualize_ast_button()
        self.render_generate_cfg_button()
        self.render_visualize_cfg_button()
        self.render_back_button()
        self.render_source_scrollbar()
        self.render_result_scrollbar()
        self.render_source_text()
        self.render_result_text()

    def render_generate_ast_button(self):
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

    def render_visualize_ast_button(self):
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

    def render_generate_cfg_button(self):
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

    def render_visualize_cfg_button(self):
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

    def handle_back_button(self):
        NotalSrcDir.src_dir = ''
        self.src_area.configure(state='normal')
        self.src_area.delete(1.0, tk.END)
        self.res_area.configure(state='normal')
        self.res_area.delete(1.0, tk.END)
        self.controller.show_frame("StartPage")

    def render_back_button(self):
        self.back_button = tk.Button(
            self,
            bg='white',
            fg='black',
            text='Back',
            command=lambda: self.handle_back_button(),
            width=6,
            height=1,
        )
        self.back_button.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

    def render_source_scrollbar(self):
        self.ver_sb = tk.Scrollbar(self, orient=tk.VERTICAL)
        self.ver_sb.pack(side=tk.LEFT, fill=tk.Y)
        self.hor_sb = tk.Scrollbar(self, orient=tk.HORIZONTAL)
        self.hor_sb.pack(side=tk.BOTTOM, fill=tk.X)

    def render_result_scrollbar(self):
        self.ver_sb_1 = tk.Scrollbar(self, orient=tk.VERTICAL)
        self.ver_sb_1.pack(side=tk.RIGHT, fill=tk.Y)
        self.hor_sb_1 = tk.Scrollbar(self, orient=tk.HORIZONTAL)
        self.hor_sb_1.pack(side=tk.BOTTOM, fill=tk.X)

    def render_source_text(self):
        self.src_area = tk.Text(
            self,
            width=67,
            height=50,
            wrap="none",
            yscrollcommand=self.ver_sb.set,
            xscrollcommand=self.hor_sb.set
        )
        self.src_area.pack(side=tk.LEFT)
        self.ver_sb.config(command=self.src_area.yview)
        self.hor_sb.config(command=self.src_area.xview)

    def render_result_text(self):
        self.res_area = tk.Text(
            self,
            width=67,
            height=50,
            wrap="none",
            yscrollcommand=self.ver_sb_1.set,
            xscrollcommand=self.hor_sb_1.set
        )
        self.res_area.pack(side=tk.RIGHT)
        self.ver_sb_1.config(command=self.res_area.yview)
        self.hor_sb_1.config(command=self.res_area.xview)

    def generate_ast(self):
        try:
            if NotalSrcDir.src_dir == '':
                self.handle_text_input(mode='ast')
                return
            ast = get_ast(NotalSrcDir.src_dir)
            self.fill_result_area_and_generate_ast_image(ast)
            messagebox.showinfo("Generate AST", "AST is generated Successfully!")
        except Exception as err:
            messagebox.showerror("Generate AST", f"{err}")
            print(err)

    def generate_cfg(self):
        try:
            if NotalSrcDir.src_dir == '':
                self.handle_text_input(mode='cfg')
                return
            ast = get_ast(NotalSrcDir.src_dir)
            cfg = get_cfg_from_ast(ast)
            self.fill_result_area_and_generate_cfg_image(cfg)
            messagebox.showinfo("Generate CFG", "CFG is generated Successfully!")
        except Exception as err:
            messagebox.showerror("Generate CFG", f"{err}")
            print(err)

    @staticmethod
    def visualize_ast():
        try:
            output_path = "../output/ast.gv.png"
            image = Image.open(output_path)
            image.show()
        except Exception as err:
            messagebox.showerror("Visualize AST", f"{err}")
            print(err)

    @staticmethod
    def visualize_cfg():
        try:
            output_path = "../output/cfg.gv.png"
            image = Image.open(output_path)
            image.show()
        except Exception as err:
            messagebox.showerror("Visualize AST", f"{err}")
            print(err)

    def handle_text_input(self, mode="ast"):
        try:
            src_input = self.src_area.get("1.0", tk.END)
            ast = get_ast(None, src_input)
            if mode == "ast":
                self.fill_result_area_and_generate_ast_image(ast)
                messagebox.showinfo("Generate AST", "AST is generated Successfully!")
            else:
                cfg = get_cfg_from_ast(ast)
                self.fill_result_area_and_generate_cfg_image(cfg)
                messagebox.showinfo("Generate CFG", "CFG is generated Successfully!")
        except Exception as err:
            if mode == "ast":
                label = "Generate AST"
            else:
                label = "Generate CFG"
            messagebox.showerror(label, err)
            print(err)

    def fill_result_area_and_generate_ast_image(self, ast):
        self.res_area.configure(state='normal')
        self.res_area.delete(1.0, tk.END)
        self.res_area.insert(tk.END, json.dumps(ast, indent=1))
        self.res_area.configure(state='disabled')

        output_path = "../output/ast.gv"
        visualize_ast(ast, output_path)

    def fill_result_area_and_generate_cfg_image(self, cfg):
        self.res_area.configure(state='normal')
        self.res_area.delete(1.0, tk.END)

        output_path = "../output/cfg.gv"
        cfg_gv = convert_cfg_to_graphviz(cfg)
        visualize_cfg(cfg_gv, is_graphviz=True, output_path=output_path)

        self.res_area.insert(tk.END, str(cfg_gv))
        self.res_area.configure(state='disabled')


class SpecificGenerator(BasicGenerator):
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
        self.res_area.delete(1.0, tk.END)
        self.src_area.delete(1.0, tk.END)
        self.show_src_button.place(relx=0.5, rely=0.1, anchor=tk.CENTER)
        self.src_area.configure(state='disabled')

    def show_src(self):
        src_input = read_src(NotalSrcDir.src_dir)
        self.src_area.configure(state='normal')
        self.src_area.delete(1.0, tk.END)
        self.src_area.insert(tk.END, src_input)
        self.src_area.configure(state='disabled')
