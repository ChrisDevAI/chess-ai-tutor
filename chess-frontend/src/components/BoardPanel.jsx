import { Chessboard } from "react-chessboard";
import { useState, useEffect } from "react";
import { Chess } from "chess.js/dist/esm/chess.js";

export default function BoardPanel({
  game,
  setGame,
  moves,
  setMoves,
  currentIndex,
  setCurrentIndex,
  jumpToMove,
  fetchBestMove,
}) {
  const [position, setPosition] = useState(game.fen());

  // Keep local board synced whenever the global game changes
  useEffect(() => {
    setPosition(game.fen());
  }, [game]);

  const boardOptions = {
    position: position,
    boardWidth: 420,

    onPieceDrop: ({ sourceSquare, targetSquare }) => {
      if (!targetSquare) return false;

      // Clone current game and apply the move
      const newGame = new Chess();
      newGame.load(game.fen());

      const move = newGame.move({
        from: sourceSquare,
        to: targetSquare,
        promotion: "q",
      });

      if (!move) return false;

      const san = move.san;

      // If user was in the middle of the line, truncate future moves
      let baseMoves;
      if (currentIndex < moves.length) {
        baseMoves = moves.slice(0, currentIndex);
      } else {
        baseMoves = moves;
      }

      const updatedMoves = [...baseMoves, san];

      setGame(newGame);
      setMoves(updatedMoves);

      // currentIndex = number of moves applied
      setCurrentIndex(updatedMoves.length);

      // Update local position
      setPosition(newGame.fen());

      // Ask backend for best move in this new position
      fetchBestMove(newGame.fen());

      return true;
    },
  };

  return (
    <div className="relative bg-black">
      <div
        className="absolute top-[0px] left-[75px] p-3"
        style={{ width: 570 }}
      >
        <Chessboard options={boardOptions} />
      </div>
    </div>
  );
}
