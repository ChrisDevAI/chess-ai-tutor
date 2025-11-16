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

# -------------------------------
# Coach Explanation (Stockfish + GPT)
# -------------------------------

@app.post("/coach")
def coach_player(req: CoachRequest):
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

    best_move = ""

    while True:
        output = engine.stdout.readline()
        if output.startswith("bestmove"):
            parts = output.split()
            best_move = parts[1] if len(parts) > 1 else ""
            break



    engine.stdin.write("quit\n")
    engine.stdin.flush()
    engine.terminate()

    explanation_prompt = (
        f"Given this position (FEN): {req.fen}\n"
        f"The best move for {req.player_color} is: {best_move}\n"
        "Explain why this is a good move and what plan it supports."
    )

    explanation = query_openai(explanation_prompt)

    return {
        "best_move": best_move,
        "explanation": explanation
    }
