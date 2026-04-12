import {supabase} from "../lib/supabase.js"
export interface Chunk {
  id: number;
  go_id: string;
  content: string;
  metadata: Record<string, string>;
  similarity: number;
}

export interface RetrieveOptions {
  matchCount?: number;
  filter?: {
    line?: string;
    track?: string;
    subdivision?: string;
  };
}

export async function retrieveChunks(
  embedding: number[],
  options: RetrieveOptions = {}
): Promise<Chunk[]> {
  const { matchCount = 5, filter = {} } = options;

  const { data, error } = await supabase.rpc('match_chunks', {
    query_embedding: embedding,
    match_count: matchCount,
    filter,
  });

  if (error) throw new Error(`Retrieval failed: ${error.message}`);
  return data as Chunk[];
}