import re
from textwrap import dedent


class Mapping:
    def __init__(self, ranges):
        self.ranges = ranges

    def __call__(self, x):
        for dst, src, rl in self.ranges:
            if (x >= src) and (x <= (src + rl)):
                diff = x - src
                return dst + diff

        return x


def build(data):
    lines = data.split("\n\n")
    seeds = [int(x) for x in lines[0].split(" ")[1:]]
    res = {"seeds": seeds, "mappings": {}}
    for mapping in lines[1:]:
        v = {}
        lines = mapping.split("\n")
        match = re.search(r"(\w+)-to-(\w+) map:", lines[0])
        from_t, to_t = (match[1], match[2])

        v.update({"from": from_t, "to": to_t})

        ranges = []
        for l in lines[1:]:
            ranges.append([int(x) for x in l.split(" ")])

        v["fn"] = Mapping(ranges)
        res["mappings"][from_t] = v

    return res


# We need to come up with a way to generate the seeds incrementally
# as they will fill up memory if created before hand
def expand_seeds(seeds):
    starts = seeds[::2]
    lens = seeds[1::2]
    pairs = zip(starts, lens)

    outs = []
    for start, ln in pairs:
        outs.append(range(start, start + ln))

    return outs


def problem_a(data):
    res = build(data.strip("\n"))

    out = []
    for s in res["seeds"]:
        key = "seed"
        tmp = s
        while key != "location":
            tmp = res["mappings"][key]["fn"](tmp)
            key = res["mappings"][key]["to"]
        out.append(tmp)

    return min(out)


class HandleRange:
    def __init__(self, lookup):
        self.lookup = lookup

    def __call__(self, rn):
        curr_min = float("inf")
        for s in rn:
            key = "seed"
            tmp = s
            while key != "location":
                tmp = self.lookup["mappings"][key]["fn"](tmp)
                key = self.lookup["mappings"][key]["to"]
            curr_min = min(tmp, curr_min)
        return curr_min


def problem_b(data):
    res = build(data.strip("\n"))

    print("expand")
    seeds = expand_seeds(res["seeds"])
    # print(seeds)

    from multiprocessing import Pool

    print("loop")

    handler = HandleRange(res)
    # for seed_range in seeds:
    with Pool(12) as p:
        out = p.map(handler, seeds)

    print(out)

    return min(out)


# TEST
import unittest


class TestProblem(unittest.TestCase):
    def test_samples_a(self):
        data = dedent(
            """\
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
            56 93 4"""
        )
        res = problem_a(data)
        self.assertEqual(res, 35)

    def test_samples_b(self):
        data = dedent(
            """\
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
            56 93 4"""
        )
        res = problem_b(data)
        self.assertEqual(res, 46)


if __name__ == "__main__":
    unittest.main()
