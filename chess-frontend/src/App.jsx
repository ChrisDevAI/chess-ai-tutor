import { useState } from "react";

import Header from "./components/Header";
import AnalysisPanel from "./components/AnalysisPanel";
import BoardPanel from "./components/BoardPanel";
import MoveList from "./components/MoveList";
import InputBar from "./components/InputBar";
import Controls from "./components/Controls";

import { Chess } from "chess.js/dist/esm/chess.js";

export default function App() {

  // -------------------------------
  // GLOBAL SHARED STATE
  // -------------------------------
  const [game, setGame] = useState(new Chess());
  const [moves, setMoves] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [bestMove, setBestMove] = useState("");

  const [analysisText, setAnalysisText] = useState("");
  const [chatReply, setChatReply] = useState("");


  // -------------------------------
  // MOVE RECONSTRUCTION (Jump To Move)
  // -------------------------------
  function jumpToMove(index) {
    const newGame = new Chess();

    for (let i = 0; i < index; i++) {
      newGame.move(moves[i]);
    }

    setGame(newGame);
    setCurrentIndex(index);
  }


  // -------------------------------
  // BEST MOVE FROM STOCKFISH
  // -------------------------------
  async function fetchBestMove(fen) {
    try {
      const res = await fetch("http://127.0.0.1:8000/best-move", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ fen })
      });

      const data = await res.json();
      console.log("Best move:", data.best_move);

      setBestMove(data.best_move);

    } catch (err) {
      console.error("Best move error:", err);
    }
  }


  // -------------------------------
  // COACH ENDPOINT (LLM + Stockfish)
  // -------------------------------
  async function runCoach(text) {
    const colorToMove = game.turn() === "w" ? "white" : "black";

    try {
      const res = await fetch("http://127.0.0.1:8000/coach", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          question: text,
          fen: game.fen(),
          player_color: colorToMove
        })
      });

      const data = await res.json();

      setChatReply(data.best_move);
      setAnalysisText(data.explanation);

    } catch (err) {
      console.error("Coach error:", err);
    }
  }



  // -------------------------------
  // ANALYZE POSITION ENDPOINT
  // -------------------------------
  async function runAnalysis() {
    try {
      const res = await fetch("http://127.0.0.1:8000/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          fen: game.fen()
        })
      });

      const data = await res.json();
      console.log("Analysis:", data.analysis);
      setAnalysisText(data.analysis);

    } catch (err) {
      console.error("Analysis error:", err);
    }
  }


  // -------------------------------
  // RENDER
  // -------------------------------
  return (
    <div className="min-h-screen w-full bg-black text-white flex flex-col items-center pb-2">

      <Header />

      <div className="mt-6 relative w-full h-full">

        {/* LEFT SIDE: Analysis + Input */}
        <div className="absolute top-[0px] left-[0px] w-[36%] ml-8">
          <AnalysisPanel text={analysisText} chat={chatReply} />

          <InputBar 
            onSendChat={runCoach}      
            onAnalyze={runAnalysis}
          />
        </div>

        {/* CENTER: Board + Controls */}
        <div className="absolute top-[-15px] left-[550px] w-[800px]">

          {/* Board */}
          <BoardPanel 
            game={game}
            setGame={setGame}
            moves={moves}
            setMoves={setMoves}
            currentIndex={currentIndex}
            setCurrentIndex={setCurrentIndex}
            jumpToMove={jumpToMove}
            fetchBestMove={fetchBestMove}
          />

          {/* Controls — EXACT restored positioning */}
          <div className="absolute top-[575px] left-[85px]">
            <Controls
              moves={moves}
              currentIndex={currentIndex}
              jumpToMove={jumpToMove}
            />
          </div>

        </div>

        {/* RIGHT SIDE: Move List */}
        <div className="absolute top-[0px] left-[1220px] w-[19%] mr-8">
          <MoveList 
            moves={moves}
            currentIndex={currentIndex}
            bestMove={bestMove}
          />
        </div>

      </div>
    </div>
  );
}
