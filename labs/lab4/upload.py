import boto3
import requests
import sys
import os

def download_file(url, filename):
    """Downloads a file from a given URL and saves it locally."""
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(filename, "wb") as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        print(f"File downloaded: {filename}")
    else:
        print("Failed to download file")
        sys.exit(1)

def upload_to_s3(filename, bucket):
    """Uploads a file to the specified S3 bucket."""
    s3 = boto3.client("s3")
    try:
        s3.upload_file(filename, bucket, os.path.basename(filename))
        print(f"File uploaded to S3: s3://{bucket}/{os.path.basename(filename)}")
    except Exception as e:
        print(f"Upload failed: {e}")
        sys.exit(1)

def generate_presigned_url(bucket, filename, expires_in):
    """Generates a presigned URL for the uploaded file."""
    s3 = boto3.client("s3")
    try:
        url = s3.generate_presigned_url(
            "get_object",
            Params={
                "Bucket": bucket,
                "Key": filename,
                "ResponseContentType": "image/*",
                "ResponseContentDisposition": "inline"
            },
            ExpiresIn=int(expires_in),
        )
        return url
    except Exception as e:
        print(f"Failed to generate presigned URL: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script.py <file_url> <bucket_name> <expires_in>")
        sys.exit(1)

    file_url = sys.argv[1]
    bucket_name = sys.argv[2]
    expires_in = sys.argv[3]

    file_name = file_url.split("/")[-1]

    download_file(file_url, file_name)
    upload_to_s3(file_name, bucket_name)
    presigned_url = generate_presigned_url(bucket_name, file_name, expires_in)

    print(f"Presigned URL (expires in {expires_in} seconds):\n{presigned_url}")
