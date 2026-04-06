import os
import json
import boto3
from extract import extract
from parser import llmParser
from chunk import chunk
from embed import embed
from db import go_upsert, get_client

def process_document(filename: str):
    print(f"Starting pipeline for: {filename}")
    # --- Step 1: Extract ---
    try:
        extraction_result = extract(filename)
        print(f"Extraction complete. Extracted {len(extraction_result):,} characters.")
    except Exception as e:
        print(f"Extraction failed: {e}")
        return
    # --- Step 2: Parse ---
    try:
        meta_data = llmParser(extraction_result)
        print("Parsing complete.")
    except Exception as e:
        print(f"Parsing failed: {e}")
        return
    # --- Step 3: Chunking ---
    try:
        chunks = chunk(extraction_result, meta_data, meta_data["general_order"])
    except Exception as e:
        print(f"chunking failed: {e} ")
        return

    # --- Step 4: Embedding ---
    try: 
        embedded_chunks = embed(chunks)
    except Exception as e:
        print(f"embedding failed: {e}")
        return
        
    # --- Step 4: db upsert ---
    try: 
        go_upsert(chunks)
    except Exception as e:
        print(f"supabase upsert failed: {e}")
        return

    # --- Step 3: Output ---
    print(f"\n Insertion of Go {chunks[0]["go_id"]} completed")
    
if __name__ == "__main__":
    bucket = os.environ["S3_BUCKET"]
    s3 = boto3.client("s3", region_name=os.environ["AWS_REGION"])

    response = s3.list_objects_v2(Bucket=bucket)
    s3_keys = [key for obj in response.get("Contents", []) if (key := obj.get("Key", "")).endswith(".pdf")]

    result = get_client().table("go_chunks").select("go_id").execute()
    ingested = {str(row["go_id"]) for row in result.data}

    pending = [key for key in s3_keys if key.removesuffix(".pdf") not in ingested]

    print(f"{len(pending)} of {len(s3_keys)} PDFs need ingestion.")
    for key in pending:
        process_document(key)