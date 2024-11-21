import * as dotenv from 'dotenv';
dotenv.config();


export const AI_BACKEND = process.env.AI_BACKEND || "http://" + window?.location?.hostname + ":8000" || "http://localhost:8000";

console.log('AI_BACKEND:', process.env.AI_BACKEND);