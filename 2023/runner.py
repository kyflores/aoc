import argparse
import importlib
import timeit
import unittest

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("problem", help="Problem number. Pass like 17-a", type=str)
    parser.add_argument(
        "-i",
        "--input",
        help="Path to input file. It will be loaded as a string.",
        type=str,
    )
    parser.add_argument(
        "-b", "--bench", help="Benchmark the solution.", action="store_true"
    )
    parser.add_argument("-t", "--test", help="Run tests", action="store_true")

    opt = parser.parse_args()

    num, part = opt.problem.split("-")
    try:
        num = int(num)
        if not (part == "a" or part == "b"):
            raise Exception("Bad part string.")
    except Exception as e:
        print(e)
        exit(1)

    with open(opt.input, "r") as f:
        inputs = f.read()

    mod = importlib.import_module("day{}".format(num))
    fn = getattr(mod, "problem_{}".format(part))

    if opt.bench:
        runs = 1000
        times = timeit.timeit(stmt="fn(inputs)", globals=globals(), number=runs)
        print("{} iters/sec".format(runs / times))
        exit(0)

    if opt.test:
        tests = getattr(mod, "TestProblem")

        runner = unittest.TextTestRunner()
        runner.run(unittest.makeSuite(tests))
        exit(0)

    res = fn(inputs)
    print(res)
