import enum
import os
import tkinter as tk
from tkinter import ttk

import pandas as pd

from Core.Executor import execute_test, execute, single_execution
from Utils.DesignPattern import DesignPattern

oracles_list = ["Adapter", "AdapterExtended", "Classes", "Test"]
current_directory = os.path.dirname(os.getcwd())
resource_directory = os.path.join(os.path.dirname(current_directory), "resources")


class Interface:
    current_interface = "GithubDetector"

    def __init__(self, master, current_interface):
        self.master = master
        self.current_interface = current_interface

        self.detector_frame = tk.Frame(self.master)
        self.detector_frame.pack(side="left")

        self.master.title("Design Pattern Detector")
        self.interface_menu()

        if current_interface == "GithubDetector":
            self.create_listbox(list(DesignPattern))
            self.create_text_box()
        elif current_interface == "OracleTest":
            self.create_listbox(oracles_list)
        elif current_interface == "Niche":
            niche_df = pd.read_excel(resource_directory + "/NICHE.xlsx")
            self.create_listbox(list(DesignPattern))
            self.create_listbox_niche(niche_df["GitHub Repo"])

        self.debug_mode = tk.BooleanVar()
        debug_mode_checkbox = tk.Checkbutton(self.detector_frame, text="Debug Mode", font=("Helvetica", 15),
                                             variable=self.debug_mode)
        debug_mode_checkbox.pack()

        self.delete_repository = tk.BooleanVar()
        self.delete_repository.set(True)
        delete_repository_checkbox = tk.Checkbutton(self.detector_frame, text="Delete Repository",
                                                    font=("Helvetica", 15), variable=self.delete_repository)
        delete_repository_checkbox.pack()

        self.button = tk.Button(self.detector_frame, text="Detect", command=self.my_function, font=("Helvetica", 15))
        self.button.pack(pady=5)

        self.create_terminal()
        self.ast_view()

    def interface_menu(self):
        self.menu = tk.Menu(self.master)

        self.menu.add_command(label="Github Detector", command=lambda: self.open_interface("GithubDetector"))
        self.menu.add_command(label="Oracles Test", command=lambda: self.open_interface("OracleTest"))
        self.menu.add_command(label="Niche", command=lambda: self.open_interface("Niche"))

        self.master.config(menu=self.menu)

    def open_interface(self, new_interface):
        if self.current_interface != new_interface:
            self.master.destroy()
            root = tk.Tk()
            Interface(root, new_interface)
            root.mainloop()

    def create_listbox(self, list_content):
        self.label_list = tk.Label(self.detector_frame, text="Select the Design Pattern you want detect:",
                                   font=("Helvetica", 15))
        self.label_list.pack()

        # This is the frame of listbox
        self.listbox_frame = tk.Frame(self.detector_frame)
        self.listbox_frame.pack(pady=5)

        self.listbox = tk.Listbox(self.listbox_frame, selectmode=tk.MULTIPLE,
                                  selectborderwidth=2, border=5, font=("Helvetica", 15), exportselection=False)

        if len(list_content) > 5:
            self.listbox.config(height=5)
        else:
            self.listbox.config(height=len(list_content))
        counter = 0
        raw_width = 3
        for pattern in list_content:
            if isinstance(pattern, enum.Enum):
                if len(pattern.name) > raw_width:
                    raw_width = len(pattern.name)
                self.listbox.insert(counter, pattern.name)
                counter = counter + 1
            else:
                if len(pattern) > raw_width:
                    raw_width = len(pattern)
                self.listbox.insert(counter, pattern)
                counter = counter + 1

        self.listbox.config(width=raw_width)
        self.listbox.pack(side="left")

        # This is the frame of buttons
        self.button_frame = tk.Frame(self.listbox_frame)
        self.button_frame.pack(side="left", padx=20)
        self.select_button = tk.Button(self.button_frame, text="Select All", command=self.select_all,
                                       font=("Helvetica", 10))
        self.select_button.pack(side="top", pady=10)
        self.select_button = tk.Button(self.button_frame, text="Deselect All", command=self.deselect_all,
                                       font=("Helvetica", 10))
        self.select_button.pack(side="bottom")

    def create_listbox_niche(self, list_content):
        self.label_list_niche = tk.Label(self.detector_frame, text="Select the Github you want analyze:",
                                         font=("Helvetica", 15))
        self.label_list_niche.pack()

        # This is the frame of listbox
        self.listbox_frame_niche = tk.Frame(self.detector_frame)
        self.listbox_frame_niche.pack(pady=5)

        self.listbox_niche = tk.Listbox(self.listbox_frame_niche, selectmode=tk.MULTIPLE,
                                        selectborderwidth=2, border=5, font=("Helvetica", 15), exportselection=False)

        if len(list_content) > 5:
            self.listbox_niche.config(height=5)
        else:
            self.listbox_niche.config(height=len(list_content))
        counter = 0
        raw_width = 3
        for pattern in list_content:
            if isinstance(pattern, enum.Enum):
                if len(pattern.name) > raw_width:
                    raw_width = len(pattern.name)
                self.listbox_niche.insert(counter, pattern.name)
                counter = counter + 1
            else:
                if len(pattern) > raw_width:
                    raw_width = len(pattern)
                self.listbox_niche.insert(counter, pattern)
                counter = counter + 1

        self.listbox_niche.config(width=raw_width)
        self.listbox_niche.pack(side="left")

        # This is the frame of buttons
        self.button_frame = tk.Frame(self.listbox_frame_niche)
        self.button_frame.pack(side="left", padx=20)
        self.select_button = tk.Button(self.button_frame, text="Select All", command=self.select_all_niche,
                                       font=("Helvetica", 10))
        self.select_button.pack(side="top", pady=10)
        self.select_button = tk.Button(self.button_frame, text="Deselect All", command=self.deselect_all_niche,
                                       font=("Helvetica", 10))
        self.select_button.pack(side="bottom")

    def create_text_box(self):
        # This is the frame of listbox
        self.github_frame = tk.Frame(self.detector_frame)
        self.github_frame.pack(pady=5)

        self.label_github = tk.Label(self.github_frame, text="Insert a Github Repository:",
                                     font=("Helvetica", 15))
        self.label_github.pack()

        self.label_repository_name = tk.Label(self.github_frame, text="Owner:", font=("Helvetica", 15))
        self.label_repository_name.pack(side="left")
        self.entry_owner = tk.Entry(self.github_frame, font=("Helvetica", 10))
        self.entry_owner.pack(side="left")
        self.label_repository_name = tk.Label(self.github_frame, text="Repository:", font=("Helvetica", 15))
        self.label_repository_name.pack(side="left")
        self.entry_repository = tk.Entry(self.github_frame, font=("Helvetica", 10))
        self.entry_repository.pack(side="left")

    def create_terminal(self):
        self.terminal_frame = tk.Frame(self.detector_frame)
        self.terminal_frame.pack()

        scrollbar = tk.Scrollbar(self.terminal_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.terminal = tk.Text(self.terminal_frame, wrap=tk.WORD, yscrollcommand=scrollbar.set, state="disabled")
        self.terminal.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.terminal.yview)

    def select_all(self):
        self.listbox.select_set(0, tk.END)

    def select_all_niche(self):
        self.listbox_niche.select_set(0, tk.END)

    def deselect_all(self):
        self.listbox.select_clear(0, tk.END)

    def deselect_all_niche(self):
        self.listbox_niche.select_clear(0, tk.END)

    def clean_terminal(self):
        self.terminal.config(state="normal")
        self.terminal.delete("1.0", tk.END)
        self.terminal.config(state="disabled")

    def clean_ast(self):
        self.ast.destroy()
        self.ast_view()

    def ast_view(self):
        self.ast = ttk.Treeview(self.master)

        self.ast['columns'] = ('#0')
        # Formatta le colonne
        self.ast.column("#0", width=200, minwidth=50, stretch=tk.NO)
        self.ast.column("#1", width=200, minwidth=50, stretch=tk.NO)

        # Crea gli header delle colonne
        self.ast.heading("#0", text="Controlled Classes", anchor=tk.W)
        self.ast.heading("#1", text="Duplicated Classes", anchor=tk.W)
        self.ast.pack(side='left', fill='both', expand=True)

    def my_function(self):
        self.clean_terminal()
        self.clean_ast()
        selected_values = [self.listbox.get(i) for i in self.listbox.curselection()]
        debug_mode = self.debug_mode.get()
        delete_repository = self.delete_repository.get()
        if self.current_interface == "GithubDetector":
            entered_text_owner = self.entry_owner.get()
            entered_text_repository = self.entry_repository.get()
            if len(selected_values) == 0:
                self.terminal.config(state="normal")
                self.terminal.insert(tk.END, "Please select a Design Pattern")
                self.terminal.config(state="disabled")
            elif entered_text_owner == "" or entered_text_repository == "":
                self.terminal.config(state="normal")
                self.terminal.insert(tk.END, "Please insert a Github Repository for example: eliotest98\\DPDPython")
                self.terminal.config(state="disabled")
            else:
                with open(os.path.join(resource_directory, "GeneratedFiles", "Oracles", "log.txt"), "a",
                          encoding='utf-8') as f:
                    string_to_add = execute(entered_text_owner, entered_text_repository, "", debug_mode, self.terminal,
                                            selected_values, self.ast, delete_repository)
                    f.writelines("[1] " + entered_text_owner + "\\" + entered_text_repository + "\n" + string_to_add)
        elif self.current_interface == "OracleTest":
            if len(selected_values) == 0:
                self.terminal.config(state="normal")
                self.terminal.insert(tk.END, "Please select a Design Pattern")
                self.terminal.config(state="disabled")
            else:
                for value in selected_values:
                    execute_test(value, debug_mode, self.terminal, self.ast)
        elif self.current_interface == "Niche":
            selected_values_niche = [self.listbox_niche.get(i) for i in self.listbox_niche.curselection()]
            if len(selected_values) == 0:
                self.terminal.config(state="normal")
                self.terminal.insert(tk.END, "Please select a Design Pattern")
                self.terminal.config(state="disabled")
                return
            if len(selected_values_niche) == 0:
                self.terminal.config(state="normal")
                self.terminal.insert(tk.END, "Please select a Repository")
                self.terminal.config(state="disabled")
                return

            try:
                os.remove(os.path.join(resource_directory, "GeneratedFiles", "Oracles", "log.txt"))
            except FileNotFoundError:
                pass
            counter = 1
            for niche_github in selected_values_niche:
                with open(os.path.join(resource_directory, "GeneratedFiles", "Oracles", "log.txt"), "a",
                          encoding='utf-8') as f:
                    string_to_add = single_execution(niche_github, debug_mode, self.terminal, selected_values, self.ast,
                                                     delete_repository)
                    f.writelines("[" + str(counter) + "] " + niche_github + "\n" + string_to_add)
                counter = counter + 1

        self.expand_all(self.ast)

    def expand_all(self, treeview, node=''):
        for child in treeview.get_children(node):
            treeview.item(child, open=True)
            self.expand_all(treeview, child)


