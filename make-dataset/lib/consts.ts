import * as dotenv from 'dotenv';
dotenv.config();

export const NEXT_PUBLIC_AI_BACKEND = process.env.NEXT_PUBLIC_AI_BACKEND || "http://localhost:8000";

console.log('NEXT_PUBLIC_AI_BACKEND:', process.env.NEXT_PUBLIC_AI_BACKEND);