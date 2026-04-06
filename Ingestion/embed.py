from openai import embeddings, OpenAI 
from dotenv import load_dotenv

load_dotenv()
client = OpenAI() 
def embed(chunks: list[dict])->list[dict]:
    contents = [c["content"] for c in chunks]
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=contents
    )

    for i, chunk in enumerate(chunks):
        chunk["embedding"] = response.data[i].embedding
    return chunks




