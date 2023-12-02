import re

example = {
    # Game number
    "id": 0,
    "games": [{"red": 0, "blue": 0, "green": 0}],
}


def handle_line(line, fill=0):
    id_part, games = line.split(":")
    games = games.split(";")

    id_match = re.match(r"(?P<game>Game )(?P<id>[0-9]+)", id_part)["id"]

    res = {"id": int(id_match), "games": []}
    for g in games:
        v = {"red": fill, "blue": fill, "green": fill}
        r_match = re.search(r"(?P<num>[0-9]+) red", g)
        if r_match:
            v["red"] = int(r_match["num"])

        b_match = re.search(r"(?P<num>[0-9]+) blue", g)
        if b_match:
            v["blue"] = int(b_match["num"])

        g_match = re.search(r"(?P<num>[0-9]+) green", g)
        if g_match:
            v["green"] = int(g_match["num"])

        res["games"].append(v)

    return res


def problem_a(data):
    r = 12
    g = 13
    b = 14

    ids = []
    lines = data.strip("\n").split("\n")

    for l in lines:
        v = handle_line(l.strip())

        def check_game(game):
            return (game["red"] <= r) and (game["green"] <= g) and (game["blue"] <= b)

        valid = [check_game(x) for x in v["games"]]
        if all(valid):
            ids.append(v["id"])

    return sum(ids)


def problem_b(data):
    ids = []
    lines = data.strip("\n").split("\n")

    powers = []
    for l in lines:
        v = handle_line(l.strip(), fill=0)

        r_m = 0
        g_m = 0
        b_m = 0

        for game in v["games"]:
            r_m = max(r_m, game["red"])
            g_m = max(g_m, game["green"])
            b_m = max(b_m, game["blue"])

        power = r_m * g_m * b_m
        powers.append(power)

    return sum(powers)


# TEST
import unittest


class TestProblem(unittest.TestCase):
    def test_handle_line(self):
        line = "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green"
        res = handle_line(line)

        sample = {
            "id": 1,
            "games": [
                {"red": 4, "blue": 3, "green": 0},
                {"red": 1, "blue": 6, "green": 2},
                {"red": 0, "blue": 0, "green": 2},
            ],
        }

        self.assertEqual(res, sample)

    def test_samples_a(self):
        data = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
                  Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
                  Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
                  Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
                  Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""
        res = problem_a(data)
        self.assertEqual(res, 8)

    def test_samples_b(self):
        data = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
                  Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
                  Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
                  Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
                  Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""
        res = problem_b(data)
        self.assertEqual(res, 2286)

    def test_samples_b_ex(self):
        # Green never appears and is zero.
        data = """Game 1: 3 blue, 4 red; 1 red, 2 blue; 2 blue"""
        res = problem_b(data)
        self.assertEqual(res, 0)


if __name__ == "__main__":
    unittest.main()
