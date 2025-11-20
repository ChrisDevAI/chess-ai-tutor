from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from dotenv import load_dotenv
import subprocess
import os
import io
import chess
import chess.pgn
from llm_handler import query_openai

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, use your actual frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------
# Models
# -------------------------------

class MoveRequest(BaseModel):
    fen: str

class ChatRequest(BaseModel):
    message: str 
    fen: Optional[str] = None

class AnalyzeRequest(BaseModel):
    fen: str

class CoachRequest(BaseModel):
    fen: str
    player_color: Optional[str] = "white"
    question: Optional[str] = ""

class PGNRequest(BaseModel):
    pgn: str


# -------------------------------
# Helpers
# -------------------------------

def uci_to_san(fen, uci_move):
    board = chess.Board(fen)
    move = chess.Move.from_uci(uci_move)
    san = board.san(move)
    return san




# -------------------------------
# PGN Loading Endpoint
# -------------------------------

@app.post("/load-pgn")
def load_pgn(req: PGNRequest):
    game = chess.pgn.read_game(io.StringIO(req.pgn))
    if game is None:
        raise HTTPException(status_code=400, detail="Invalid PGN format.")

    board = game.board()
    move_list = []

    for move in game.mainline_moves():
        san = board.san(move)
        move_list.append(san)
        board.push(move)

    return {
        "moves": move_list,
        "final_fen": board.fen(),
        "pgn": req.pgn
    }

# -------------------------------
# Stockfish Best Move Endpoint
# -------------------------------

@app.post("/best-move")
def get_best_move(request: MoveRequest):
    stockfish_path = "./engines/stockfish/stockfish-windows-x86-64-avx2.exe"
    engine = subprocess.Popen(
        [stockfish_path],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        universal_newlines=True,
    )

    # Standard UCI init
    engine.stdin.write("uci\n")
    engine.stdin.write(f"position fen {request.fen}\n")
    engine.stdin.write("go movetime 500\n")
    engine.stdin.flush()

    best_move_raw = ""

    # Read lines until bestmove appears
    while True:
        line = engine.stdout.readline()
        if not line:
            continue

        line = line.strip()
        print("DEBUG STOCKFISH RAW:", repr(line))

        if line.startswith("bestmove"):
            parts = line.split()
            # UCI spec: bestmove <move> [ponder <move>]
            if len(parts) >= 2:
                best_move_raw = parts[1]
            else:
                best_move_raw = ""
            break

    engine.stdin.write("quit\n")
    engine.stdin.flush()
    engine.terminate()

    # Final hard sanitizing
    cleaned = (
        best_move_raw
        .strip()
        .split()[0]        # in case something else sneaks in
        .encode("ascii", "ignore")
        .decode()
    )

    san = uci_to_san(request.fen, cleaned)

    return {"best_move": san}



    

# -------------------------------
# Chat with LLM
# -------------------------------

@app.post("/chat")
def chat_with_llm(req: ChatRequest):
    reply = query_openai(req.message, req.fen)
    return {"reply": reply}

# -------------------------------
# Analyze Position with GPT
# -------------------------------

@app.post("/analyze")
def analyze_position(req: AnalyzeRequest):
    analysis_prompt = (
        f"Given this chess position (FEN): {req.fen}\n"
        "Please explain the strengths, weaknesses, and possible plans for both sides."
        " Use clear, educational language suitable for a serious beginner or intermediate player."
    )
    reply = query_openai(analysis_prompt)
    return {"analysis": reply}


def describe_board_from_fen(fen: str) -> str:
    """
    Convert a FEN string into a human-readable list of pieces and squares.
    This anchors the LLM so it cannot hallucinate pieces or threats.
    """
    board = chess.Board(fen)
    piece_map = board.piece_map()

    piece_names = {
        "p": "pawn",
        "n": "knight",
        "b": "bishop",
        "r": "rook",
        "q": "queen",
        "k": "king",
    }

    white_pieces = []
    black_pieces = []

    for square, piece in piece_map.items():
        square_name = chess.square_name(square)
        symbol = piece.symbol()  # 'P' for white pawn, 'p' for black pawn
        base = symbol.lower()
        piece_name = piece_names.get(base, "piece")

        entry = f"{piece_name} on {square_name}"

        if symbol.isupper():
            white_pieces.append(entry)
        else:
            black_pieces.append(entry)

    white_text = "White pieces:\n" + ("\n".join(white_pieces) if white_pieces else "(none)")
    black_text = "Black pieces:\n" + ("\n".join(black_pieces) if black_pieces else "(none)")

    return white_text + "\n\n" + black_text



# -------------------------------
# Coach Explanation (Stockfish + GPT, hallucination-resistant)
# -------------------------------

@app.post("/coach")
def coach_player(req: CoachRequest):
    # 1. Run Stockfish to get best move in UCI
    stockfish_path = "./engines/stockfish/stockfish-windows-x86-64-avx2.exe"
    engine = subprocess.Popen(
        [stockfish_path],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        universal_newlines=True
    )

    engine.stdin.write("uci\n")
    engine.stdin.write(f"position fen {req.fen}\n")
    engine.stdin.write("go movetime 500\n")
    engine.stdin.flush()

    best_move_uci = ""

    while True:
        output = engine.stdout.readline()
        if not output:
            continue

        output = output.strip()
        if output.startswith("bestmove"):
            parts = output.split()
            best_move_uci = parts[1] if len(parts) > 1 else ""
            break

    engine.stdin.write("quit\n")
    engine.stdin.flush()
    engine.terminate()

    # Convert UCI best move to SAN for readability (if any)
    best_move_san = ""
    if best_move_uci:
        try:
            best_move_san = uci_to_san(req.fen, best_move_uci)
        except Exception as e:
            print("Error converting best move to SAN:", e)
            best_move_san = best_move_uci  # fallback to UCI string

    # 2. Build a human-readable board description
    board_description = describe_board_from_fen(req.fen)

    # 3. Build the coaching prompt with strict anti-hallucination rules
    coaching_prompt = f"""
You are a chess coach.

Here is the exact board position, described in plain English:

{board_description}

Side to move: {req.player_color}
Stockfish best move (UCI): {best_move_uci}
Stockfish best move (SAN, if available): {best_move_san}

The player asked this question about the position:
\"\"\"{req.question}\"\"\"


INSTRUCTIONS (CRITICAL):

- Base ALL of your reasoning ONLY on the pieces and squares listed in the board description above.
- DO NOT invent any extra pieces, pawns, squares, or threats that are not explicitly present there.
- If a move or threat is not supported by the described position, DO NOT mention it.
- If the player's question cannot be answered from this position, say so honestly.

COACHING STYLE:

1. Briefly explain the idea behind Stockfish's suggested move for {req.player_color}
   (using the SAN notation if available).

2. Directly answer the player's QUESTION in the context of THIS exact position.
   Be concrete: suggest candidate moves, plans, or defensive ideas that fit the board.

3. Keep the explanation clear and practical, suitable for a serious 1300–1700 player.
"""

    explanation = query_openai(coaching_prompt)

    return {
        "best_move": best_move_san or best_move_uci,
        "explanation": explanation
    }
