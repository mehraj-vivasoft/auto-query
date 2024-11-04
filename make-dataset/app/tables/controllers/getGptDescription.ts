export const getGptDescription = async (
  tableData: string,
  prefixMessage: string
): Promise<string> => {
  const response = await fetch("/api/gptDescription", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      tableData,
      prefixMessage,
    }),
  });

  if (!response.ok) {
    throw new Error("Network response was not ok");
  }

  const data = await response.json();

  const description = data.description;

  return description;
};
