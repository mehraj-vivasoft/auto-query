import { NextResponse } from 'next/server';
import clientPromise from '../../../lib/mongodb';

// Handle GET requests
export async function GET() {
  try {
    const client = await clientPromise;
    const db = client.db('pihr-dataset');
    const documents = await db.collection('test').find({}).toArray();
    return NextResponse.json(documents);
  } catch (error) {
    console.error('Error fetching documents:', error);
    return new NextResponse('Something went wrong', { status: 500 });
  }
}

// Handle POST requests
export async function POST(req: Request) {
  try {
    const client = await clientPromise;
    const db = client.db('pihr-dataset');
    const body = await req.json();
    const result = await db.collection('test').insertOne(body);
    return NextResponse.json({ message: 'Document added!', result }, { status: 201 });
  } catch (error) {
    console.error('Error adding document:', error);
    return new NextResponse('Something went wrong', { status: 500 });
  }
}
