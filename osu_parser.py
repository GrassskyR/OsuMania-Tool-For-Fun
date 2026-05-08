from dataclasses import dataclass
@dataclass
class Beatmap:
    format_version : str
    general : dict[str, str]
    editor : dict[str, str]
    metadata : dict[str, str]
    difficulty : dict[str, str]
    events : list[list[str]]
    timing_points : list[list[str]]
    colours : dict[str, str]
    hit_objects : list[list[str]]

class BeatmapParser:

    def __init__(self):
        self.list_type_sections = ["Events", "TimingPoints", "HitObjects"]
        self.dict_type_sections = ["General", "Editor", "Metadata", "Difficulty", "Colours"]

    def parse(self, raw_osu : str) -> Beatmap:   # Accept raw lines string of the osu file
        raw_lines = raw_osu.splitlines()

        format_version = raw_lines[0]
        general = self._get_beatmap_section("General", raw_lines)
        editor = self._get_beatmap_section("Editor", raw_lines)
        metadata = self._get_beatmap_section("Metadata", raw_lines)
        difficulty = self._get_beatmap_section("Difficulty", raw_lines)
        events = self._get_beatmap_section("Events", raw_lines)
        timing_points = self._get_beatmap_section("TimingPoints", raw_lines)
        colours = self._get_beatmap_section("Colours", raw_lines)
        hit_objects = self._get_beatmap_section("HitObjects", raw_lines)

        beatmap = Beatmap(format_version, general, editor, metadata, difficulty, events, timing_points, colours, hit_objects)

        return beatmap


    def _get_beatmap_section(self, section : str, raw_lines : list[str]):
        section_dict = {}
        section_list = []
        beatmap_section_index = section

        try:
            section_index = raw_lines.index(f"[{beatmap_section_index}]")
        except ValueError:
            return None

        if beatmap_section_index in self.list_type_sections:

            for i in range(section_index + 1, len(raw_lines)):  # Parse Comma-separated lists
                # print(raw_lines[i])
                if raw_lines[i] == '':
                    continue
                elif raw_lines[i][0] == "[" and raw_lines[i][-1] == "]":    # End of Section Parse
                    break
                else:
                    section_list.append(raw_lines[i].strip().split(','))

            return section_list

        elif beatmap_section_index in self.dict_type_sections:  # Parse key-value pairs

            for i in range(section_index + 1, len(raw_lines)):
                # print(raw_lines[i])
                if raw_lines[i] == '':
                    continue
                elif raw_lines[i][0] == "[" and raw_lines[i][-1] == "]":    # End of Section Parse
                    break
                else:
                    section_dict.update({raw_lines[i].split(':', 1)[0]: raw_lines[i].split(':', 1)[1].strip()})

            return section_dict

        return None


def main():
    import osu_io
    beatmap = osu_io.load_osu("test.osu")
    print(beatmap)
    ...


if __name__ == "__main__":
    main()