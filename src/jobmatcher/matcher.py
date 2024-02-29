from __future__ import annotations

from os import PathLike
from typing import Any

import polars as pl


def match_jobs_from_csv(jobseekers_csv: PathLike[Any], jobs_csv: PathLike[Any]) -> pl.DataFrame:
    """
    :param jobseekers_csv:
        path to csv with three columns: ["id", "name", "skills"], where skills is a comma separated list
    :param jobs_csv:
        path to csv with three columns: ["id", "title", "required_skills"],
         where required_skills is a comma separated list
    :return:
    """
    jobseekers = pl.read_csv(jobseekers_csv)
    jobs = pl.read_csv(jobs_csv)
    matched = match_jobs_from_frames(jobseekers, jobs)
    return matched


def match_jobs_from_frames(jobseekers: pl.DataFrame, jobs: pl.DataFrame) -> pl.DataFrame:
    jobs, jobseekers = reformat_inputs(jobseekers, jobs)

    num_matched_skills = (
        jobseekers.explode("skills")
        .join(jobs.explode("required_skills"), left_on="skills", right_on="required_skills")
        .group_by([pl.col("jobseeker_id", "job_id")])
        .agg(pl.len().alias("matching_skill_count"))
    )

    return (
        num_matched_skills.join(jobs, on="job_id")
        .join(jobseekers, on="jobseeker_id")
        .with_columns(((100 * pl.col("matching_skill_count")) / pl.col("num_skills")).alias("matching_skill_percent"))
        .select(
            pl.col(
                "jobseeker_id",
                "jobseeker_name",
                "job_id",
                "job_title",
                "matching_skill_count",
                "matching_skill_percent",
            )
        )
        .sort(
            [pl.col("jobseeker_id"), pl.col("matching_skill_percent"), pl.col("job_id")],
            descending=[False, True, False],
        )
    )


def reformat_inputs(jobseekers: pl.DataFrame, jobs: pl.DataFrame):
    """
    :param jobseekers:
        pl.DataFrame with columns: ["id", "name", "skills"] where skills is a string containing a comma separated list
    :param jobs:
        pl.DataFrame with columns ["id", "title", "required_skills"]
         where required_skills is a string containing a comma separated list
    :return: Two pl.DataFrames:
        jobseekers pl.DataFrame with ["id", "name"] columns renamed to ["jobseeker_id", "jobseeker_name"],
         and the "skills" column split on commas into a list
        jobs pl.DataFrame with ["id", "title"] columns renamed to ["job_id", "job_name"], the "required_skills" column
         split on commas into a list, and with a "num_skills"" column with the len of the list in "required_skills"
    """
    jobseekers = jobseekers.rename({col: f"jobseeker_{col}" for col in ["id", "name"]})
    jobs = jobs.rename({col: f"job_{col}" for col in ["id", "title"]})
    # split the skills
    # this splits on commas and then strips whitespace from each element
    split = lambda col: pl.col(col).str.split(",").list.eval(pl.element().str.strip_chars())
    jobseekers = jobseekers.with_columns(split("skills"))
    jobs = jobs.with_columns(split("required_skills")).with_columns(
        pl.col("required_skills").list.len().alias("num_skills")
    )
    return jobs, jobseekers
