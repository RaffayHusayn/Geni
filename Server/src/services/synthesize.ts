import { Messages } from "openai/resources/chat/completions.mjs";
import { client } from "../lib/openai";
import { buildPrompt } from "./prompt";

export async function synthesize(question: any, chunks:any){
    const {system, user}= buildPrompt(question, chunks)
    const response = await client.chat.completions.create({
        model: 'gpt-5-mini',
        messages: [
            {role:'system', content: system },
            {role: 'user', content: user}
        ],
    })
    return response.choices[0].message.content
}