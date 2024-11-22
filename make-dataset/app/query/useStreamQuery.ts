import { NEXT_PUBLIC_AI_BACKEND } from "@/lib/consts"
import { useState } from "react"

function useStreamResponse({
  streamCallback,
}: {
  streamCallback: React.Dispatch<React.SetStateAction<string[]>>
}) {
  // const [responses, setResponses] = useState("")
  const [data, setData] = useState<any>()
  const [isLoading, setIsLoading] = useState(false)
  async function runQuery(queryContent: string) {    
    const response = await fetch(NEXT_PUBLIC_AI_BACKEND + "/query/stream", {
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
        // the text will start with <<GGWWP>> and if multiple <<GGWWP>> is there, it will be split by <<GGWWP>>
        // also remove the <<GGWWP>> prefix        

        const responses = text.split("<<GGWWP>>").filter((response) => response !== "")
        responses.forEach((response) => {
          streamCallback((prevValue) => [...prevValue, response])
        })

        // setResponses((prev) => prev + text)
        // streamCallback((prevValue) => [...prevValue, text])
      }
      read()
    }
    read()
  }

  return { data, runQuery, isLoading }
}

export default useStreamResponse