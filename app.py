'''import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
import PyPDF2
import requests
from flask_cors import CORS

# Load .env file
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
if not os.path.exists(dotenv_path):
    raise FileNotFoundError("🌑 .env file not found in project root.")
load_dotenv(dotenv_path=dotenv_path)

# Load API key
api_key = os.getenv("GROQ_API_KEY")
print("🔐 Loaded GROQ_API_KEY:", api_key)
if not api_key:
    raise ValueError("🚫 GROQ_API_KEY not found. Please set it in your .env file.")

# Initialize Flask
app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)

# Generate questions using Groq API
def generate_questions(paragraph, num_mcqs, num_fibs, num_tfs):
    try:
        input_tokens = len(paragraph.split())
        max_input_tokens = 4000
        max_output_tokens = 3000
        max_tokens_limit = 7000
        tokens_per_question = 100

        if input_tokens > max_input_tokens:
            paragraph = " ".join(paragraph.split()[:max_input_tokens])
            input_tokens = len(paragraph.split())

        total_requested_tokens = tokens_per_question * (num_mcqs + num_fibs + num_tfs)
        if total_requested_tokens > max_output_tokens or input_tokens + total_requested_tokens > max_tokens_limit:
            print("⚠️ Token limit exceeded. Try fewer questions.")
            return None

        prompt = f"""
You are an expert AI question generator.
Generate exactly {num_mcqs} multiple-choice questions, {num_fibs} fill-in-the-blank questions, and {num_tfs} True/False questions from the following text:
{paragraph}

Rules:
1. No two questions under the same category should share the same idea, theme, or fact.
2. For fill-in-the-blank questions, remove key terms and replace with "" while keeping grammatical correctness.
3. For True/False questions, ensure each statement is a fact that can be evaluated as True or False.
4. Only generate the exact number of questions requested.

Format the response as follows:

MCQs:
Q1: [Question text]
a) [Option 1]
b) [Option 2]
c) [Option 3]
d) [Option 4]
Answer: [Correct Option]

F-I-Bs:
Q1: [Sentence with a blank like __________]
Answer: [Correct Answer]

T or F:
Q1: [Statement]
Answer: [True/False]
"""

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "llama3-70b-8192",  # ✅ Updated model name
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": total_requested_tokens
        }

        print("🌌 Sending request to Groq...")
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=payload
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]

    except requests.exceptions.HTTPError as http_err:
        print(f"🚨 HTTP error: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"🌧️ Network error: {req_err}")
    except Exception as e:
        print(f"⚠️ Unexpected error: {e}")

    # Optional fallback response
    return """MCQs:
Q1: What is the purpose of aging in scheduling?
a) To reduce CPU usage
b) To increase priority of long-waiting processes
c) To prevent deadlock
d) To allocate memory
Answer: b

F-I-Bs:
Q1: Starvation can be prevented using __________.
Answer: aging

T or F:
Q1: Aging decreases the priority of long-waiting processes.
Answer: False
"""

# Extract text from uploaded PDF
def extract_text_from_pdf(pdf_file):
    try:
        reader = PyPDF2.PdfReader(pdf_file)
        text = "\n".join(page.extract_text() or "" for page in reader.pages).strip()
        return text
    except Exception as e:
        print("📄 PDF extraction error:", e)
        return ""

# Home page
@app.route("/")
def index():
    return render_template("index.html")

# Question generation endpoint
@app.route("/generate", methods=["POST"])
def handle_generation():
    text = request.form.get("text", "").strip()
    file = request.files.get("pdf")
    paragraph = extract_text_from_pdf(file) if file else text

    if not paragraph:
        return jsonify({"error": "No text provided"}), 400

    try:
        mcqs = int(request.form.get("mcqs", 0))
        fibs = int(request.form.get("fibs", 0))
        tfs = int(request.form.get("tfs", 0))
    except ValueError:
        return jsonify({"error": "Invalid question numbers"}), 400

    questions = generate_questions(paragraph, mcqs, fibs, tfs)
    if not questions:
        return jsonify({
            "error": "Failed to generate questions. Try reducing the numbers or checking your API setup."
        }), 500

    return jsonify({"questions": questions})

# Run the app
if __name__ == "__main__":
    print("🌙 Flask app is starting...")
    app.run(debug=True)

    '''

