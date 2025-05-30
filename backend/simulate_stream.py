#!/usr/bin/env python3
"""
Edge‐agent simulator: uploads all images from a local directory to an S3 bucket.
"""
import os
import time
import argparse
import boto3

def load_dotenv(dotenv_path: str = '.env') -> None:
    """
    Simple .env loader: parse KEY=VALUE pairs and set them into os.environ
    if they aren’t already defined.
    """
    try:
        with open(dotenv_path, encoding='utf-8') as f:
            for raw_line in f:
                line = raw_line.strip()
                # skip comments and blank lines
                if not line or line.startswith('#') or '=' not in line:
                    continue
                key, _, val = line.partition('=')
                key = key.strip()
                val = val.strip().strip('\'"')
                # don’t overwrite existing env vars
                if key and key not in os.environ:
                    os.environ[key] = val
    except FileNotFoundError:
        # .env not found: nothing to load
        pass

def upload_images(directory: str, bucket: str, prefix: str, interval: float):
    """
    Uploads every .jpg/.jpeg/.png in `directory` to S3 bucket `bucket`,
    under an optional key prefix, waiting `interval` seconds between uploads.
    """
    s3 = boto3.client('s3')
    for filename in sorted(os.listdir(directory)):
        if not filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            continue

        local_path = os.path.join(directory, filename)
        s3_key = f"{prefix.rstrip('/')}/{filename}" if prefix else filename

        print(f"Uploading {local_path} → s3://{bucket}/{s3_key} ...", end=' ')
        try:
            s3.upload_file(local_path, bucket, s3_key)
            print("✓ Success")
        except Exception as e:
            print(f"✗ Failed: {e}")

        time.sleep(interval)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Simulate edge‐agent: upload a stream of images to S3."
    )
    parser.add_argument(
        '--dir', required=True,
        help='Local directory containing images.'
    )
    parser.add_argument(
        '--bucket', required=True,
        help='Target S3 bucket name.'
    )
    parser.add_argument(
        '--prefix', default='',
        help='S3 key prefix (e.g. shelf-images/).'
    )
    parser.add_argument(
        '--interval', type=float, default=1.0,
        help='Seconds to wait between uploads.'
    )
    args = parser.parse_args()

    # Load AWS credentials (and any other vars) from .env into os.environ
    load_dotenv()

    upload_images(
        directory=args.dir,
        bucket=args.bucket,
        prefix=args.prefix,
        interval=args.interval
    )
