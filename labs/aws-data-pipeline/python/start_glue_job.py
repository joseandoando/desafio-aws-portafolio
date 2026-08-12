import argparse

import boto3


def start_job(job_name: str, source_path: str, target_path: str) -> str:
    glue = boto3.client("glue")
    response = glue.start_job_run(
        JobName=job_name,
        Arguments={
            "--SOURCE_PATH": source_path,
            "--TARGET_PATH": target_path,
        },
    )
    return response["JobRunId"]


def main() -> None:
    parser = argparse.ArgumentParser(description="Start an AWS Glue ETL job")
    parser.add_argument("--job-name", required=True)
    parser.add_argument("--source", required=True, help="Example: s3://bucket/raw/")
    parser.add_argument("--target", required=True, help="Example: s3://bucket/curated/")
    args = parser.parse_args()

    run_id = start_job(args.job_name, args.source, args.target)
    print(f"Glue job started. Run ID: {run_id}")


if __name__ == "__main__":
    main()
