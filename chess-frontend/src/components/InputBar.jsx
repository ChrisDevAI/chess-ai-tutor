import { useState } from "react";

export default function InputBar({ onSendChat, onAnalyze }) {
  const [text, setText] = useState("");

  return (
    <div className="flex flex-col mt-4">

      <input
        type="text"
        placeholder="Ask anything or paste PGN..."
        value={text}
        onChange={(e) => setText(e.target.value)}
        className="px-3 py-2 bg-[#2c2c2c] rounded-md text-white placeholder-gray-400"
      />

      <div className="mt-3">

        <button
          className="px-4 py-2 bg-[#d7a165] text-black rounded-md ml-[100px]"
          onClick={() => {
            if (text.trim() !== "") {
              onSendChat(text);     // send text to backend
              setText("");          // clear the field
            }
          }}
        >
          Send
        </button>

        <button
          className="px-4 py-2 bg-[#d7a165] text-black rounded-md ml-[160px]"
          onClick={onAnalyze}
        >
          Analyze Position
        </button>

      </div>
    </div>
  );
}
