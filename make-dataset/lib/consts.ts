import * as dotenv from 'dotenv';
dotenv.config();

export const AI_BACKEND = process.env.AI_BACKEND || "http://localhost:8000";