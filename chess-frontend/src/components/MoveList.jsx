import { useEffect, useRef } from "react";

export default function MoveList({ moves, currentIndex, bestMove }) {
  const containerRef = useRef(null);
  const activeRef = useRef(null);

  // Convert flat SAN array into paired rows (white/black)
  const pairedMoves = [];
  for (let i = 0; i < moves.length; i += 2) {
    pairedMoves.push({
      white: moves[i] || "",
      black: moves[i + 1] || "",
    });
  }

  // currentIndex = number of moves applied (0..moves.length)
  // active SAN index is currentIndex - 1 (or none if 0)
  const activeMoveIndex = currentIndex - 1;

  // Auto-scroll whenever the active move changes
  useEffect(() => {
    if (activeRef.current && containerRef.current) {
      const container = containerRef.current;
      const active = activeRef.current;

      const top = active.offsetTop - container.clientHeight / 2;
      container.scrollTo({
        top,
        behavior: "smooth",
      });
    }
  }, [currentIndex]);

  return (
    <div
      ref={containerRef}
      className="bg-[#2c2c2c] p-4 shadow-lg h-[600px] overflow-y-auto"
    >
      <div className="text-[#CD9A63] font-semibold">
        Best Move: {bestMove || "--"}
      </div>

      <div className="mt-4">
        <h3 className="text-[#CD9A63] font-semibold mb-2">Move List:</h3>

        <table className="w-full text-left">
          <thead>
            <tr className="text-gray-400 text-sm">
              <th className="w-10">#</th>
              <th className="w-24">White</th>
              <th className="w-24">Black</th>
            </tr>
          </thead>

          <tbody>
            {pairedMoves.map((pair, idx) => {
              const whiteIndex = idx * 2;
              const blackIndex = idx * 2 + 1;

              const whiteActive = whiteIndex === activeMoveIndex;
              const blackActive = blackIndex === activeMoveIndex;

              return (
                <tr key={idx} className="border-b border-gray-700">
                  <td className="py-1 text-gray-400">{idx + 1}.</td>

                  <td
                    ref={whiteActive ? activeRef : null}
                    className={
                      "py-1 px-2 rounded " +
                      (whiteActive
                        ? "bg-[#825B34] text-white"
                        : "text-gray-300")
                    }
                  >
                    {pair.white}
                  </td>

                  <td
                    ref={blackActive ? activeRef : null}
                    className={
                      "py-1 px-2 rounded " +
                      (blackActive
                        ? "bg-[#825B34] text-white"
                        : "text-gray-300")
                    }
                  >
                    {pair.black}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
