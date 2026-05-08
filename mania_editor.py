import random as rd
import math
from typing import Any

from osu_parser import Beatmap
import logging
from collections import defaultdict

logger = logging.getLogger(__name__)


def remove_random_notes_per_row(beatmap: Beatmap, count: int) -> Beatmap:

    left_index = 0
    right_index = 0

    hit_objects_section_length = len(beatmap.hit_objects)

    beatmap.metadata["Version"] += f" Removed {count} Note"  # Change the version of the map

    while right_index < hit_objects_section_length:  # This code finds hit_objects section at the same column

        if beatmap.hit_objects[right_index][2] != beatmap.hit_objects[left_index][2]:
            column_count = right_index - left_index

            if column_count >= count:
                rd_column_indexs = rd.sample(range(left_index, right_index), count)
                for rd_column_index in rd_column_indexs:
                    beatmap.hit_objects[rd_column_index] = []  # random remove 1 notes
            left_index = right_index

        right_index = right_index + 1

    if left_index < len(beatmap.hit_objects):
        column_count = right_index - left_index

        if column_count >= count:
            rd_column_indexs = rd.sample(range(left_index, right_index), count)
            for rd_column_index in rd_column_indexs:
                beatmap.hit_objects[rd_column_index] = []

    new_hit_objects = []
    for hit_object in beatmap.hit_objects:
        if not hit_object:
            continue
        new_hit_objects.append(hit_object)

    beatmap.hit_objects = new_hit_objects
    return beatmap


def add_random_notes_per_row(beatmap: Beatmap, count: int) -> Beatmap:
    left_index = 0
    right_index = 0

    beatmap.metadata["Version"] += f" Added {count} Note"
    column_blacklist = defaultdict(list)

    while right_index < len(beatmap.hit_objects):  # find All Long Notes

        if beatmap.hit_objects[right_index][2] != beatmap.hit_objects[left_index][2]:
            column_blacklist = _add_long_notes_to_black_list(beatmap, left_index, right_index, column_blacklist)
            left_index = right_index

        right_index = right_index + 1

    if left_index < len(beatmap.hit_objects):
        column_blacklist = _add_long_notes_to_black_list(beatmap, left_index, right_index, column_blacklist)

    left_index = 0
    right_index = 0

    while right_index < len(beatmap.hit_objects):  # Add Notes

        if beatmap.hit_objects[right_index][2] != beatmap.hit_objects[left_index][2]:
            empty_columns = _get_empty_columns(beatmap, left_index, right_index, column_blacklist)
            beatmap, right_index = _add_notes_to_empty_columns(beatmap, empty_columns, left_index, right_index, count)
            left_index = right_index

        right_index = right_index + 1

    if left_index < len(beatmap.hit_objects):
        empty_columns = _get_empty_columns(beatmap, left_index, right_index, column_blacklist)
        beatmap, right_index = _add_notes_to_empty_columns(beatmap, empty_columns, left_index, right_index, count)

    return beatmap


def _add_notes_to_empty_columns(beatmap: Beatmap, empty_columns: list, left_index: int, right_index: int, count : int) -> tuple[
    Beatmap, int]:
    cur_timing = int(beatmap.hit_objects[left_index][2])
    circle_size = beatmap.difficulty["CircleSize"]
    cnt = 0
    while empty_columns and cnt < count:
        cnt += 1
        random_column = rd.choice(empty_columns)  # Randomly select a column to add a hit object
        empty_columns.remove(random_column)  # Remove the column from the list
        x = _generate_x_value(random_column, circle_size)  # Calculate the x value of the hit object
        beatmap.hit_objects.insert(left_index,
                                   [str(x), "192", str(cur_timing), "1", "0", "0:0:0:0:"])  # Insert the hit object
        right_index = right_index + 1
    return beatmap, right_index


def _get_empty_columns(beatmap: Beatmap, left_index: int, right_index: int, column_blacklist: dict) -> list:
    circle_size = beatmap.difficulty["CircleSize"]
    cur_timing = int(beatmap.hit_objects[left_index][2])
    columns = set()
    empty_columns = set(list(range(1, int(circle_size) + 1)))

    for i in range(left_index, right_index):  # get available columns
        column = _get_hit_object_column_index(beatmap.hit_objects[i], circle_size)
        columns.add(column)

    empty_columns -= columns
    empty_columns = list(empty_columns)

    block_columns = []

    for column in empty_columns:  # check LN stack
        lone_note_sections = column_blacklist[column]
        for lone_note_section in lone_note_sections:
            start_time = lone_note_section[0]
            end_time = lone_note_section[1]
            if start_time <= cur_timing <= end_time:
                block_columns.append(column)
                break

    empty_columns = list(set(empty_columns) - set(block_columns))

    return empty_columns


def _add_long_notes_to_black_list(beatmap: Beatmap, left_index: int, right_index: int, column_blacklist: dict) -> dict[
    int, list]:
    long_notes = _find_long_notes_in_row(beatmap.hit_objects, left_index, right_index)
    circle_size = beatmap.difficulty["CircleSize"]

    for long_note_index in long_notes:
        column = _get_hit_object_column_index(beatmap.hit_objects[long_note_index], circle_size)
        if column not in column_blacklist:
            column_blacklist[column] = []
        long_note_start_time = int(beatmap.hit_objects[long_note_index][2])  # start time of ln
        long_note_end_time = int((beatmap.hit_objects[long_note_index][5]).split(":")[0])  # end time of ln
        column_blacklist[column].append([long_note_start_time, long_note_end_time])  # Add LN time to blacklist

    return column_blacklist


def _find_long_notes_in_row(hit_objects: list[list], left_index: int,
                            right_index: int) -> list:  # return all Long Note in the same row
    long_notes = []
    for i in range(left_index, right_index):
        if _is_long_note(hit_objects[i]):
            long_notes.append(i)
    return long_notes  # return index of long note in the hit_object list


def _is_long_note(hit_object: list) -> bool:
    mask = 0b10000000
    note_type = int(hit_object[3])
    note_type = (note_type & mask) >> 7  # if the 7th bit of a type is 1, the type of Note is a Long Note

    return note_type == 1  # check if a note is LN


def _get_hit_object_column_index(hit_object: list, circle_size: str) -> int:
    key_column = int(circle_size)
    column_index = math.floor(int(hit_object[0]) * key_column / 512) + 1  # Calculate the column index of the hitobject
    return column_index


def _generate_x_value(column_index: int, circle_size: str) -> int:
    key_column = int(circle_size)
    x = math.ceil(int(column_index - 1) * 512 / key_column)  # Calculate the x value of the hitobject
    return x


def main():
    from osu_io import load_osu, save_osu
    beatmap = load_osu("test_LN2.osu")
    beatmap = remove_random_notes_per_row(beatmap, 1)
    save_osu(beatmap, "")
    ...


if __name__ == "__main__":
    main()
