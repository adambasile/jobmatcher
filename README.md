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

Pytest is used to run tests. Make sure you run it from project root

```console
pytest
```

The following linters and checkers are run on the code

```console
black .
ruff check
mypy src
```

## License

`jobmatcher` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
