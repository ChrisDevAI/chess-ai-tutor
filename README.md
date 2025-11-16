# 📘 Chess AI Tutor — MVP
A multi-component AI system combining **Stockfish + AI** with a custom Flutter front-end interface.

This project demonstrates a working prototype of a hybrid chess analysis tool where a deterministic chess engine evaluates positions and a language model provides natural language explanations. The result is an interactive position explainer with a clean UI, move navigation, and contextual tutoring.

This is an **MVP**, intentionally scoped to show **system architecture, AI integration, and full-stack engineering**, not to compete with full commercial chess engines.

---

## 🌐 Live Demo (Frontend Only)

**UI Preview (Vercel link):**  
> _This deployment includes only the frontend to demonstrate the interface._  
> _The backend (FastAPI + Stockfish + AI) runs locally and is not deployed._

---

## 🧠 System Architecture

### High-Level Flow
```
Frontend (Flutter) →
    FastAPI Backend →
        Stockfish Engine →
        AI Language Model →
    Frontend UI
```

### Components
- **Frontend (Flutter):** Chessboard, move list, explanation panel, navigation buttons  
- **Backend (FastAPI):** Stockfish orchestration + AI prompts  
- **Stockfish Engine:** Local deterministic chess analysis  
- **OpenAI Model:** Converts engine output into human-readable guidance  

This structure cleanly separates calculation, explanation, and presentation.

---

## 🎯 Features (MVP)

- ✔ **Position Snapshot Analysis**  
- ✔ **AI-Generated Explanations**  
- ✔ **Interactive Chessboard**  
- ✔ **Move Navigation (Start / Prev / Next / End)**  
- ✔ **Scrollable Move List**  
- ✔ **Chat-Style Explanation Panel**  
- ✔ **Structured, Two-Column UI Layout**

---

## ⚠ MVP Status & Limitations

This prototype focuses on architecture and integration. Current constraints include:

- Backend is **local-only**  
- AI explanations vary with prompt behavior  
- No PGN import/export UI yet  
- Limited move validation  
- No evaluation bar or centipawn graph  
- Stockfish runs with lightweight settings for portability

---

## 📂 Project Structure

```
chess-ai-app/
│
├── chess-frontend/       # Flutter UI
├── chess-backend/        # FastAPI backend (Stockfish + AI)
├── screenshots/          # UI images
│
├── README.md
└── .gitignore
```

---

# 🚀 Running the Full System Locally

This project contains two components:

1. **Backend:** FastAPI + Stockfish + OpenAI  
2. **Frontend:** Flutter UI  

Both must run locally for the full MVP.

---

### 1. Clone the Repository

```bash
git clone https://github.com/ChrisDevAI/chess-ai-app.git
cd chess-ai-app
```

---

### 2. Backend Setup (FastAPI + Stockfish)

```bash
cd chess-backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file in the backend folder:

```env
OPENAI_API_KEY=your_key_here
```

Run the backend with Uvicorn:

```bash
uvicorn main:app --reload --port 8000
```

Backend will run at:

```
http://localhost:8000
```

Swagger API docs:

```
http://localhost:8000/docs
```

---

### 3. Frontend Setup (Flutter)

```bash
cd chess-frontend
flutter pub get
```

Run the UI:

**Web (Chrome):**
```bash
flutter run -d chrome
```

**Windows Desktop:**
```bash
flutter run -d windows
```

**Android (optional):**
```bash
flutter run -d android
```

Flutter will open the UI automatically on the selected device.

---

# Current Version (Polished UI)
> **Insert screenshot here:**  
> `![Current UI](screenshots/current-1.jpg)`

The polished interface includes:

- A dark theme  
- Clear panel separation  
- Two-column move list  
- Gold-accented navigation buttons  
- Clean spacing and improved readability  
- Modern chess application layout  

---

# 🖼 UI Evolution (Before → After)

## Early Version (Prototype)
> **Insert screenshot here:**  
> `![Early UI](screenshots/early-1.jpg)`

The initial prototype showed:

- Flat, washed-out color palette  
- Weak visual hierarchy  
- Broken move list  
- Inconsistent spacing  
- No UI structure  

Functional, but visually rough.

---

# 🛠 Development Journey (Iteration Process)

A key strength of this project is the visible evolution from prototype to polished MVP.

---

## 1. Early Prototype (Functional but unpolished)
> **Insert screenshot here:**  
> `![Prototype Move List](screenshots/prototype-move-1.jpg)`

Issues included:

- Multiple moves per row  
- Incorrect numbering  
- No alignment  
- Minimal styling  

---

## 2. Mid-Development Issues (Debugging Phase)
> **Insert screenshot here:**  
> `![Broken Move List](screenshots/mid-broken-1.jpg)`  
> **Insert second debugging screenshot:**  
> `![Another Broken State](screenshots/mid-broken-2.jpg)`

These snapshots show:

- Overlapping text  
- Incorrect grouping  
- Misaligned rows  
- Highlight issues  
- Layout bugs  

Fixes included:

- Rewriting the move list renderer  
- Turn-based grouping  
- Grid/Flex layout corrections  
- Cleaner spacing and padding  

---

# 🔧 Technical Stack

**Frontend:** Flutter (Dart)  
**Backend:** FastAPI (Python)  
**Engine:** Stockfish (local binary)  
**AI:** OpenAI API (GPT models)  
**Deployment:** Vercel (frontend preview), local backend  
**Tools:** Git, VS Code, Python, Flutter SDK  

---

# 🛠 Future Improvements

- Interpreter-style explanation system  
- PGN import/export  
- Evaluation bar  
- Per-move explanation buttons  
- Engine depth controls  
- Dockerized backend  
- Stronger chess reasoning prompts  
- Optional cloud deployment (Railway / Fly.io)

---

# 📄 License

MIT License.

---

# 👤 Author

**Christopher Mena**  
AI/ML Engineer  

**GitHub:** [@ChrisDevAI](https://github.com/ChrisDevAI)  
**LinkedIn:** [LinkedIn Profile](https://linkedin.com/in/ChrisDevAI)  
**Website:** [ChrisAI.dev](https://ChrisAI.dev)

---

## Notes
This is an early MVP focused on architecture, integration, and rapid prototyping. Further enhancements will solidify the analysis workflow and interpreter logic.

