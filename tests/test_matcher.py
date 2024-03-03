from pathlib import Path

import polars as pl
import polars.testing

from jobmatcher.matcher import match_jobs_from_csv, match_to_jobs


def test_match_jobs_from_file():
    sample_data_dir = Path(__file__).parent / "sample_data"
    matched = match_jobs_from_csv(sample_data_dir / "jobseekers.csv", sample_data_dir / "jobs.csv")
    polars.testing.assert_frame_equal(matched, pl.read_csv(sample_data_dir / "result.csv"), check_dtype=False)


def test_match_to_jobs():
    jobseekers = pl.DataFrame({"jobseeker_id": [1, 2], "skills": [["polars", "SQL"], ["polars", "R"]]})
    jobs = pl.DataFrame({"job_id": [1, 2], "required_skills": [["polars", "SQL"], ["R", "SQL"]]}).with_columns(
        pl.col("required_skills").list.len().alias("num_skills")
    )
    matched = match_to_jobs(jobseekers, jobs)
    sorted_matched = matched.sort(["jobseeker_id", "job_id"])  # don't care about order from match_to_jobs
    expected = pl.DataFrame(
        {
            "jobseeker_id": [1, 1, 2, 2],
            "job_id": [1, 2, 1, 2],
            "matching_skill_count": [2, 1, 1, 1],
            "required_skill_count": [2, 2, 2, 2],
            "matching_skill_percent": [100.0, 50.0, 50.0, 50.0],
        }
    )
    polars.testing.assert_frame_equal(sorted_matched, expected, check_dtype=False)
