import fs from "fs";
import path from "path";
import { NextResponse } from "next/server";

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const fileName = searchParams.get("fileName") || "table-metadata";
  const filePath = path.join(process.cwd(), "exported-datasets", fileName + ".jsonl");

  let data = [];

  try {
    const fileContent = fs.readFileSync(filePath, "utf-8");
    data = fileContent
      .split("\n")
      .filter((line) => line)
      .map((line) => JSON.parse(line));
  } catch (error) {
    return NextResponse.json(
      { error: "Failed to read JSONL file", details: error },
      { status: 500 }
    );
  }

  return NextResponse.json({ data });
}
