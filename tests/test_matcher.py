from pathlib import Path

import polars as pl
import polars.testing

from jobmatcher.matcher import match_jobs_from_csv


def test_match_jobs_from_file():
    sample_data_dir = Path(__file__).parent / "sample_data"
    matched = match_jobs_from_csv(sample_data_dir / "jobs.csv", sample_data_dir / "jobseekers.csv")
    polars.testing.assert_frame_equal(matched.head(6), pl.read_csv(sample_data_dir / "result_head.csv"))
