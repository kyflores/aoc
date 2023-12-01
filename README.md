# aoc
Advent of Code

## Usage
```
usage: runner.py [-h] [-i INPUT] [-b] [-t] problem

positional arguments:
  problem               Problem number. Pass like 17-a

options:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Path to input file. It will be loaded as a string.
  -b, --bench           Benchmark the solution.
  -t, --test            Run tests
```

Follow these naming conventions for runner to work.
* `day#.py` for filenames
* `problem_{a,b}` for problem functions
* `TestProblem` for test cases

## Goals
* Learn more advanced python features:
  * generators
  * context managers
  * decorators
