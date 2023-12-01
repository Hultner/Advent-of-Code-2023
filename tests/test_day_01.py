from typing import Any

from aoc.day_01.core import part_1, part_2, construct_calibration_number

sample_seed_1 = (
    "1abc2",
    "pqr3stu8vwx",
    "a1b2c3d4e5f",
    "treb7uchet",
)
sample_seed_2 = (
    "two1nine",
    "eightwothree",
    "abcone2threexyz",
    "xtwone3four",
    "4nineeightseven2",
    "zoneight234",
    "7pqrstsixteen",
)


# Not done anything with these yet
partial_answers = (
    12,
    38,
    15,
    77,
)

answers = (
    142,
    142,
)


def test_parts() -> None:
    # Oracle says so
    # Used to prevent regressions when refactoring after after a part is done.
    assert part_1() == 55123
    assert part_2() > 54751
    assert part_2() == 55260


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
    assert part_2(sample_seed_2) == 281


def test_calibration_construction() -> None:
    for value, answer in zip(sample_seed_1, partial_answers):
        assert construct_calibration_number(value) == answer
