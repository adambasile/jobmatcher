# jobmatcher

-----

**Table of Contents**

- [Installation](#installation)
- [Usage](#Usage)
- [Developing](#Developing)
- [License](#license)

## Installation

```console
pip install git+https://github.com/adambasile/jobmatcher.git
```

## Usage

```console
$ python -m jobmatcher -h

usage: jobmatcher [-h] --jobseekers JOBSEEKERS --jobs JOBS [--output OUTPUT]

Matches jobseekers to jobs on the basis of the proportion of skills in the job that the jobseeker possesses

options:
  -h, --help            show this help message and exit
  --jobseekers JOBSEEKERS
                        Path to csv with ["id", "name", "skills"] columns
  --jobs JOBS           Path to csv with ["id", "title", "required_skills"] columns
  --output OUTPUT       Path to output csv. If omitted output will be sent to stdout.

```

## Developing

The following linters and checkers are run on the code

```console
black .
ruff check
mypy src
```

`pytest` is used to run tests. Make sure you run it from project root

```console
pytest
```

Run it with `coverage` to get a report on test coverage

```console
$ coverage run -m pytest
$ coverage report
Name                         Stmts   Miss Branch BrPart  Cover
--------------------------------------------------------------
src\jobmatcher\__init__.py       0      0      0      0   100%
src\jobmatcher\__main__.py       3      3      0      0     0%
src\jobmatcher\matcher.py       29      0      0      0   100%
tests\__init__.py                0      0      0      0   100%
tests\test_matcher.py            8      0      0      0   100%
--------------------------------------------------------------
TOTAL                           40      3      0      0    92%
```

`requirements.txt` is generated from `requirements-dev.in` using `uv`

```console
uv pip compile requirements-dev.in -o requirements.txt
```

## License

`jobmatcher` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
