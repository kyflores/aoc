import argparse
import importlib

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("problem", help="Problem number. Pass like 17-a", type=str)
    parser.add_argument(
        "input_filename",
        help="Path to input file. It will be loaded as a string.",
        type=str,
    )

    opt = parser.parse_args()

    num, part = opt.problem.split("-")
    try:
        num = int(num)
        if not (part == "a" or part == "b"):
            raise Exception("Bad part string.")
    except Exception as e:
        print(e)
        exit(1)

    with open(opt.input_filename, "r") as f:
        inputs = f.read()

    mod = importlib.import_module("day{}".format(num))
    top = getattr(mod, "problem_{}".format(part))
    res = top(inputs)
    print(res)
