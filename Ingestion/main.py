import sys
import json
from extract import extract
from parser import llmParser 
from chunk import chunk

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

    # --- Step 3: Output ---
    print("\nFinal Structured Output")
    print(json.dumps(chunks, indent=2))
    
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python main.py <filename.pdf>")
        sys.exit(1)
    pdf = sys.argv[1] 
    process_document(pdf)