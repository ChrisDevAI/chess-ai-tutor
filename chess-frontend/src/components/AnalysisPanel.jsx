export default function AnalysisPanel({ text, chat }) {
  return (
    <div className="bg-[#2c2c2c] p-4 shadow-lg h-[500px] overflow-y-auto">
      
      {/* Title */}
      <h2 className="font-semibold mb-2">Type something below to begin</h2>

      {/* GPT Chat reply (Send button) */}
      {chat && (
        <div className="mt-4">
          <h3 className="text-[#CD9A63] font-semibold mb-1">Chat Response:</h3>
          <p className="text-gray-300 whitespace-pre-wrap">{chat}</p>
        </div>
      )}

      {/* GPT Analysis reply (Analyze button) */}
      {text && (
        <div className="mt-6">
          <h3 className="text-[#CD9A63] font-semibold mb-1">Analysis:</h3>
          <p className="text-gray-300 whitespace-pre-wrap">{text}</p>
        </div>
      )}

    </div>
  );
}
