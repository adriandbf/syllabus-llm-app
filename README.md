# Syllabus LLM App

A minimal local web application that lets students upload a course syllabus (PDF) and ask natural-language questions about it (e.g., exam dates, grading breakdown, policies). The app uses Retrieval-Augmented Generation (RAG) with the Gemini API to ensure answers are grounded strictly in the uploaded document.

---

## Features

* Upload a syllabus PDF
* Ask questions in plain English
* RAG pipeline (chunking + embeddings + vector search)
* Safety guardrails (system rules, injection checks, input limits)
* Telemetry logging (latency, tokens, RAG path)
* Offline evaluation with automated pass-rate reporting

---

## Architecture

```
User → Web UI → Flask API
                → PDF Parser → Chunking → Embeddings → Vector Store
                → Retriever → LLM (Gemini) → Answer
                → Telemetry Logger
```

---

## Tech Stack

* Backend: Python, Flask
* LLM: Gemini API
* RAG: FAISS or Chroma
* Embeddings: Gemini embeddings
* PDF Parsing: pypdf or pdfplumber
* Frontend: HTML, CSS, Vanilla JS

---

## Requirements

* Python 3.9+
* Gemini API Key

---

## Environment Setup

Create a `.env` file in the root directory based on `.env.example`:

```
GEMINI_API_KEY=your_api_key_here
```

---

## One-Command Run

```bash
pip install -r requirements.txt
python app.py
```

Then open your browser at:

```
http://localhost:5000
```

---

## Offline Evaluation

* Test cases are stored in `tests.json`
* Run evaluation with:

```bash
python eval.py
```

This prints a pass rate based on regex pattern matching.

---

## Safety & Guardrails

* Strict system prompt: only answer from syllabus content
* Prompt injection detection
* Input length limits
* Graceful error handling

---

## Telemetry

Each request logs:

* Timestamp
* Pathway (RAG)
* Latency
* Tokens / cost (if available)

---

## Project Structure (Planned)

```
syllabus-llm-app/
├── app.py
├── rag.py
├── llm.py
├── eval.py
├── logger.py
├── templates/
│   └── index.html
├── static/
│   ├── style.css
│   └── app.js
├── data/
│   ├── uploads/
│   └── vectors/
├── tests.json
├── sample_syllabus.pdf
├── requirements.txt
├── .env.example
└── README.md
```

---

## Known Limitations (Initial)

* Single syllabus at a time
* Text-based answers only
* Accuracy depends on PDF text quality

---

## Demo Video (To Be Added)

A 3–5 minute walkthrough covering:

* Problem statement
* Live demo
* RAG explanation
* Evaluation results

---

## 👨‍🎓 Author

Andrew Weston
