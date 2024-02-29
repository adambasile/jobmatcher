from __future__ import annotations

from os import PathLike
from typing import Any

import polars as pl


def match_jobs_from_csv(jobseekers_csv: PathLike[Any], jobs_csv: PathLike[Any]) -> pl.DataFrame:
    jobseekers = pl.read_csv(jobseekers_csv)
    jobs = pl.read_csv(jobs_csv)
    matched = match_jobs_from_frames(jobseekers, jobs)
    return matched


def match_jobs_from_frames(jobseekers: pl.DataFrame, jobs: pl.DataFrame) -> pl.DataFrame:
    pass
