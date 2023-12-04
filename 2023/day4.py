from textwrap import dedent
import re
import functools


def index_have(s):
    matches = re.findall(r"\d+", s)
    return {int(m): i for i, m in enumerate(matches)}


def problem_a(data):
    lines = data.strip("\n").split("\n")
    lines = [x.split(":")[1].split("|") for x in lines]

    out = []
    for wins, have in lines:
        index = index_have(have)

        wins = [int(x) for x in re.findall(r"\d+", wins)]
        total = sum([(1 if (index.get(x) is not None) else 0) for x in wins])
        val = int(2 ** (total - 1))  # Int conversion truncates 0.5 to 0 point value
        out.append(val)

    return sum(out)


def problem_b(data):
    # First preprocess all the lines into one data structure.
    all_cards = []
    lines = data.strip("\n").split("\n")
    lines = [x.split(":")[1].split("|") for x in lines]
    for ix, (left, right) in enumerate(lines, start=1):
        right = index_have(right)
        left = [int(x) for x in re.findall(r"\d+", left)]
        # total = sum([(1 if (right.get(x) is not None) else 0) for x in right])
        all_cards.append({"ix": ix, "left": left, "right": right})

    # Cards is just one line when first called, but will expand as we recurse
    @functools.cache
    def count(card_ix) -> int:
        card = all_cards[card_ix]
        total = [(1 if (card["right"].get(x) is not None) else 0) for x in card["left"]]
        total = sum(total)
        # print("Card {} had {} matches".format(card, total))

        # If this card had no matches, return immediately as the base case.
        if total == 0:
            return 0

        dups_total = 0
        for x in all_cards[card["ix"] : card["ix"] + total]:
            dups_total += count(x["ix"] - 1)

        return total + dups_total

    # Since my recursive function only counts the dups that result from a given card,
    # we start the count at len(all_cards) to include the ones we already start with.
    out = len(all_cards)
    for c in range(len(all_cards)):
        res = count(c)
        out += res

    return out


# TEST
import unittest


class TestProblem(unittest.TestCase):
    def test_samples_a(self):
        data = dedent(
            """\
            Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
            Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
            Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
            Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
            Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
            Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
            """
        )
        res = problem_a(data)

        self.assertEqual(res, 13)

    def test_samples_b(self):
        data = dedent(
            """\
            Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
            Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
            Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
            Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
            Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
            Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
            """
        )
        res = problem_b(data)
        self.assertEqual(res, 30)


if __name__ == "__main__":
    unittest.main()
