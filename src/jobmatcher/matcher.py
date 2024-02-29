from __future__ import annotations

from pathlib import Path
from typing import Tuple, TypeAlias

import polars as pl

Pathlike: TypeAlias = str | Path


def match_jobs_from_csv(jobseekers_csv: Pathlike, jobs_csv: Pathlike) -> pl.DataFrame:
    """
    Matches jobseekers to jobs on the basis of the proportion of skills in the job that the jobseeker possesses

    Returns dataframe sorted by the jobseeker id ascending, matching skill percent descending and job id ascending
    :param jobseekers_csv:
        path to csv with three columns: ["id", "name", "skills"], where skills is a comma separated list
    :param jobs_csv:
        path to csv with three columns: ["id", "title", "required_skills"],
         where required_skills is a comma separated list
    :return: pl.DataFrame with columns:
        ["jobseeker_id" ,"jobseeker_name", "job_id", "job_title", "matching_skill_count", "matching_skill_percent"]
    """
    jobseekers = pl.read_csv(jobseekers_csv)
    jobs = pl.read_csv(jobs_csv)
    matched = match_jobs_from_frames(jobseekers, jobs)
    return matched


def match_jobs_from_frames(jobseekers: pl.DataFrame, jobs: pl.DataFrame) -> pl.DataFrame:
    """
    Matches jobseekers to jobs on the basis of the proportion of skills in the job that the jobseeker possesses

    :param jobseekers:
        pl.DataFrame with columns: ["id", "name", "skills"] where skills is a string containing a comma separated list
    :param jobs:
        pl.DataFrame with columns ["id", "title", "required_skills"]
         where required_skills is a string containing a comma separated list
    :return: pl.DataFrame with columns:
        ["jobseeker_id" ,"jobseeker_name", "job_id", "job_title", "matching_skill_count", "matching_skill_percent"]
    """
    jobseekers, jobs = preprocess_inputs(jobseekers, jobs)
    job_matches = match_to_jobs(jobseekers, jobs)
    return format_for_output(job_matches, jobseekers, jobs)


def preprocess_inputs(jobseekers: pl.DataFrame, jobs: pl.DataFrame) -> Tuple[pl.DataFrame, pl.DataFrame]:
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
    jobseekers = jobseekers.with_columns(split_and_strip("skills"))
    jobs = jobs.with_columns(split_and_strip("required_skills")).with_columns(
        pl.col("required_skills").list.len().alias("num_skills")
    )
    return jobseekers, jobs


def split_and_strip(col: str) -> pl.Expr:
    # this splits on commas and then strips whitespace from each element
    return pl.col(col).str.split(",").list.eval(pl.element().str.strip_chars())


def match_to_jobs(jobseekers: pl.DataFrame, jobs: pl.DataFrame) -> pl.DataFrame:
    """
    Matches jobseekers to jobs on the basis of the proportion of skills in the job that the jobseeker possesses
    :param jobseekers: pl.DataFrame with columns: ["jobseeker_id", "skills"]
    :param jobs: pl.DataFrame with columns: ["job_id", "skills", "num_skills"]
    :return: pl.DataFrame with columns:
         ["jobseeker_id", "job_id", "matching_skill_count", "required_skill_count", "matching_skill_percent"]
    """
    num_matched_skills = (
        jobseekers.explode("skills")
        .join(jobs.explode("required_skills"), left_on="skills", right_on="required_skills")
        .group_by([pl.col("jobseeker_id", "job_id")])
        .agg(pl.len().alias("matching_skill_count"))
        .join(jobs.select(pl.col("job_id"), pl.col("num_skills").alias("required_skill_count")), on="job_id")
        .with_columns(
            ((100 * pl.col("matching_skill_count")) / pl.col("required_skill_count")).alias("matching_skill_percent")
        )
    )
    return num_matched_skills


def format_for_output(job_matches: pl.DataFrame, jobseekers: pl.DataFrame, jobs: pl.DataFrame) -> pl.DataFrame:
    """
    Adds columns to job matches, selects just the ones we want, and sorts them in the order we want
    :param job_matches: pl.DataFrame with columns:
        ["jobseeker_id", "job_id", "matching_skill_count", "required_skill_count", "matching_skill_percent"]
    :param jobseekers: pl.DataFrame with columns: ["jobseeker_id", "jobseeker_name"]
    :param jobs: pl.DataFrame with columns: ["job_id", "job_title"]
    :return: pl.DataFrame with columns:
        ["jobseeker_id", "jobseeker_name", "job_id", "job_title", "matching_skill_count", "matching_skill_percent"]
    """
    messy_output = job_matches.join(jobs, on="job_id").join(jobseekers, on="jobseeker_id")
    pretty_formatted = messy_output.select(
        pl.col(
            "jobseeker_id", "jobseeker_name", "job_id", "job_title", "matching_skill_count", "matching_skill_percent"
        )
    ).sort(
        [pl.col("jobseeker_id"), pl.col("matching_skill_percent"), pl.col("job_id")],
        descending=[False, True, False],
    )
    return pretty_formatted
