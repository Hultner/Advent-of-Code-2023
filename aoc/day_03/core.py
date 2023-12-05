"""
Advent of Code - Day 03

--- Day 3: Gear Ratios ---
You and the Elf eventually reach a gondola lift station; he says the gondola
lift will take you up to the water source, but this is as far as he can bring
you. You go inside.

It doesn't take long to find the gondolas, but there seems to be a problem:
they're not moving.

"Aaah!"

You turn around to see a slightly-greasy Elf with a wrench and a look of
surprise. "Sorry, I wasn't expecting anyone! The gondola lift isn't working
right now; it'll still be a while before I can fix it." You offer to help.

The engineer explains that an engine part seems to be missing from the engine,
but nobody can figure out which one. If you can add up all the part numbers in
the engine schematic, it should be easy to work out which part is missing.

The engine schematic (your puzzle input) consists of a visual representation of
the engine. There are lots of numbers and symbols you don't really understand,
but apparently any number adjacent to a symbol, even diagonally, is a "part
number" and should be included in your sum. (Periods (.) do not count as a
symbol.)

Here is an example engine schematic:

467..114..
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
from re import finditer
from more_itertools import partition
from typing import NamedTuple, Iterator
from operator import mul

from aoc.day_03.seed import p1


class Token(NamedTuple):
    type: str
    value: str | int
    line: int
    column: int


def tokenizer(raw_data: str) -> Iterator[Token]:
    token_specification = (
        ("NUMBER", r"\d+"),
        ("SYMBOL", r"[^\d\n.]"),
        ("NEWLINE", r"\n"),
    )
    token_pattern = "|".join(
        f"(?P<{group}>{pattern})" for group, pattern in token_specification
    )
    line_num = 1
    line_start = 0
    for match in finditer(token_pattern, raw_data):
        kind = match.lastgroup
        value: str | int = match.group()
        column = match.start() - line_start
        match kind:
            case "NUMBER":
                value = int(value)
            case "SYMBOL":
                # We will use the value directly
                pass
            case "NEWLINE":
                line_start = match.end()
                line_num = line_num + 1
                continue
            case _:
                raise ValueError("Unhandled token")
        yield Token(kind, value, line_num, column)


def is_adjacent(number: Token, symbol: Token) -> bool:
    # Collision detection
    return bool(
        # Make sure line is in allowed range, +2 for inclusive comparison
        number.line in range(symbol.line - 1, symbol.line + 2)
        and
        # If any columns of the numbers intersect with symbol column ±1
        set(range(number.column, number.column + len(str(number.value))))
        & set(range(symbol.column - 1, symbol.column + 2))
    )


def part_1(puzzle_input: str = p1) -> int:
    """
    In this schematic, two numbers are not part numbers because they are not
    adjacent to a symbol: 114 (top right) and 58 (middle right). Every other
    number is adjacent to a symbol and so is a part number; their sum is 4361.

    Of course, the actual engine schematic is much larger. What is the sum of
    all of the part numbers in the engine schematic?
    """
    tokens = tokenizer(puzzle_input)
    # Split up the tokens to reduce unecessary filtering in search
    (symbol_gen, numbers) = partition(lambda t: t.type == "NUMBER", tokens)
    symbols = list(symbol_gen)  # We iterate per number
    part_numbers: Iterator[int] = (
        int(number.value)
        for number in numbers
        if any(is_adjacent(number, symbol) for symbol in symbols)
    )
    return sum(part_numbers)


def part_2(puzzle_input: str = p1) -> int:
    """
    --- Part Two ---
    The engineer finds the missing part and installs it in the engine! As the
    engine springs to life, you jump in the closest gondola, finally ready to
    ascend to the water source.

    You don't seem to be going very fast, though. Maybe something is still
    wrong? Fortunately, the gondola has a phone labeled "help", so you pick it
    up and the engineer answers.

    Before you can explain the situation, she suggests that you look out the
    window. There stands the engineer, holding a phone in one hand and waving
    with the other. You're going so slowly that you haven't even left the
    station. You exit the gondola.

    The missing part wasn't the only issue - one of the gears in the engine is
    wrong. A gear is any * symbol that is adjacent to exactly two part numbers.
    Its gear ratio is the result of multiplying those two numbers together.

    This time, you need to find the gear ratio of every gear and add them all
    up so that the engineer can figure out which gear needs to be replaced.

    Consider the same engine schematic again:

    467..114..
    ...*......
    ..35..633.
    ......#...
    617*......
    .....+.58.
    ..592.....
    ......755.
    ...$.*....
    .664.598..

    In this schematic, there are two gears. The first is in the top left; it
    has part numbers 467 and 35, so its gear ratio is 16345. The second gear is
    in the lower right; its gear ratio is 451490. (The * adjacent to 617 is not
    a gear because it is only adjacent to one part number.) Adding up all of
    the gear ratios produces 467835.

    What is the sum of all of the gear ratios in your engine schematic?
    """
    tokens = tokenizer(puzzle_input)
    # Split up the tokens to reduce unecessary filtering in search
    (symbol_gen, number_gen) = partition(lambda t: t.type == "NUMBER", tokens)
    numbers = list(number_gen)
    gears = (
        mul(*cogs)
        for gear in symbol_gen
        if gear.value == "*"
        and len(cogs := [cog.value for cog in numbers if is_adjacent(cog, gear)]) == 2
    )
    return sum(gears)
