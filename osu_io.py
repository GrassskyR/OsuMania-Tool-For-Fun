from osu_parser import Beatmap
from osu_parser import BeatmapParser
from pathlib import Path

def load_osu(path : str) -> Beatmap:
    with open(path, "r") as f:
        raw_str = f.read()
        beatmap = BeatmapParser().parse(raw_str)
    return beatmap

def desanitize_filename(filename : str):
    illegal_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    for char in illegal_chars:
        filename = filename.replace(char, ' ')
    return filename

def save_osu(beatmap : Beatmap, save_path : str):

    format_version = beatmap.format_version
    general = beatmap.general  # Get the sections of the osu file
    editor = beatmap.editor
    metadata = beatmap.metadata
    difficulty = beatmap.difficulty
    events = beatmap.events
    timing_points = beatmap.timing_points
    hit_objects = beatmap.hit_objects

    filename = desanitize_filename(f"{metadata['Artist']} - {metadata['Title']} [{metadata['Version']}].osu")

    file_path = Path(save_path) / filename

    file_path = str(file_path)

    with open(file_path, "w", encoding="UTF-8") as f:
        f.write(f"{format_version}\n")  # Osu file format version
        f.write("\n")

        f.write("[General]\n")
        for key, value in general.items():
            f.write(
                f"{key}: {value}\n")  # General Editor sections have an extra space after the colon.I don't know why
        f.write("\n")

        f.write("[Editor]\n")
        for key, value in editor.items():
            f.write(f"{key}: {value}\n")  # Extra space after colon
        f.write("\n")

        f.write("[Metadata]\n")
        for key, value in metadata.items():
            f.write(f"{key}:{value}\n")
        f.write("\n")

        f.write("[Difficulty]\n")
        for key, value in difficulty.items():
            f.write(f"{key}:{value}\n")
        f.write("\n")

        f.write("[Events]\n")
        for event in events:
            line = ",".join(event)
            f.write(f"{line}\n")
        f.write("\n")

        f.write("[TimingPoints]\n")
        for timing_point in timing_points:
            line = ",".join(timing_point)
            f.write(f"{line}\n")
        f.write("\n")

        f.write("\n")  # Mania Maps don't have colour info
        # Write an empty line to instead

        f.write("[HitObjects]\n")
        for hit_object in hit_objects:
            line = ",".join(hit_object)
            f.write(f"{line}\n")
        f.write("\n")
        f.close()

def main():
    ...

if __name__ == '__main__':
    main()