'''
import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
import PyPDF2
import requests
from flask_cors import CORS

# Load .env file
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
if not os.path.exists(dotenv_path):
    raise FileNotFoundError("🌑 .env file not found in project root.")
load_dotenv(dotenv_path=dotenv_path)

# Load API key
api_key = os.getenv("GROQ_API_KEY")
print("🔐 Loaded GROQ_API_KEY:", api_key)
if not api_key:
    raise ValueError("🚫 GROQ_API_KEY not found. Please set it in your .env file.")

# Initialize Flask
app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)

# -------------------- AI Question Generator --------------------
def generate_questions(paragraph, num_mcqs, num_fibs, num_tfs, difficulty="medium"):
    try:
        input_tokens = len(paragraph.split())
        max_input_tokens = 4000
        max_output_tokens = 3000
        max_tokens_limit = 7000
        tokens_per_question = 120

        # Limit input size
        if input_tokens > max_input_tokens:
            paragraph = " ".join(paragraph.split()[:max_input_tokens])
            input_tokens = len(paragraph.split())

        total_requested_tokens = tokens_per_question * (num_mcqs + num_fibs + num_tfs)
        if total_requested_tokens > max_output_tokens or input_tokens + total_requested_tokens > max_tokens_limit:
            return {"error": "⚠️ Token limit exceeded. Try fewer questions."}

        prompt = f"""
You are an expert AI tutor and question generator. 
Generate quiz questions of {difficulty.upper()} difficulty from the following text.

Generate:
- {num_mcqs} multiple-choice questions
- {num_fibs} fill-in-the-blank questions
- {num_tfs} true/false questions

Rules:
1. Questions must be {difficulty.upper()} difficulty.
2. No two questions under the same category should share the same idea or fact.
3. For MCQs: provide 4 options, 1 correct answer, and a short 2–3 line explanation.
4. For FIBs: provide 1 correct answer + explanation.
5. For T/F: provide statement, correct answer, and explanation.

Format your response as **valid JSON** with the structure:
{{
  "mcqs": [
    {{
      "question": "...",
      "options": ["a", "b", "c", "d"],
      "answer": "b",
      "explanation": "..."
    }}
  ],
  "fibs": [
    {{
      "question": "...",
      "answer": "...",
      "explanation": "..."
    }}
  ],
  "tfs": [
    {{
      "question": "...",
      "answer": "True/False",
      "explanation": "..."
    }}
  ]
}}

Text:
{paragraph}
"""

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "llama3-70b-8192",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": total_requested_tokens
        }

        print("🌌 Sending request to Groq...")
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=payload
        )
        response.raise_for_status()

        # Parse JSON output from Groq
        content = response.json()["choices"][0]["message"]["content"].strip()
        print("✅ Raw AI Response:", content[:300], "...")
        return content

    except requests.exceptions.HTTPError as http_err:
        print(f"🚨 HTTP error: {http_err}")
        return {"error": f"HTTP error: {http_err}"}
    except requests.exceptions.RequestException as req_err:
        print(f"🌧️ Network error: {req_err}")
        return {"error": f"Network error: {req_err}"}
    except Exception as e:
        print(f"⚠️ Unexpected error: {e}")
        return {"error": str(e)}

# -------------------- PDF Text Extractor --------------------
def extract_text_from_pdf(pdf_file):
    try:
        reader = PyPDF2.PdfReader(pdf_file)
        text = "\n".join(page.extract_text() or "" for page in reader.pages).strip()
        return text
    except Exception as e:
        print("📄 PDF extraction error:", e)
        return ""

# -------------------- Routes --------------------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def handle_generation():
    text = request.form.get("text", "").strip()
    file = request.files.get("pdf")
    difficulty = request.form.get("difficulty", "medium").lower()
    paragraph = extract_text_from_pdf(file) if file else text

    if not paragraph:
        return jsonify({"error": "No text provided"}), 400

    try:
        mcqs = int(request.form.get("mcqs", 0))
        fibs = int(request.form.get("fibs", 0))
        tfs = int(request.form.get("tfs", 0))
    except ValueError:
        return jsonify({"error": "Invalid question numbers"}), 400

    result = generate_questions(paragraph, mcqs, fibs, tfs, difficulty)
    if not result or "error" in str(result):
        return jsonify({"error": "Failed to generate questions. Try again."}), 500

    return jsonify({"questions": result})

# -------------------- Run --------------------
if __name__ == "__main__":
    print("🌙 Flask app is starting...")
    app.run(debug=True)
'''



