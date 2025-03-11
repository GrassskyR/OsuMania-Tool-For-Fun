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
        
    def random_remove_hitobjects(self, del_column : int):

        LeftIndex = 0
        RightIndex = 0
        i = 0
        hitobjects_in_a_row = 0

        self.osufile.Metadata["Version"] += f" Removed {del_column} Note"  # Change the version of the map

        HitObjectsSectionLength = len(self.osufile.HitObjects)
        random_index = 0

        while i < HitObjectsSectionLength - 1:
            i = i + 1
            RightIndex = i

            if self.osufile.HitObjects[LeftIndex][2] != self.osufile.HitObjects[RightIndex][2]: # Find hitobjects in the same row

                hitobjects_in_a_row = RightIndex - LeftIndex    # Calculate the number of hitobjects in a row

                if hitobjects_in_a_row == 1:    # If there is only one hitobject in a row
                    LeftIndex = RightIndex
                    continue    # Skip deleting the hitobject

                available_columns = []  # List to store the available columns

                for j in range(LeftIndex, RightIndex):
                    available_columns.append(j)

                for j in range(0, del_column):  # Randomly delete hitobjects

                    if len(available_columns) == 1: # Left one hitobject in the row
                        break

                    random_index = rd.choice(available_columns)    # Randomly select a hitobject to delete
                    available_columns.remove(random_index)    # Remove the hitobject from the list
                    self.osufile.HitObjects[random_index] = ""   # Delete the hitobject
                    
                LeftIndex = RightIndex  # Move to the next row

            if RightIndex == HitObjectsSectionLength - 1:   # Deal with situation when the last element is reached

                hitobjects_in_a_row = RightIndex - LeftIndex + 1    # Copied from above
 
                if hitobjects_in_a_row == 1:
                    LeftIndex = RightIndex
                    continue
                
                for j in range(0, del_column):  

                    if len(available_columns) == 1: 
                        break

                    random_index = rd.choice(available_columns)    
                    available_columns.remove(random_index)    
                    self.osufile.HitObjects[random_index] = ""   
                    
                LeftIndex = RightIndex  # Move to the next row

                LeftIndex = RightIndex  

        for hitobject in self.osufile.HitObjects:
            if hitobject == "":
                self.osufile.HitObjects.remove(hitobject) # Remove the empty elements from the list

        print("Done")

    def random_add_hitobjects(self, add_column : int):

        LeftIndex = 0
        RightIndex = 0
        i = 0
        hitobjects_in_a_row = 0
        

        self.osufile.Metadata["Version"] += f" Added {add_column} Note"

        key_column = self.osufile.Difficulty["CircleSize"]    # Get the number of key columns of the map
        
        random_column = 0
        x = 0

        while i < len(self.osufile.HitObjects) - 1:   # Loop through the hitobjects

            i = i + 1
            RightIndex = i
            hitobjects_column = []
            time = self.osufile.HitObjects[LeftIndex][2]

            if self.osufile.HitObjects[LeftIndex][2] != self.osufile.HitObjects[RightIndex][2]: # Find hitobjects in the same row

                hitobjects_in_a_row = RightIndex - LeftIndex    # Calculate the number of hitobjects in a row

                if hitobjects_in_a_row == key_column:   # Skip full column
                    LeftIndex = RightIndex
                    continue

                ln_info = self.__find_ln_in_row(self.osufile.HitObjects, LeftIndex, RightIndex) #check ln stack
                self.column_blacklist.update(ln_info)

                # column_hitojects = self.__get_hitobject_column_index_list(self.osufile.HitObjects, LeftIndex, RightIndex)

                empty_columns = self.__get_empty_column(LeftIndex, RightIndex, self.column_blacklist)    # Get the empty columns in the row

                for j in range(0, add_column):  # Randomly add hitobjects
                    

                    if len(empty_columns) == 0:
                        break

                    if j == key_column: # Skip if the number of hitobjects added is equal to the number of key columns
                        break

                    random_column = rd.choice(empty_columns)    # Randomly select a column to add a hitobject
                    empty_columns.remove(random_column)    # Remove the column from the list
                    x = self.__generate_x_value(random_column)    # Calculate the x value of the hitobject
                    self.osufile.HitObjects.insert(LeftIndex, [str(x), "192", time, "1", "0", "0:0:0:0:"])    # Insert the hitobject
                    RightIndex = RightIndex + 1

                LeftIndex = RightIndex  # Move to the next row
                i = RightIndex

        
        print("Done")

    def __get_hitobject_column_index_list(self, hitobjects : list, LeftIndex : int, RightIndex : int):
        column_index_list = []
        for i in range(LeftIndex, RightIndex):
            column_index = self.__get_hitobject_column_index(hitobjects[i])
            column_index_list.append(column_index)
        column_index_list.sort()
        return column_index_list
        
    def __find_ln_in_row(self, hitobjects : list, LeftIndex : int, RightIndex : int):
        
        column_blacklist = {}
        for i in range(LeftIndex, RightIndex):
            ln_info = {}    # Dictionary to store the long note information
            if self.__is_note_a_ln(hitobjects[i]):
                column = self.__get_hitobject_column_index(hitobjects[i])
                start = self.osufile.HitObjects[i][2]
                end = (self.osufile.HitObjects[i][5]).split(":")[0]
                ln_info["LnStartTime"] = int(start)
                ln_info["LnEndTime"] = int(end)
                column_blacklist[column] = ln_info
        return column_blacklist

    def __get_hitobject_column_index(self, hitobject : list):
        key_column = int(self.osufile.Difficulty["CircleSize"])    
        column_index =  math.floor(int(hitobject[0]) * key_column / 512) + 1 # Calculate the column index of the hitobject
        return column_index

    def __is_note_a_ln(self, hitobject : list):
        if hitobject[3] == "128" :  # check if the hitobject is a long note
            return True
    
    def __generate_x_value(self, column_index : int):
        key_column = int(self.osufile.Difficulty["CircleSize"])
        x = math.ceil(int(column_index - 1) * 512 / key_column)    # Calculate the x value of the hitobject
        return x

    def __check_ln_stack(self, column_blacklist : dict, column_index : int, time : int):

        isColumnHasLn = False

        if column_index in column_blacklist.keys():    # Check if the column is in the blacklist
            LnStartTime = column_blacklist[column_index]["LnStartTime"]
            LnEndTime = column_blacklist[column_index]["LnEndTime"]
            isColumnHasLn = (time >= LnStartTime and time <= LnEndTime)    # Check if the column has a long note
            return isColumnHasLn
    
    def __get_empty_column(self,LeftIndex : int, RightIndex : int, column_blacklist : dict):

        occupied_columns = []
        empty_columns = []
        
        column_time = int(self.osufile.HitObjects[LeftIndex][2])
        key_column = int(self.osufile.Difficulty["CircleSize"])

        occupied_columns = self.__get_hitobject_column_index_list(self.osufile.HitObjects, LeftIndex, RightIndex)

        for i in range(1, key_column + 1):
            if i not in occupied_columns:
                if self.__check_ln_stack(column_blacklist, i, column_time) == True:
                    occupied_columns.append(i)

        for i in range(1 , key_column + 1):
            if i not in occupied_columns:
                empty_columns.append(i)

        empty_columns.sort()
        return empty_columns

if __name__ == "__main__":
    pass