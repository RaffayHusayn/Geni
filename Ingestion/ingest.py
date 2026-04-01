from pathlib import Path
def ingest_file(pdf_path: str)->None:
    name=Path(pdf_path).name