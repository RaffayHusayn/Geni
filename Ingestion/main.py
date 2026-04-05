import sys
import json
from extract import extract
from parser import llmParser 

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
        parsed_data = llmParser(extraction_result)
        print("Parsing complete.")
    except Exception as e:
        print(f"Parsing failed: {e}")
        return
    # --- Step 3: Output ---
    print("\nFinal Structured Output")
    print(json.dumps(parsed_data, indent=2))
    
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python main.py <filename.pdf>")
        sys.exit(1)
    pdf = sys.argv[1] 
    process_document(pdf)