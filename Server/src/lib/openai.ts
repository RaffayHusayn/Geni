import dotenv from 'dotenv';
import path from 'path';
dotenv.config({ path: path.resolve(import.meta.dirname, '../../../.env') });
import OpenAI from 'openai';

export const client = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY
});
