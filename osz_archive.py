import os
import zipfile as zf

def extract_osz(osz_path : str, target_dir : str):  # Extract the osz file
    osz = zf.ZipFile(osz_path, 'r')
    osz.extractall(target_dir)
    osu_files = []

    for root, dirs, files in os.walk(target_dir, topdown=False):  # Get all osu files
        for name in files:
            osu_files.append(os.path.join(root, name))

    return osu_files  # Return the list of osu files

def compress_osz(source_dir : str, osz_file_name : str):
    file_list = []

    for root, dirs, files in os.walk(source_dir):  # Get all files in the directory
        for file in files:
            file_list.append(os.path.join(root, file))

    osz = zf.ZipFile(osz_file_name, "w")  # Compress the files
    for file in file_list:
        osz.write(file, arcname=os.path.basename(file))
    osz.close()


if __name__ == "__main__":
    pass
