# import weaviate
# import weaviate.classes as wvc
# import os
# from dotenv import load_dotenv

# load_dotenv()

# client = weaviate.connect_to_local(
#     headers={
#         "X-OpenAI-Api-Key": os.environ["OPENAI_API_KEY"]  # Replace with your inference API key
#     }
# )

# chunks = client.collections.get("Question")
# print(len(chunks))

# # response = chunks.query.near_text(query="doctoor??", limit=3, return_metadata=wvc.query.MetadataQuery(distance=True))
# # for chunk in response.objects:
# #     print(chunk.metadata.distance)
# #     print(chunk.properties)
# #     print(chunk.vector)
# #     print(chunk.uuid)
#     # print(chunk.vector)

# print(chunks.generate.hybrid(query="Is there a doctoor", alpha=0.5, limit=3, return_metadata=wvc.query.MetadataQuery(distance=True), include_vector=True, grouped_task="use the context to answer the question"))

# client.close()

import csv
from typing import List, Dict

# Define your schema structure
pihr_schema = [
    {"name": "document", "data_type": "TEXT"},
    {"name": "document_type", "data_type": "TEXT"},
    {"name": "tag", "data_type": "TEXT_ARRAY"},
]

# Define a function to process CSV rows into the required format
def import_data_from_csv(csv_file_path: str) -> List[Dict[str, str]]:
    data_rows = []
    with open(csv_file_path, mode="r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Parse and process the 'tag' column as a list
            row["tag"] = row["tag"].split(",") if "tag" in row and row["tag"] else []
            data_rows.append(row)
    return data_rows

# Usage example
csv_file_path = "src/rag/rag_factory/weviate/data.csv"  # Replace with your actual CSV file path
data_rows = import_data_from_csv(csv_file_path)

# Output the imported data
for row in data_rows:
    print(row)
