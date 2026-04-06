# db.py
from supabase import create_client, Client
from dotenv import load_dotenv
import os

load_dotenv()

supabaseClient: Client | None = None

def get_client() -> Client:
    global supabaseClient
    if supabaseClient is None:
        supabaseClient = create_client(
            os.environ["SUPABASE_URL"],
            os.environ["SUPABASE_SERVICE_KEY"]
        )
    return supabaseClient 


def insert_chunks(chunks: list[dict]) -> None:
    """
    Insert a list of chunk dicts into go_chunks.
    Each chunk must have: go_id, chunk_index, content, metadata, embedding.
    """
    client = get_client()
    client.table("go_chunks").insert(chunks).execute()


def delete_go(chunks:list[dict]) -> None:
    """
    Delete all chunks for a GO before re-ingesting.
    Useful when re-running ingest on an already-stored document.
    """
    go_id = chunks[0]["go_id"]
    client = get_client()
    client.table("go_chunks").delete().eq("go_id", go_id).execute()


def go_exists (chunks:list[dict]) -> bool:
    """
    Check if a GO has already been ingested.
    """
    go_id = chunks[0]["go_id"]
    client = get_client()
    result = (
        client.table("go_chunks")
        .select("id")
        .eq("go_id", go_id)
        .limit(1)
        .execute()
    )
    return len(result.data) > 0

def go_upsert(chunks:list[dict])-> None:
    delete_go(chunks) # if go_id doesn't exist then it does nothing
    insert_chunks(chunks)
