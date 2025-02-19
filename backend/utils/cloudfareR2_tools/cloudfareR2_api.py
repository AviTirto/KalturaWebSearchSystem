import os
import boto3
from dotenv import load_dotenv
import io

# Load environment variables
load_dotenv()

# Cloudflare R2 Credentials
CLOUDFARE_R2_ENDPOINT = os.getenv("CLOUDFARE_R2_ENDPOINT")
CLOUDFARE_R2_SECRET_KEY = os.getenv("CLOUDFARE_R2_SECRET_KEY") 
CLOUDFARE_R2_BUCKET_NAME = os.getenv("CLOUDFARE_R2_BUCKET_NAME")
CLOUDFARE_R2_ACCESS_KEY = os.getenv("CLOUDFARE_R2_ACCESS_KEY")

def get_cloudfareR2():
    """Returns an S3-compatible client for Cloudflare R2."""
    return boto3.client(
        's3',
        endpoint_url=CLOUDFARE_R2_ENDPOINT,
        aws_access_key_id=CLOUDFARE_R2_ACCESS_KEY,
        aws_secret_access_key=CLOUDFARE_R2_SECRET_KEY,
        region_name='us-east-1'
    )

def upload_file(r2_client, file_data, object_key: str):
    """Uploads a file to Cloudflare R2 from file data."""
    try:
        # Upload file from the data (assuming 'file_data' is a binary stream)
        r2_client.put_object(Bucket=CLOUDFARE_R2_BUCKET_NAME, Key=object_key, Body=file_data)
        return {"status": "success", "message": f"Uploaded file with key: {object_key}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def download_file(r2_client, object_key: str):
    """Downloads a file from Cloudflare R2."""
    try:
        # Get the file object from R2
        response = r2_client.get_object(Bucket=CLOUDFARE_R2_BUCKET_NAME, Key=object_key)
        file_content = io.BytesIO(response['Body'].read())  # This contains the file data (as bytes)
        return {"status": "success", "file_data": file_content}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def delete_file(r2_client, object_key: str):
    """Deletes a file from Cloudflare R2."""
    try:
        r2_client.delete_object(Bucket=CLOUDFARE_R2_BUCKET_NAME, Key=object_key)
        return {"status": "success", "message": f"Deleted file with key: {object_key}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def list_files(r2_client):
    """Lists all files in the R2 bucket."""
    try:
        response = r2_client.list_objects_v2(Bucket=CLOUDFARE_R2_BUCKET_NAME)
        files = [item['Key'] for item in response.get('Contents', [])]
        return {"status": "success", "files": files}
    except Exception as e:
        return {"status": "error", "message": str(e)}
