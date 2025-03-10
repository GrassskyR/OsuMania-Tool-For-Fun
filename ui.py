import tkinter as tk
import osu_file_parser
import osu_beatmap_editor
import os

class MyApplication(tk.Frame):

    select_operation = 0

    def __init__(self, master = None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
    pass

    def create_widgets(self):
        self.btn0 = tk.Button(self, text = "每行随机删除一个键", command = self.del_op, width = 25, height = 2)
        self.btn0.pack(side = "left", expand = True, padx = 10, anchor = "center")
        self.btn1 = tk.Button(self, text = "每行随机增加一个键", command = self.add_op, width = 25, height = 2)
        self.btn1.pack(side = "right", expand = True, padx = 10, anchor = "center")
        pass
    
    def del_op(self):
        print("Chosed del")
        self.select_operation = 1
        self.quit()

    def add_op(self):
        print("Chosed add")
        self.select_operation = 2
        self.quit()

def main():
    root = tk.Tk()
    root.title("osu! Beatmap Editor")
    root.geometry("400x100")
    root.resizable(False,False)
    app = MyApplication(master=root)
    app.mainloop()
    app.destroy()
    
    op = osu_file_parser.OsuParser("test7.osu")

    obe = osu_beatmap_editor.OsuBeatmapEditor(op)

    if app.select_operation == 0:
        print("未选择操作")
    elif app.select_operation == 1:
        print("del")
        obe.random_remove_hitobjects()
    elif app.select_operation == 2:
        print("add")
        obe.random_add_hitobjects()

if __name__ == "__main__":
    main()