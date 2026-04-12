import helmet from "helmet"
import "dotenv/config" 
import express, { Request, Response } from "express"
import cors from "cors"
import queryRouter from "./routes/query"

const app = express();
const PORT = process.env.PORT ?? 3000;

// ----  Middlewares ----
app.use(helmet());
app.use(cors());
app.use(express.json());


app.get('/health', (req: Request, res: Response) => {
  res.json({ status: 'ok' });
});
app.use("/", queryRouter)

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});