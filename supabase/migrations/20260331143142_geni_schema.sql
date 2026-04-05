create extension if not exists vector;

create table if not exists go_chunks (
    id          bigserial primary key,
    go_id       text        not null,
    chunk_index int         not null,
    content     text        not null,
    metadata    jsonb       default '{}',
    embedding   vector(1536),
    created_at  timestamptz default now()
);

create index if not exists go_chunks_embedding_idx
    on go_chunks using hnsw (embedding vector_cosine_ops)
    with (m = 16, ef_construction = 64);

create index if not exists go_chunk_metadata_idx
    on go_chunks using gin (metadata);

create or replace function match_chunks(
    query_embedding vector(1536),
    match_count     int   default 5,
    filter          jsonb default '{}'
)
returns table (
    id         bigint,
    go_id      text,
    content    text,
    metadata   jsonb,
    similarity float
)
language plpgsql as $$
begin
    return query
    select
        goc.id,
        goc.go_id,
        goc.content,
        goc.metadata,
        1 - (goc.embedding <=> query_embedding) as similarity
    from go_chunks goc
    where (filter is null or goc.metadata @> filter)
    order by goc.embedding <=> query_embedding
    limit match_count;
end;
$$;