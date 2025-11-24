# Chess AI Tutor

![Hero Screenshot](screenshots/Hero.jpg)

A hybrid AI chess analysis tool that combines AI, deterministic engine evaluation (Stockfish), and a clean React interface, to analyze Chess positions.

---

## 🔴 Live Demo (Frontend Only)
https://chess-ai-tutor-react.web.app

> Full functionality requires running the backend locally.

---

## Installation (Quick Start)

Python version: 3.10.x

Clone the repo:

```bash
git clone https://github.com/ChrisDevAI/chess-ai-tutor.git
cd chess-ai-tutor
```

---

### Backend Setup

```bash
cd chess-backend
py 3.10 -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Rename `.env.example` to `.env` and add:

```
OPENAI_API_KEY=your_key_here
```

Run backend:

```bash
uvicorn main:app --reload --port 8000
```

---

### Frontend Setup

```bash
cd ../chess-frontend
npm install
npm run dev
```

---

## Overview
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Development Journey](#development-journey)
- [License](#license)
- [Author](#author)

---

## Features

### Engine + AI Integration
- Snapshot-based position evaluation  
- Stockfish best-move computation  
- LLM-generated coaching and reasoning  
- Structured coaching endpoint  

### UI / Interaction
- Clean two-panel React layout  
- Scrollable move list  
- Move history navigation  
- Chat-style natural-language analysis  
- Tailwind dark theme  

### Architecture Advantages
- Fast Vite builds  
- Clean separation of engine vs AI logic  
- Deterministic local engine + expressive AI explanations  

[⬆️ Back to Overview](#overview)

---

## Tech Stack

### Frontend
- React  
- Vite  
- TailwindCSS  
- react-chessboard  

### Backend  
- Python  
- FastAPI  
- Stockfish  
- python-chess  
- Uvicorn  

### AI
- OpenAI GPT models  

[⬆️ Back to Overview](#overview)

---

## Development Journey

### Early Prototype (Flutter)
![Early UI](screenshots/early-1.jpg)

### Early Move-List Problems
![Prototype Move List](screenshots/prototype-move-1.jpg)

### Mid-Development Bugs
![Broken Move List](screenshots/mid-broken-1.jpg)
![Another Broken State](screenshots/mid-broken-2.jpg)


### Final UI in React (Post-Rewrite)
![React Final](screenshots/Hero.jpg)

[⬆️ Back to Overview](#overview)

---

## License
MIT License

---

## Author

**Christopher Mena**  
AI/ML Engineer  
GitHub: https://github.com/ChrisDevAI  
Website: https://ChrisAI.dev  
LinkedIn: https://linkedin.com/in/ChrisDevAI