import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
import PyPDF2
from groq import Groq
from flask_cors import CORS

# Load .env file explicitly
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
if not os.path.exists(dotenv_path):
    raise FileNotFoundError(".env file not found in project root.")
load_dotenv(dotenv_path=dotenv_path)

# Debug: check if API key is loaded
api_key = os.getenv("GROQ_API_KEY")
print("Loaded GROQ_API_KEY:", api_key)
if not api_key:
    raise ValueError("GROQ_API_KEY not found. Please set it in your .env file.")

# Initialize Flask
app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)

# Initialize Groq client
client = Groq(api_key=api_key)


def generate_questions(paragraph, num_mcqs, num_fibs, num_tfs):
    try:
        input_tokens = len(paragraph.split())
        max_input_tokens = 4000
        max_output_tokens = 3000
        max_tokens_limit = 7000

        if input_tokens > max_input_tokens:
            paragraph = " ".join(paragraph.split()[:max_input_tokens])
            input_tokens = len(paragraph.split())

        tokens_per_question = 100
        total_requested_tokens = tokens_per_question * (num_mcqs + num_fibs + num_tfs)
        if total_requested_tokens > max_output_tokens or input_tokens + total_requested_tokens > max_tokens_limit:
            return None

        prompt = f"""
You are an expert AI question generator.
Generate exactly {num_mcqs} multiple-choice questions, {num_fibs} fill-in-the-blank questions, and {num_tfs} True/False questions from the following text:
{paragraph}

Rules:
1. No two questions under the same category should share the same idea, theme, or fact.
2. For fill-in-the-blank questions, remove key terms and replace with "" while keeping grammatical correctness.
3. For True/False questions, ensure each statement is a fact that can be evaluated as True or False.
4. Only generate the exact number of questions requested.

Format the response as follows:

MCQs:
Q1: [Question text]
a) [Option 1]
b) [Option 2]
c) [Option 3]
d) [Option 4]
Answer: [Correct Option]

F-I-Bs:
Q1: [Sentence with a blank like __________]
Answer: [Correct Answer]

T or F:
Q1: [Statement]
Answer: [True/False]
"""
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",  # updated model
            max_tokens=total_requested_tokens
        )
        return response.choices[0].message.content
    except Exception as e:
        print("Generation error:", e)
        return None


def extract_text_from_pdf(pdf_file):
    try:
        reader = PyPDF2.PdfReader(pdf_file)
        text = "\n".join(page.extract_text() or "" for page in reader.pages).strip()
        return text
    except Exception as e:
        print("PDF extraction error:", e)
        return ""


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def handle_generation():
    text = request.form.get("text", "").strip()
    file = request.files.get("pdf")
    paragraph = extract_text_from_pdf(file) if file else text

    if not paragraph:
        return jsonify({"error": "No text provided"}), 400

    try:
        mcqs = int(request.form.get("mcqs", 0))
        fibs = int(request.form.get("fibs", 0))
        tfs = int(request.form.get("tfs", 0))
    except ValueError:
        return jsonify({"error": "Invalid question numbers"}), 400

    questions = generate_questions(paragraph, mcqs, fibs, tfs)
    if not questions:
        return jsonify(
            {"error": "Failed to generate questions. Try reducing the numbers."}
        ), 500

    return jsonify({"questions": questions})


if __name__ == "__main__":
    app.run(debug=True)
