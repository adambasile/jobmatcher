import argparse
import sys

from jobmatcher.matcher import match_jobs_from_csv

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="jobmatcher",
        description=(
            "Matches jobseekers to jobs on the basis of the proportion of skills in the job that the "
            "jobseeker possesses"
        ),
    )
    parser.add_argument(
        "--jobseekers", type=str, help='Path to csv with ["id", "name", "skills"] columns', required=True
    )
    parser.add_argument(
        "--jobs", type=str, help='Path to csv with ["id", "title", "required_skills"] columns', required=True
    )
    parser.add_argument(
        "--output", type=str, help="Path to output csv. If omitted output will be sent to stdout", default=sys.stdout
    )
    args = parser.parse_args()
    matched = match_jobs_from_csv(args.jobseekers, args.jobs)
    matched.write_csv(args.output)
