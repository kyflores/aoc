# TEMPLATE

from textwrap import dedent


def problem_a(data):
    lines = data.split("\n")
    return "a"


def problem_b(data):
    lines = data.split("\n")
    return "b"


# TEST
import unittest


class TestProblem(unittest.TestCase):
    def test_samples_a(self):
        data = dedent(
            """\
            """
        )
        self.assertEqual(True, True)

    def test_samples_b(self):
        self.assertEqual(True, True)


if __name__ == "__main__":
    unittest.main()
