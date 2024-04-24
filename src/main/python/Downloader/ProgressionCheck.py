from git import RemoteProgress
from tqdm import tqdm
import tkinter as tk


class Progress(RemoteProgress):
    def update(self, op_code, cur_count, max_count=None, message=''):
        pbar = tqdm(total=max_count)
        pbar.update(cur_count)


class ProgressDetection:
    def update(self, max_count, cur_count, what, terminal):
        pbar = tqdm(total=max_count, desc=what)
        pbar.update(cur_count)
        terminal.config(state="normal")
        terminal.insert(tk.END,
                        what + ": " + str(int(cur_count / max_count * 100)) + "% " + str(cur_count) + "/" + str(
                            max_count) + "\n")
        terminal.see(tk.END)
        terminal.config(state="disabled")
        terminal.update_idletasks()
