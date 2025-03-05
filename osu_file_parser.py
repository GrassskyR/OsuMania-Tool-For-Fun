class OsuParser:

    osufile = []
    beatmap_section_index_index = ""
    list_type_sections = ["Events", "TimingPoints", "HitObjects"]
    dict_type_sections = ["General", "Editor", "Metadata", "Difficulty","Colours"]
    section_dict = {}
    section_list = []

    General = {}
    Editor = {}
    Metadata = {}
    Difficulty = {}
    Events = []
    TimingPoints = []
    Colours = {}
    HitObjects = []


    def __init__(self, file_path):
        self.file_path = file_path      #Read osu file into list
        fp = open(self.file_path, 'r', encoding = "utf-8")
        self.osufile = fp.readlines()
        fp.close()  #end of reading osu file into list
        self.General = self.get_beatmap_section("General")
        self.Editor = self.get_beatmap_section("Editor")
        self.Metadata = self.get_beatmap_section("Metadata")
        self.Difficulty = self.get_beatmap_section("Difficulty")
        self.Events = self.get_beatmap_section("Events")
        self.TimingPoints = self.get_beatmap_section("TimingPoints")
        # self.Colours = self.get_beatmap_section("Colours")
        self.HitObjects = self.get_beatmap_section("HitObjects")
    pass

    def get_beatmap_section(self, section):
        self.section_dict = {}
        self.section_list = []
        self.beatmap_section_index = section
        section_index = self.osufile.index(f"[{self.beatmap_section_index}]\n")

        if self.beatmap_section_index in self.list_type_sections:

            for i in range(section_index + 1, len(self.osufile)):   #parse Comma-separated lists
                if self.osufile[i] == '\n':
                    break
                else:
                    self.section_list.append(self.osufile[i].strip().split(','))

            return self.section_list
        
        elif self.beatmap_section_index in self.dict_type_sections:     #parse key-value pairs

            for i in range(section_index + 1, len(self.osufile)):
                if self.osufile[i] == '\n':
                    break
                else:
                    self.section_dict.update({self.osufile[i].split(':')[0]: self.osufile[i].split(':')[1].strip()})

            return self.section_dict
    
        
if __name__ == "__main__":
    osu = OsuParser("test.osu")
    print(osu.get_beatmap_section("General"))
    print(osu.General)
    pass