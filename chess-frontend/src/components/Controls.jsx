import {
  FaStepBackward,
  FaCaretLeft,
  FaCaretRight,
  FaStepForward
} from "react-icons/fa";

export default function Controls({ moves, currentIndex, jumpToMove }) {
  
  function goStart() {
    jumpToMove(0);
  }

  function goPrev() {
    if (currentIndex > 0) {
      jumpToMove(currentIndex - 1);
    }
  }

  function goNext() {
    if (currentIndex < moves.length) {
      jumpToMove(currentIndex + 1);
    }
  }

  function goEnd() {
    jumpToMove(moves.length);
  }

  return (
    <div className="flex">
      <button
        onClick={goStart}
        className="px-4 py-2 bg-[#825B34] rounded-md ml-[30px] flex items-center gap-2"
      >
        <FaStepBackward size={14} />
        Start
      </button>

      <button
        onClick={goPrev}
        className="px-4 py-2 bg-[#825B34] rounded-md ml-[50px] flex items-center gap-2"
      >
        <FaCaretLeft size={14} />
        Prev
      </button>

      <button
        onClick={goNext}
        className="px-4 py-2 bg-[#825B34] rounded-md ml-[50px] flex items-center gap-2"
      >
        Next
        <FaCaretRight size={14} />
      </button>

      <button
        onClick={goEnd}
        className="px-4 py-2 bg-[#825B34] rounded-md ml-[50px] flex items-center gap-2"
      >
        End
        <FaStepForward size={14} />
      </button>
    </div>
  );
}
