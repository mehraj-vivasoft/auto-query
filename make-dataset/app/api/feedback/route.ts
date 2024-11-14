import { NextResponse } from "next/server";
import clientPromise from "../../../lib/mongodb";
import { ObjectId } from "mongodb";

export async function POST(req: Request) {
  const { isSuccess, query, comment } = await req.json();

  if (!isSuccess || !query) {
    return NextResponse.json(
      { message: "query and isSuccess are required" },
      { status: 400 }
    );
  }

  try {
    const client = await clientPromise;
    const db = client.db("pihr-dataset");
    const collection = db.collection("feedback");
    const result = await collection.insertOne({ isSuccess, query, comment });

    return NextResponse.json(
      { message: "Feedback saved", result },
      { status: 200 }
    );
  } catch (error) {
    console.error("Error saving Feedback:", error);
    return NextResponse.json(
      {
        message: "Failed to save Feedback",
        error,
      },
      { status: 500 }
    );
  }
}

export async function GET(req: Request) {
  const { searchParams } = new URL(req.url);
  const isSuccess = searchParams.get("isSuccess") === "true";  

  //   if (!isSuccess) {
  //     return NextResponse.json(
  //       { message: "isSuccess query params is required" },
  //       { status: 400 }
  //     );
  //   }

  try {
    const client = await clientPromise;
    const db = client.db("pihr-dataset");
    const collection = db.collection("feedback");

    // Find all documents where the `tableName` matches
    const documents = isSuccess
      ? await collection.find({ isSuccess }).toArray()
      : await collection.find().toArray();

    if (documents.length === 0) {
      return NextResponse.json(
        { message: "No Feedback found for the given isSuccess" },
        { status: 404 }
      );
    }

    const parsedDocs = documents.map((doc) => {
      return {
        id: doc._id.toString(),
        isSuccess: doc.isSuccess,
        query: doc.query,
        comment: doc.comment,
      };
    });

    return NextResponse.json({ feedbacks: parsedDocs }, { status: 200 });
  } catch (error) {
    console.error("Error fetching feedbacks:", error);
    return NextResponse.json(
      { message: "Failed to fetch feedbacks", error },
      { status: 500 }
    );
  }
}

export async function PUT(req: Request) {
  const { id, query, isSuccess, comment } = await req.json();

  if (!id || !query || !isSuccess || !comment) {
    return NextResponse.json(
      { message: "id , query, isSuccess and comment are required" },
      { status: 400 }
    );
  }

  try {
    const client = await clientPromise;
    const db = client.db("pihr-dataset");
    const collection = db.collection("feedback");

    // Convert the id to a MongoDB ObjectId
    const objectId = new ObjectId(id);

    // Update the document where the `_id` matches the provided id
    const result = await collection.updateOne(
      { _id: objectId },
      { $set: { query, isSuccess, comment } }
    );

    if (result.matchedCount === 0) {
      return NextResponse.json(
        { message: "No feedback found with the given id" },
        { status: 404 }
      );
    }

    return NextResponse.json(
      { message: "Feedback updated successfully", result },
      { status: 200 }
    );
  } catch (error) {
    console.error("Error updating Feedback:", error);
    return NextResponse.json(
      { message: "Failed to update Feedback", error },
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
    const collection = db.collection("feedback");

    // Convert the id to a MongoDB ObjectId
    const objectId = new ObjectId(id);

    // Delete the document where the `_id` matches the provided id
    const result = await collection.deleteOne({ _id: objectId });

    if (result.deletedCount === 0) {
      return NextResponse.json(
        { message: "No Feedback found with the given id" },
        { status: 404 }
      );
    }

    return NextResponse.json(
      { message: "Feedback deleted successfully" },
      { status: 200 }
    );
  } catch (error) {
    console.error("Error deleting Feedback:", error);
    return NextResponse.json(
      { message: "Failed to delete Feedback", error },
      { status: 500 }
    );
  }
}
