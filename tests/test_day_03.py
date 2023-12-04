from typing import Any

from aoc.day_03.core import part_1, part_2

sample_seed_1 = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
"""

answers = (
    4361,
    467835,
)


def test_parts() -> None:
    # Oracle says so
    assert part_1() == 521601
    assert part_2() == 80694070


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
