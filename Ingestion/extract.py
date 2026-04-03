from boto3 import client
from dotenv import load_dotenv
from time import sleep
import os

load_dotenv()

textract = client("textract", region_name=os.getenv("AWS_REGION"))
BUCKET = os.environ["S3_BUCKET"]

def extract(filename: str) -> str:
    response = textract.start_document_text_detection(
        DocumentLocation={"S3Object": {"Bucket": BUCKET, "Name": filename}}
    )
    job_id = response["JobId"]

    # Poll until complete
    while True:
        result = textract.get_document_text_detection(JobId=job_id)
        status = result["JobStatus"]
        if status == "SUCCEEDED":
            break
        elif status == "FAILED":
            raise Exception("Textract job failed")
        print(f"Polling | Status: {status} .....")
        sleep(3)

    # Collect lines across all pages
    lines = []
    next_token = None

    while True:
        if next_token:
            result = textract.get_document_text_detection(JobId=job_id, NextToken=next_token)
        else:
            result = textract.get_document_text_detection(JobId=job_id)

        for block in result["Blocks"]:
            if block.get("BlockType") == "LINE" and "Text" in block:
                lines.append(block["Text"])

        next_token = result.get("NextToken")
        if not next_token:
            break

    return "\n".join(lines)


if __name__ == "__main__":
    import sys
    text = extract(sys.argv[1])
    print(text)
    print(f"\n── {len(text):,} chars extracted ──")