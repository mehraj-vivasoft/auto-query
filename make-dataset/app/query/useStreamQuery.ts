import { NEXT_PUBLIC_AI_BACKEND } from "@/lib/consts";
import { useState } from "react";

function useStreamResponse({
  streamCallback,
}: {
  streamCallback: React.Dispatch<React.SetStateAction<string[]>>;
}) {
  // const [responses, setResponses] = useState("")
  const [data, setData] = useState<any>();
  const [isLoading, setIsLoading] = useState(false);
  const [buffer, setBuffer] = useState("");
  async function runQuery(queryContent: string) {
    const response = await fetch(NEXT_PUBLIC_AI_BACKEND + "/query/stream", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ query: queryContent }),
    });

    if (!response.body) {
      throw new Error("ReadableStream not supported in this browser.");
    }

    const reader = response.body.getReader();
    setIsLoading(true);
    streamCallback([]);
    readStream(reader);
    return reader;
  }

  async function readStream(reader: ReadableStreamDefaultReader) {
    async function read() {
      const { done, value } = await reader.read();
      if (done) {
        setIsLoading(false);
        return;
      }

      const text = new TextDecoder("utf-8").decode(value, { stream: true });
      if (text.includes("COMPLETED _ END OF STREAM _ FINAL RESULT")) {
        setData(text.replace(/.*COMPLETED _ END OF STREAM _ FINAL RESULT/, ""));
      } else {
        // the text will start with <<GGWWP>> and if multiple <<GGWWP>> is there, it will be split by <<GGWWP>>
        // also remove the <<GGWWP>> prefix        

        const responses = text
          .split("<<GGWWP>>")
          .filter((response) => response !== "");
        responses.forEach((response) => {
          // if response starts with $ then remove $ and append it to buffer and then set buffer to ""
          if (response.startsWith("$")) {            
            streamCallback((prevValue) => [...prevValue, buffer + response.slice(1)]);
            setBuffer("");  
          } else {
            setBuffer(buffer + response);
          }          
        });

        // setResponses((prev) => prev + text)
        // streamCallback((prevValue) => [...prevValue, text])
      }
      read();
    }
    read();
  }

  return { data, runQuery, isLoading, setIsLoading };
}

export default useStreamResponse;
