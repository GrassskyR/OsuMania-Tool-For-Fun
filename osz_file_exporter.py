import os
import zipfile as zf

class OszExporter:

    def __init__(self, beatmap_file_path : str):
        self.beatmap_file_path = beatmap_file_path
        pass

    def compress_osz(self, osz_file_name):
        file_list = []

        for root, dirs, files in os.walk(self.beatmap_file_path):   # Get all files in the directory
            for file in files:
                file_list.append(os.path.join(root, file))
        
        osz = zf.ZipFile(osz_file_name, "w")    # Compress the files
        for file in file_list:
            osz.write(file, arcname=os.path.basename(file))
        osz.close()
    
if __name__ == "__main__":
    pass


        