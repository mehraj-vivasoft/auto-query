import { useState } from "react"

function useStreamResponse({
  streamCallback,
}: {
  streamCallback: React.Dispatch<React.SetStateAction<string[]>>
}) {
  const [responses, setResponses] = useState("")
  const [data, setData] = useState<any>()
  const [isLoading, setIsLoading] = useState(false)
  async function runQuery(queryContent: string) {
    const response = await fetch("http://localhost:8000/query/stream", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ query: queryContent }),
    })

    if (!response.body) {
      throw new Error("ReadableStream not supported in this browser.")
    }

    const reader = response.body.getReader()
    setIsLoading(true)
    streamCallback([])    
    readStream(reader)
    return reader
  }  

  async function readStream(reader: ReadableStreamDefaultReader) {
    async function read() {
      const { done, value } = await reader.read()
      if (done) {
        setIsLoading(false)
        return
      }

      const text = new TextDecoder().decode(value)
      if (text.includes("COMPLETED _ END OF STREAM _ FINAL RESULT")) {
        setData(text.replace(/.*COMPLETED _ END OF STREAM _ FINAL RESULT/, ""))
      } else {
        setResponses((prev) => prev + text)
        streamCallback((prevValue) => [...prevValue, text])
      }
      read()
    }
    read()
  }

  return { responses, data, runQuery, isLoading }
}

export default useStreamResponse