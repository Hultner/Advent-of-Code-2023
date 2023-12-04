"""
Advent of Code - Day 04
"""
from typing import NamedTuple, Iterator
import re

from aoc.day_04.seed import p1


class Card(NamedTuple):
    id: int
    card_numbers: set[int]
    winning_numbers: set[int]


def parse(raw_str: str) -> Iterator[Card]:
    # pattern = r"Card (P<id>\d+):(P<card>(\s+(\d+))+) \|(P<winning>(\s+(\d+))+)"
    pattern = r"Card\s+(\d+):((\s+\d+)+) \|((\s+\d+)+)"
    for line in raw_str.splitlines():
        for match in re.findall(pattern, line):
            # Just to make sure double winnings isn't possible
            assert (
                len(set(int(v) for v in match[3].split())) ==
                len(list(int(v) for v in match[3].split()))
            )
            assert (
                len(set(int(v) for v in match[1].split())) ==
                len(list(int(v) for v in match[1].split()))
            )
            yield Card(
                int(match[0]),
                set(int(v) for v in match[1].split()),
                set(int(v) for v in match[3].split()),
            )


def part_1(puzzle_input: str = p1) -> int:
    """"""
    cards = parse(puzzle_input)
    return sum(
            2**(exp-1)
            for card in cards
            if (exp := len(card.winning_numbers & card.card_numbers)) > 0
    )


def part_2(puzzle_input: str = p1) -> int:
    """"""
    cards = list(parse(puzzle_input))
    for card in cards:
        winners = card.winning_numbers & card.card_numbers
        cards += cards[card.id: card.id+len(winners)]
    return len(cards)
