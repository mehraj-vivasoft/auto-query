import { NextResponse } from "next/server";
import clientPromise from "../../../lib/mongodb";
import { ObjectId } from "mongodb";

export async function POST(req: Request) {
  const { tableName, trainingData } = await req.json();

  if (!tableName || !trainingData) {
    return NextResponse.json(
      { message: "tableName and trainingData are required" },
      { status: 400 }
    );
  }

  try {
    const client = await clientPromise;
    const db = client.db("pihr-dataset");
    const collection = db.collection("table-metadata");
    const result = await collection.insertOne({ tableName, trainingData });

    return NextResponse.json(
      { message: "Document saved", result },
      { status: 200 }
    );
  } catch (error) {
    console.error("Error saving document:", error);
    return NextResponse.json(
      {
        message: "Failed to save document",
        error,
      },
      { status: 500 }
    );
  }
}

export async function GET(req: Request) {
  const { searchParams } = new URL(req.url);
  const tableName = searchParams.get("tableName");

  if (!tableName) {
    return NextResponse.json(
      { message: "tableName is required" },
      { status: 400 }
    );
  }

  try {
    const client = await clientPromise;
    const db = client.db("pihr-dataset");
    const collection = db.collection("table-metadata");

    // Find all documents where the `tableName` matches
    const documents = await collection.find({ tableName }).toArray();

    if (documents.length === 0) {
      return NextResponse.json(
        { message: "No documents found for the given tableName" },
        { status: 404 }
      );
    }

    const parsedDocs = documents.map((doc) => {
      return { trainingData: doc.trainingData, id: doc._id };
    });

    return NextResponse.json(
      { addedTrainingData: parsedDocs },
      { status: 200 }
    );
  } catch (error) {
    console.error("Error fetching documents:", error);
    return NextResponse.json(
      { message: "Failed to fetch documents", error },
      { status: 500 }
    );
  }
}

export async function PUT(req: Request) {
  const { id, trainingData } = await req.json();

  if (!id || !trainingData) {
    return NextResponse.json(
      { message: "id and trainingData are required" },
      { status: 400 }
    );
  }

  try {
    const client = await clientPromise;
    const db = client.db("pihr-dataset");
    const collection = db.collection("table-metadata");

    // Convert the id to a MongoDB ObjectId
    const objectId = new ObjectId(id);

    // Update the document where the `_id` matches the provided id
    const result = await collection.updateOne(
      { _id: objectId },
      { $set: { trainingData } }
    );

    if (result.matchedCount === 0) {
      return NextResponse.json(
        { message: "No document found with the given id" },
        { status: 404 }
      );
    }

    return NextResponse.json(
      { message: "Document updated successfully", result },
      { status: 200 }
    );
  } catch (error) {
    console.error("Error updating document:", error);
    return NextResponse.json(
      { message: "Failed to update document", error },
      { status: 500 }
    );
  }
}

export async function DELETE(req: Request) {
  const { id } = await req.json();

  if (!id) {
    return NextResponse.json({ message: "id is required" }, { status: 400 });
  }

  try {
    const client = await clientPromise;
    const db = client.db("pihr-dataset");
    const collection = db.collection("table-metadata");

    // Convert the id to a MongoDB ObjectId
    const objectId = new ObjectId(id);

    // Delete the document where the `_id` matches the provided id
    const result = await collection.deleteOne({ _id: objectId });

    if (result.deletedCount === 0) {
      return NextResponse.json(
        { message: "No document found with the given id" },
        { status: 404 }
      );
    }

    return NextResponse.json(
      { message: "Document deleted successfully" },
      { status: 200 }
    );
  } catch (error) {
    console.error("Error deleting document:", error);
    return NextResponse.json(
      { message: "Failed to delete document", error },
      { status: 500 }
    );
  }
}
