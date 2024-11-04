import { MongoClient } from 'mongodb';

if (!process.env.MONGODB_URI) {
  throw new Error('Please add your Mongo URI to .env.local');
}

const uri: string = process.env.MONGODB_URI;
const options = {};

const client = new MongoClient(uri, options);
const clientPromise = client.connect();

export default clientPromise;
