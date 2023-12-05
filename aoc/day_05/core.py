"""
Advent of Code - Day 05
"""

from aoc.day_05.seed import p1
import re
from typing import NamedTuple, Callable
from functools import reduce
from itertools import batched, chain, count


class MapRange(NamedTuple):
    dest: int
    src: int
    length: int


class Map(NamedTuple):
    name: str
    ranges: list[MapRange]


def get_range_pos(map_range: MapRange, pos: int) -> int | None:
    if not map_range.src <= pos < map_range.src + map_range.length:
        # Out of bounds
        return None
    return map_range.dest + (pos - map_range.src)


def get_map_pos(
    pos: int,
    map_: Map,
    get_pos: Callable[[MapRange, int], int | None] = get_range_pos,
) -> int:
    return next(
        (
            dest_pos
            for map_range in map_.ranges
            if (dest_pos := get_pos(map_range, pos)) is not None
        ),
        pos,
    )


num = r"(\d+)"


def parse_map(map_raw: str) -> Map:
    [map_name, *map_data] = map_raw.splitlines()
    map_name = map_name[0:-5]
    map_numbers = [
        MapRange(*[int(seed.group()) for seed in re.finditer(num, line)])
        for line in map_data
    ]
    return Map(
        map_name,
        map_numbers,
    )


def parse(puzzle_input: str) -> tuple[list[int], list[Map]]:
    [seeds_r, *maps_r] = puzzle_input.split("\n\n")
    seeds = [int(seed.group()) for seed in re.finditer(num, seeds_r)]
    maps = list(map(parse_map, maps_r))
    return seeds, maps


def part_1(puzzle_input: str = p1) -> int:
    """"""
    seeds, maps = parse(puzzle_input)
    locations = list(
        reduce(lambda pos, seed_map: get_map_pos(pos, seed_map), maps, seed)
        for seed in seeds
    )
    return min(locations)


def get_range_pos_inv(map_range: MapRange, pos: int) -> int | None:
    if not map_range.dest <= pos < map_range.dest + map_range.length:
        # Out of bounds
        return None
    return map_range.src + (pos - map_range.dest)


def part_2(puzzle_input: str = p1) -> int:
    """"""
    seeds, maps = parse(puzzle_input)
    seed_ranges = [range(seed, seed + length) for (seed, length) in batched(seeds, 2)]
    print("Start part 2")
    for loc in count():
        # Back search
        seed = reduce(
            lambda pos, seed_map: get_map_pos(pos, seed_map, get_range_pos_inv),
            reversed(maps),
            loc,
        )
        # Check if loc is in any of the ranges
        # print(f"{seed} -> {loc}")
        if any(r.start <= seed <= r.stop for r in seed_ranges):
            return loc
    return 0
