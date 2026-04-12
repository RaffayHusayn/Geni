export function buildPrompt(question: any, chunks: any[]) {
    const sources = chunks.map((c, i) => `[Sources ${i + 1}] GO ${c.go_id}\n ${c.content}`).join(`\n\n`);
    const system = `You are an assistant that asnwers questions about General Orders. Answer ONLY from the provided source excerpt. If the answer is not present in the provided sources, say " I Don't have enough information to answer this question". Always cite [Source N] when referring to information from the sources.`
    const user = `Sources:\n${sources}\n\nQuestion: ${question}`;

    return { system, user };

}