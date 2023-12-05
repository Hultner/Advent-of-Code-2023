from typing import Any

from aoc.day_05.core import part_1, part_2, get_map_pos, parse
from itertools import accumulate

sample_seed_1 = """
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
""".strip()

answers = (
    35,
    46,
)

seed_to_soil = (
    (79, 81),
    (14, 14),
    (55, 57),
    (13, 13),
)

# Seed, soil, fertilizer, water, light, temperature, humidity, location
seed_path_to_location = (
    # Seed 79, soil 81, fertilizer 81, water 81, light 74, temperature 78, humidity 78, location 82.
    (79, 81, 81, 81, 74, 78, 78, 82),
    # Seed 14, soil 14, fertilizer 53, water 49, light 42, temperature 42, humidity 43, location 43.
    (14, 14, 53, 49, 42, 42, 43, 43),
    # Seed 55, soil 57, fertilizer 57, water 53, light 46, temperature 82, humidity 82, location 86.
    (55, 57, 57, 53, 46, 82, 82, 86),
    # Seed 13, soil 13, fertilizer 52, water 41, light 34, temperature 34, humidity 35, location 35.
    (13, 13, 52, 41, 34, 34, 35, 35),
)


def test_sub_parts() -> None:
    seeds, maps = parse(sample_seed_1)
    for seed, *path, dest in seed_path_to_location:
        travel = accumulate(
            func=lambda pos, seed_map: get_map_pos(pos, seed_map),
            iterable=maps,
            initial=seed,
        )
        assert list(travel) == [seed, *path, dest]


# def test_sub_parts_2() -> None:
#     seeds, maps = parse(sample_seed_1)
#     for seed, *path, dest in seed_path_to_location:
#         travel = accumulate(
#             func=lambda pos, seed_map: get_map_pos(pos, seed_map),
#             iterable=maps,
#             initial=seed,
#         )
#         assert list(travel) == [seed, *path, dest]


def test_parts() -> None:
    # Oracle says so
    #                   25316841
    assert part_1() == 486613012
    # assert part_2() == 56931769
    pass


def verify_day(data: Any, expected_1: Any, expected_2: Any) -> None:
    assert part_1(data) == expected_1
    assert part_2(data) == expected_2


def test_samples() -> None:
    """
    Tests the given examples
    """
    examples = ((sample_seed_1, answers),)

    for data, expected in examples:
        verify_day(data, *expected)
