import osu_file_parser
import random as rd

class OsuBeatmapEditor():

    def __init__(self, osu_file : osu_file_parser.OsuParser):
        self.osufile = osu_file

    def save_osu_file(self, save_path : str):
        
        General = self.osufile.General
        Editor = self.osufile.Editor
        Metadata = self.osufile.Metadata
        Difficulty = self.osufile.Difficulty
        Events = self.osufile.Events
        TimingPoints = self.osufile.TimingPoints
        HitObjects = self.osufile.HitObjects
        
        with open(f"{save_path}\{Metadata['Artist']} - {Metadata['Title']} [{Metadata['Version']}].osu", "w",encoding="UTF-8") as f:
            f.write("osu file format v14\n")    #osu file format version
            f.write("\n")

            f.write("[General]\n")
            for key, value in General.items():
                f.write(f"{key}: {value}\n")    #General Editor sections have an extra space after the colon.I dont know why
            f.write("\n")
            
            f.write("[Editor]\n")
            for key, value in Editor.items():
                f.write(f"{key}: {value}\n")    #extra space after colon
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
            
            f.write("\n")   #Mania Maps dont have a colour info.
                            #Write an empty line to instead

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
        hitobjects_in_a_row = 0     #unused

        self.osufile.Metadata["Version"] += " Edited"  #Change the version of the map

        HitObjectsSectionLength = len(self.osufile.HitObjects)

        while i < HitObjectsSectionLength - 1:
            i += 1
            RightIndex = i

            if(self.osufile.HitObjects[LeftIndex][2] != self.osufile.HitObjects[RightIndex][2]):  #If the column of the hitobjects are different
                hitobjects_in_a_row = RightIndex - LeftIndex
                if(hitobjects_in_a_row > 1):    #If there are more than 1 hitobjects in a row
                    self.osufile.HitObjects.pop(rd.randint(LeftIndex, RightIndex - 1))   #Remove a random hitobject from the row
                LeftIndex = RightIndex
                HitObjectsSectionLength = len(self.osufile.HitObjects)
                continue

        print("Done")

if __name__ == "__main__":
    pass
        