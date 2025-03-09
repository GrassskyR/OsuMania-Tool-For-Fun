import osu_file_parser
import random as rd

class OsuBeatmapEditor():

    def __init__(self, osu_file : osu_file_parser.OsuParser):
        self.osufile = osu_file

    def save_osu_file(self, save_path : str):
        
        General = self.osufile.General  # Get the sections of the osu file
        Editor = self.osufile.Editor
        Metadata = self.osufile.Metadata
        Difficulty = self.osufile.Difficulty
        Events = self.osufile.Events
        TimingPoints = self.osufile.TimingPoints
        HitObjects = self.osufile.HitObjects
        
        with open(f"{save_path}\{Metadata['Artist']} - {Metadata['Title']} [{Metadata['Version']}].osu", "w",encoding="UTF-8") as f:
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

        self.osufile.Metadata["Version"] += " Edited"  # Change the version of the map

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

if __name__ == "__main__":
    pass
        