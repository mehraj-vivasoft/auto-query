import clientPromise from "@/lib/mongodb";
import fs from "fs";
import { NextResponse } from "next/server";
import path from "path";

export async function GET(req: Request) {
  try {
    const client = await clientPromise;
    const db = client.db("pihr-dataset");
    const { searchParams } = new URL(req.url);
    const collection_name =
      searchParams.get("collectionName") || "table-metadata";
    const collection = db.collection(collection_name);

    const cursor = collection.find();
    // const exportDir = path.join(process.cwd(), "exported-datasets");
    const exportDir = "exported-datasets";

    if (!fs.existsSync(exportDir)) {
      fs.mkdirSync(exportDir);
    }

    const filePath = path.join(exportDir, collection_name + ".jsonl");

    // Open a writable stream for JSONL format
    const writeStream = fs.createWriteStream(filePath, { flags: "w" });

    for await (const doc of cursor) {
      writeStream.write(`${JSON.stringify(doc["trainingData"])}\n`);
      // console.log(doc);
    }

    writeStream.end(); // Close the stream after writing all documents

    return NextResponse.json(
      { message: "Data written to JSONL file", filePath },
      { status: 200 }
    );
  } catch (error) {
    console.error(error);
    return NextResponse.json(
      { message: "Error occurred while exporting data", error },
      { status: 500 }
    );
  }
}
