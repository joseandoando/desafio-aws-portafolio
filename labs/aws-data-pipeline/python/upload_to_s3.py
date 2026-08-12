import argparse
from pathlib import Path

import boto3


def upload_file(bucket: str, file_path: str, prefix: str = "raw") -> str:
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    key = f"{prefix.rstrip('/')}/{path.name}"
    s3 = boto3.client("s3")

    s3.upload_file(str(path), bucket, key)
    return f"s3://{bucket}/{key}"


def main() -> None:
    parser = argparse.ArgumentParser(description="Upload a dataset to the raw S3 zone")
    parser.add_argument("--bucket", required=True, help="Destination S3 bucket")
    parser.add_argument("--file", required=True, help="Local CSV file")
    parser.add_argument("--prefix", default="raw", help="S3 prefix (default: raw)")
    args = parser.parse_args()

    uri = upload_file(args.bucket, args.file, args.prefix)
    print(f"Uploaded successfully: {uri}")


if __name__ == "__main__":
    main()
