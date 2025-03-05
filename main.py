import random as rd
import os
from tempfile import TemporaryDirectory
import osz_file_importer
import osu_file_parser
import osu_beatmap_editor
import osz_file_exporter

def main():    

    osu_file_list = []
    bm = osz_file_importer.Beatmap()
    tmp = TemporaryDirectory()

    extracted_files = bm.get_oszfile_list(tmp.name)

    for file in extracted_files:
        if os.path.basename(file).endswith(".osu"):
            print("选择的osu文件:", file)
            osu_file_list.append(file)
        else:
            continue
    
    for osu_file in osu_file_list:
        op = osu_file_parser.OsuParser(osu_file)
        bme = osu_beatmap_editor.OsuBeatmapEditor(op)
        bme.random_remove_hitobjects()
        bme.save_osu_file(tmp.name)

    osz_name = os.path.basename(bm.file_path).replace(".osz", "_edited.osz")
    osz = osz_file_exporter.OszExporter(tmp.name)
    osz.compress_osz(osz_name)
    
    tmp.cleanup()
    
if __name__ == "__main__":
    main()