if __name__ == '__main__':
    interface_list = ["Github Detector", "Oracle Test"]
    try:
        os.makedirs(os.path.join(resource_directory, "GeneratedFiles", "Oracles"))
    except:
        pass

    name = input("Enter the mode GUI/CMD or end for terminate: ")
    name = name.upper()
    while name != "END":
        if name == "GUI":
            try:
                root = tk.Tk()
                my_interface = Interface(root, "GithubDetector")
                root.mainloop()
                name = "END"
            except tk.TclError as e:
                print("Error, is impossible open a GUI for this reason: ", e)
                print("Please, try with the CMD mode")
                name = ""
        elif name == "CMD":
            print("What you want to do? 1-3 exit for terminate")
            number = 1
            for interface in interface_list:
                print(number, ": ", interface)
                number = number + 1
            name = input()
            while name != "exit":
                if name == "1":
                    print("Github Detector")
                    print("Please enter the design pattern you want detect:")
                    number = 1
                    for dp in list(DesignPattern):
                        print(number, ": ", dp.value)
                        number = number + 1
                    number_write = input()

                    repository = input("Please enter the github you want analyze (Ex. advboxes\\Advbox): ")
                    repository = repository.split("\\")

                    debug_active = input("You want active the Debug Mode? Y/N: ").strip().upper()
                    debug_active = 1 if debug_active == "Y" else 0

                    delete_after = input("You want delete the repository at the end of detect? Y/N: ").strip().upper()
                    delete_after = 1 if delete_after == "Y" else 0

                    with open(os.path.join(resource_directory, "GeneratedFiles", "Oracles", "log.txt"), "a",
                              encoding='utf-8') as f:
                        string_to_add = execute(repository[0], repository[1], "", debug_active, None,
                                                [list(DesignPattern)[int(number_write) - 1].value], None, delete_after)
                        f.writelines("[1] " + repository[0] + "\\" + repository[1] + "\n" + string_to_add)
                    name = "exit"
                    break
                elif name == "2":
                    print("Oracle Test")
                    print("Please enter what oracle you want execute:")
                    number = 1
                    for oracle in oracles_list:
                        print(number, ": ", oracle)
                        number = number + 1
                    number_write = input()
                    debug_active = input("You want active the Debug Mode? Y/N: ").strip().upper()
                    debug_active = 1 if debug_active == "Y" else 0
                    execute_test(oracles_list[int(number_write) - 1], debug_active, None, None)
                    name = "exit"
                    break
                elif name == "exit":
                    break
                else:
                    print("What you want to do? 1-3 exit for terminate")
                    number = 1
                    for interface in interface_list:
                        print(number, ": ", interface)
                        number = number + 1
                    name = input()
        elif name == "END":
            break
        else:
            name = input("Enter the mode GUI/CMD or end for terminate: ")
            name = name.upper()

    print("Exit Status")
