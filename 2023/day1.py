import string
import re


def problem_a(data):
    lines = data.split("\n")

    line_digits = []
    for l in lines:
        # First perform forward traversal for first digit
        first = 0
        last = 0
        for c in l:
            if c in string.digits:
                first = int(c)
                break

        # Backwards traversal for last digit. Maybe more efficient than
        # full traversal if the string is long
        for c in l[::-1]:
            if c in string.digits:
                last = int(c)
                break

        line_digits.append(first * 10 + last)

    return sum(line_digits)


def problem_b(data):
    digits = {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
    }
    digit_strs = list(digits.keys()) + [str(x) for x in digits.values()]
    # https://stackoverflow.com/questions/11430863/how-to-find-overlapping-matches-with-a-regexp
    pat = re.compile(r"(?=({}))".format("|".join(digit_strs)))

    lines = data.split("\n")
    line_digits = []

    def maybe_decode(val):
        if val in string.digits:
            return int(val)
        else:
            return digits[val]

    for l in lines:
        matches = re.findall(pat, l)
        if matches:
            first = maybe_decode(matches[0])
            last = maybe_decode(matches[-1])
            line_digits.append(first * 10 + last)

    return sum(line_digits)


# TEST
import unittest


class TestProblem1(unittest.TestCase):
    def test_samples_a(self):
        data = """1abc2
               pqr3stu8vwx
               a1b2c3d4e5f
               treb7uchet"""
        self.assertEqual(problem_a(data), 142)

    def test_samples_b(self):
        data = """
            two1nine
            eightwothree
            abcone2threexyz
            xtwone3four
            4nineeightseven2
            zoneight234
            7pqrstsixteen"""

        res = problem_b(data)
        self.assertEqual(res, 281)

    # https://www.reddit.com/r/adventofcode/comments/1884fpl/2023_day_1for_those_who_stuck_on_part_2/
    def test_samples_b_ex(self):
        data = """
            eighthree
            sevenine
        """
        # 83 + 79 = 162
        res = problem_b(data)
        self.assertEqual(res, 162)


if __name__ == "__main__":
    unittest.main()
