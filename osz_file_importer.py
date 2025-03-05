import os
import tkinter as tk
from tkinter import filedialog
import zipfile

class Beatmap:

    file_path = ""

    def __init__(self):
        root = tk.Tk()
        root.withdraw()

        self.file_path = filedialog.askopenfilename(
            title="选择文件",
            filetypes=[("osu beatmap", "*.osz")]  # Filter for osz files
        )
        root.destroy()

    def get_oszfile_list(self, extract_path):
        if self.file_path:
            print("选择的文件路径:", self.file_path)
            osz = zipfile.ZipFile(self.file_path,'r')
            osz.extractall(extract_path)
            print("解压完成")
            osu_files = []

            for root, dirs, files in os.walk(extract_path, topdown=False):
                for name in files:
                    osu_files.append(os.path.join(root, name))
                    
            return osu_files
        else:
            print("用户取消了选择")
            pass

    
if __name__ == "__main__":
    pass
