import os
import time
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

# TODO: Local modules
from rag import process_document, answer_question
from logger import log_request

load_dotenv()

UPLOAD_FOLDER = "data/uploads"
ALLOWED_EXTENSIONS = {"pdf"}

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Simple in-memory state (single syllabus at a time for v1)
CURRENT_INDEX_READY = False


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_file():
    global CURRENT_INDEX_READY

    if "file" not in request.files:
        return jsonify({"error": "No file part in the request."}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No file selected."}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "Only PDF files are supported."}), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(file_path)

    try:
        process_document(file_path)
        CURRENT_INDEX_READY = True
        return jsonify({"message": "Syllabus uploaded and processed successfully."})
    except Exception as e:
        return jsonify({"error": f"Failed to process document: {str(e)}"}), 500


@app.route("/ask", methods=["POST"])
def ask_question():
    global CURRENT_INDEX_READY

    start_time = time.time()

    if not CURRENT_INDEX_READY:
        return jsonify({"error": "No syllabus uploaded yet."}), 400

    data = request.get_json()
    question = data.get("question", "")

    # Safety: input length guard
    if len(question) > 500:
        return jsonify({"error": "Question too long. Please shorten it."}), 400

    # Safety: basic prompt-injection detection
    blocked_phrases = [
        "ignore previous instructions",
        "system override",
        "act as dan"
    ]

    lower_q = question.lower()
    for phrase in blocked_phrases:
        if phrase in lower_q:
            return jsonify({"error": "Unsafe prompt detected."}), 400

    try:
        answer = answer_question(question)
    except Exception as e:
        return jsonify({"error": f"LLM error: {str(e)}"}), 500

    latency_ms = int((time.time() - start_time) * 1000)

    # Telemetry logging
    log_request(
        pathway="RAG",
        latency_ms=latency_ms,
        tokens=None
    )

    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(debug=True)