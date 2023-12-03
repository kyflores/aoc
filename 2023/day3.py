# TEMPLATE

from textwrap import dedent
import re
import math

SYMBOLS = "!@#$%^&*+=-/"


def problem_a(data):
    matrix = data.split("\n")

    mask = []
    for row in matrix:
        mask.append([0] * len(row))

    # Assumption here that all rows of the input are equal length.
    rows = len(matrix)
    cols = len(matrix[0])

    for r in range(1, rows - 1):
        for c in range(1, cols - 1):
            if matrix[r][c] in SYMBOLS:
                mask[r - 1][c - 1] = 1
                mask[r - 1][c] = 1
                mask[r - 1][c + 1] = 1
                mask[r][c - 1] = 1
                mask[r][c] = 1
                mask[r][c + 1] = 1
                mask[r + 1][c - 1] = 1
                mask[r + 1][c] = 1
                mask[r + 1][c + 1] = 1

    outs = []
    for r, row in enumerate(matrix):
        matches = re.finditer(r"(\d)+", row)
        for m in matches:
            acc = 0
            for c in range(m.start(), m.end()):
                acc += mask[r][c]

            if acc > 0:
                outs.append(int(m[0]))

    return sum(outs)


def problem_b(data):
    """
    Locate every gear.
    Generate masks for the gears like in A. Now, instead of placing 0 or 1 in the mask,
    place None or (R, C) of the gear
    Locate all numbers touching a gear, the same way as one, but now we know WHICH gear it is.
    Add the numbers to a dict keyed on the gear's (R, C) tuple
    Scan the gear dict for every gear with two numbers in its values.
    Gears can touch exactly 2 numbers by definition, so reject any gear that has 1 or >2
    """
    matrix = data.split("\n")

    mask = []
    for row in matrix:
        mask.append([None] * len(row))

    # Assumption here that all rows of the input are equal length.
    rows = len(matrix)
    cols = len(matrix[0])

    gears = {}
    for r in range(1, rows - 1):
        for c in range(1, cols - 1):
            if matrix[r][c] == "*":
                v = (r, c)
                gears[v] = []
                mask[r - 1][c - 1] = v
                mask[r - 1][c] = v
                mask[r - 1][c + 1] = v
                mask[r][c - 1] = v
                mask[r][c] = v
                mask[r][c + 1] = v
                mask[r + 1][c - 1] = v
                mask[r + 1][c] = v
                mask[r + 1][c + 1] = v

    # print(mask)
    outs = []
    for r, row in enumerate(matrix):
        matches = re.finditer(r"(\d)+", row)
        for m in matches:
            valid = None
            for c in range(m.start(), m.end()):
                # Note that this does not work if a number touches two gears, but this seems
                # to never happen in the real data because the solution was accepted
                if mask[r][c] is not None:
                    valid = mask[r][c]

            if valid is not None:
                gears[valid].append(int(m[0]))

    # print(gears)
    out = 0
    for g in gears.values():
        if len(g) == 2:
            out += math.prod(g)

    return out


# TEST
import unittest


class TestProblem(unittest.TestCase):
    def test_samples_a(self):
        data = dedent(
            """\
            467..114..
            ...*......
            ..35..633.
            ......#...
            617*......
            .....+.58.
            ..592.....
            ......755.
            ...$.*....
            .664.598.."""
        )

        res = problem_a(data)
        self.assertEqual(res, 4361)

    def test_samples_b(self):
        data = dedent(
            """\
            467..114..
            ...*......
            ..35..633.
            ......#...
            617*......
            .....+.58.
            ..592.....
            ......755.
            ...$.*....
            .664.598.."""
        )

        res = problem_b(data)

        self.assertEqual(res, 467835)


if __name__ == "__main__":
    unittest.main()
