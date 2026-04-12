import { Router } from "express";
import { embedQuestion } from "../services/embed";
import { retrieveChunks } from "../services/retrieve";
import { synthesize } from "../services/synthesize";

const router = Router()
router.post("/", async(req, res)=>{
    const {question, filter= {}} = req.body

    if (!question.trim()){
        return res.status(400). json({error: "Question can't be empty"})
    }

    try{
        const embedding = await embedQuestion(question)
        const chunks = await retrieveChunks(embedding, filter)

        if(!chunks.length){
            return res.json({answer: "No relevant records found", sources: []})
        }

        const answer = await synthesize(question, chunks)
        res.json({
            answer,
            sources: chunks.map(c=>({
                go_id: c.go_id,
                content: c.content,
                metadata: c.metadata,
                similarity: c.similarity
            }))
        })
    } catch(err){
        console.error(err)
        res.status(500).json({error: err.message})
    }
})
export default router