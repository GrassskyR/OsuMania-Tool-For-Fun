import osu_file_parser
import random as rd
import math
import os

class OsuBeatmapEditor():

    def __init__(self, osu_file : osu_file_parser.OsuParser):
        self.osufile = osu_file
        self.column_blacklist = {}

    def sanitize_filename(self, filename):
        illegal_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
        for char in illegal_chars:
            filename = filename.replace(char, ' ')
        return filename

    def save_osu_file(self, save_path : str):
        
        General = self.osufile.General  # Get the sections of the osu file
        Editor = self.osufile.Editor
        Metadata = self.osufile.Metadata
        Difficulty = self.osufile.Difficulty
        Events = self.osufile.Events
        TimingPoints = self.osufile.TimingPoints
        HitObjects = self.osufile.HitObjects
        
        filename = self.sanitize_filename(f"{Metadata['Artist']} - {Metadata['Title']} [{Metadata['Version']}].osu")

        file_path = os.path.join(save_path, filename)

        with open(file_path, "w",encoding="UTF-8") as f:
            f.write("osu file format v14\n")    # Osu file format version
            f.write("\n")

            f.write("[General]\n")
            for key, value in General.items():
                f.write(f"{key}: {value}\n")    # General Editor sections have an extra space after the colon.I dont know why
            f.write("\n")
            
            f.write("[Editor]\n")
            for key, value in Editor.items():
                f.write(f"{key}: {value}\n")    # Extra space after colon
            f.write("\n")
            
            f.write("[Metadata]\n")
            for key, value in Metadata.items():
                f.write(f"{key}:{value}\n")
            f.write("\n")
            
            f.write("[Difficulty]\n")
            for key, value in Difficulty.items():
                f.write(f"{key}:{value}\n")
            f.write("\n")
            
            f.write("[Events]\n")
            for event in Events:
                line = ",".join(event)
                f.write(f"{line}\n")
            f.write("\n")
            
            f.write("[TimingPoints]\n")
            for timingpoint in TimingPoints:
                line = ",".join(timingpoint)
                f.write(f"{line}\n")
            f.write("\n")
            
            f.write("\n")   # Mania Maps dont have a colour info.
                            # Write an empty line to instead

            f.write("[HitObjects]\n")
            for hitobject in HitObjects:
                line = ",".join(hitobject)
                f.write(f"{line}\n") 
            f.write("\n")
            f.close()
        
    def random_remove_hitobjects(self):

        LeftIndex = 0
        RightIndex = 0
        i = 0
        hitobjects_in_a_row = 0

        self.osufile.Metadata["Version"] += " Removed Edited"  # Change the version of the map

        HitObjectsSectionLength = len(self.osufile.HitObjects)
        random_index = 0

        while i < HitObjectsSectionLength - 1:
            i = i + 1
            RightIndex = i

            if self.osufile.HitObjects[LeftIndex][2] != self.osufile.HitObjects[RightIndex][2]: # Find hitobjects in the same row

                hitobjects_in_a_row = RightIndex - LeftIndex    # Calculate the number of hitobjects in a row

                if hitobjects_in_a_row == 1:    # If there is only one hitobject in a row
                    LeftIndex = RightIndex
                    continue    # Skip to the next iteration

                random_index = rd.randint(LeftIndex,RightIndex - 1)   # Randomly select a hitobject in the row

                self.osufile.HitObjects[random_index] = ""  # Remove the hitobject

                LeftIndex = RightIndex

            if RightIndex == HitObjectsSectionLength - 1:   # Deal with situation when the last element is reached

                hitobjects_in_a_row = RightIndex - LeftIndex + 1

                if hitobjects_in_a_row == 1:
                    LeftIndex = RightIndex
                    continue

                random_index = rd.randint(LeftIndex,RightIndex - 1)

                self.osufile.HitObjects[random_index] = ""

                LeftIndex = RightIndex

        for hitobject in self.osufile.HitObjects:
            if hitobject == "":
                self.osufile.HitObjects.remove(hitobject) # Remove the empty elements from the list

        print("Done")

    def random_add_hitobjects(self):

        LeftIndex = 0
        RightIndex = 0
        i = 0
        hitobjects_in_a_row = 0

        self.osufile.Metadata["Version"] += " Added Edited"

        key_column = self.osufile.Difficulty["CircleSize"]    # Get the number of key columns of the map
        
        random_column = 0
        x = 0

        while i < len(self.osufile.HitObjects) - 1:
            i = i + 1
            RightIndex = i

            if self.osufile.HitObjects[LeftIndex][2] != self.osufile.HitObjects[RightIndex][2]: # Find hitobjects in the same row

                hitobjects_in_a_row = RightIndex - LeftIndex    # Calculate the number of hitobjects in a row

                for j in range(LeftIndex, RightIndex):
                    if self.is_note_a_ln(self.osufile.HitObjects[j]):    # If the hitobject is a long note
                        ln_info = {}    # Create a dictionary to store the long note info
                        ln_info["LnStartTime"] = int(self.osufile.HitObjects[j][2])
                        ln_info["LnEndTime"] = int((self.osufile.HitObjects[j][5]).split(":")[0])
                        self.column_blacklist[self.get_hitobject_column_index(self.osufile.HitObjects[j])] = ln_info    # Add the LN info to the blacklist to prevent stack notes

                # print(self.column_blacklist.values())

                if hitobjects_in_a_row == key_column:   # Skip full column
                    LeftIndex = RightIndex
                    # print("Full !!")
                    continue
                
                random_column = self.get_random_column(LeftIndex, RightIndex, self.column_blacklist)    # Get a random column

                if random_column == 0:
                    # print("Full !!")
                    LeftIndex = RightIndex
                    continue

                time = self.osufile.HitObjects[LeftIndex][2]    # Get the time of the hitobject in the same row
                x = self.generate_x_value(random_column)   # Generate the x value of the hitobject
                # print(f"x = {x} \nrandom = {random_column}")
                self.osufile.HitObjects.insert(LeftIndex, [str(x), "192", time, "1", "0", "0:0:0:0:"])    # Insert the hitobject
                RightIndex = RightIndex + 1
                LeftIndex = RightIndex

    
        print("Done")

    def get_hitobject_column_index(self, hitobject : list):
        key_column = int(self.osufile.Difficulty["CircleSize"])    
        column_index =  math.floor(int(hitobject[0]) * key_column / 512) + 1 # Calculate the column index of the hitobject
        return column_index

    def is_note_a_ln(self, hitobject : list):
        if hitobject[3] == "128" :  # check if the hitobject is a long note
            return True
    
    def generate_x_value(self, column_index : int):
        key_column = int(self.osufile.Difficulty["CircleSize"])
        x = math.ceil(int(column_index - 1) * 512 / key_column)    # Calculate the x value of the hitobject
        return x

    def __check_ln_stack(self, column_blacklist : dict, column_index : int, time : int):
        if column_index in column_blacklist.keys():    # Check if the column is in the blacklist
            if time >= column_blacklist[column_index]["LnStartTime"] and time <= column_blacklist[column_index]["LnEndTime"]:
                return True
        return False
    
    def get_random_column(self,LeftIndex : int, RightIndex : int, column_blacklist : dict):
        occupied_columns = []
        column_time = int(self.osufile.HitObjects[LeftIndex][2])
        key_column = int(self.osufile.Difficulty["CircleSize"])
        # print(column_time)
        random_column = 0

        empty_columns = []

        for i in range(LeftIndex, RightIndex):
            column_index = self.get_hitobject_column_index(self.osufile.HitObjects[i])
            occupied_columns.append(column_index)

        for i in range(1, key_column + 1):
            if i not in occupied_columns:
                if self.__check_ln_stack(column_blacklist, i, column_time):
                    occupied_columns.append(i)

        for i in range(1 , key_column + 1):
            if i not in occupied_columns:
                empty_columns.append(i)

        if len(empty_columns) != 0: 
            random_column = rd.choice(empty_columns)    # Randomly select a column
        
        # print(f"occupied = {occupied_columns} \nempty = {empty_columns}")

        return random_column

if __name__ == "__main__":
    pass
        