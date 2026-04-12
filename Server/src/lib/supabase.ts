import dotenv from 'dotenv';
import path from 'path';
dotenv.config({ path: path.resolve(import.meta.dirname, '../../../.env') });
import { createClient } from '@supabase/supabase-js';

export const supabase = createClient(
  process.env.SUPABASE_URL!,
  process.env.SUPABASE_SERVICE_KEY!
);