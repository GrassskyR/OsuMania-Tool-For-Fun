import os
from tempfile import TemporaryDirectory
import osz_file_importer
import osu_file_parser
import osu_beatmap_editor
import osz_file_exporter
import tkinter as tk
from ui import MyApplication

def main():    

    osu_file_list = []
    bm = osz_file_importer.Beatmap()
    tmp = TemporaryDirectory()

    extracted_files = bm.get_oszfile_list(tmp.name)

    for file in extracted_files:    # Get list of all osu files
        if os.path.basename(file).endswith(".osu"):
            print("选择的osu文件:", file)
            osu_file_list.append(file)
        else:
            continue
    
    root = tk.Tk()
    root.title("osu! Beatmap Editor")
    root.geometry("400x100")
    app = MyApplication(root)
    app.mainloop()

    for osu_file in osu_file_list:  # Modify the osu file
        op = osu_file_parser.OsuParser(osu_file)

        if op.General["Mode"] != "3":   # Skip if the osu file is not a mania map
            print("Not a Mania Map")
            continue

        bme = osu_beatmap_editor.OsuBeatmapEditor(op)

        if app.select_operation == 0:
            print("未选择操作")
            break
        elif app.select_operation == 1:
            print("del")
            bme.random_remove_hitobjects(app.column_counmt)
        elif app.select_operation == 2:
            print("add")
            bme.random_add_hitobjects(app.column_counmt)
        bme.save_osu_file(tmp.name)

    osz_name = os.path.basename(bm.file_path)    # Export the osz file to current directory
    osz = osz_file_exporter.OszExporter(tmp.name)
    osz.compress_osz(osz_name)
    
    tmp.cleanup()
    
if __name__ == "__main__":
    main()