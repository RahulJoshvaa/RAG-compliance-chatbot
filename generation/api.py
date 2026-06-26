"""
HTTP API for the RAG chatbot.
"""

import os
import sys

sys.path.append(os.path.dirname(__file__))

from flask import Flask, request, jsonify
from flask_cors import CORS

from config import GROQ_API_KEY, GROQ_MODEL
from pipeline import (
    run_pipeline,
    run_traditional_pipeline,
)

# ---------------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------------

BASE_DIR = os.path.dirname(__file__)
CHROMA_PATH = os.path.join(BASE_DIR, "src", "chroma_db")

# ---------------------------------------------------------------------------
# LIVE / DEMO CHECK
# ---------------------------------------------------------------------------

LIVE = False
INIT_ERROR = None

try:

    if not GROQ_API_KEY:
        raise RuntimeError(
            "GROQ_API_KEY is not set."
        )

    if not os.path.isdir(CHROMA_PATH):
        raise RuntimeError(
            "Chroma index not found."
        )

    LIVE = True
    print(f"[api] LIVE mode — model={GROQ_MODEL}")

except Exception as e:
    INIT_ERROR = str(e)
    print(f"[api] DEMO mode — {INIT_ERROR}")

# ---------------------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------------------

def is_api_key_error(err):

    text = str(err).lower()

    signals = [
        "api key",
        "api_key",
        "quota",
        "rate limit",
        "429",
        "permission_denied",
        "unauthenticated",
        "401",
        "403",
        "invalid",
        "expired",
    ]

    return any(signal in text for signal in signals)


# ---------------------------------------------------------------------------
# DEMO MODE
# ---------------------------------------------------------------------------

def demo_chat(query, mode):

    return {
        "answer": (
            f'Demo response ({mode}). '
            f'You asked: "{query}". '
            "Configure the Groq API key and build the Chroma index "
            "to enable the live backend."
        ),
        "sources": [
            {
                "source": "Demo.pdf",
                "page": 1
            }
        ],
        "mode": mode,
        "live": False,
        "metrics": {
            "latency": 0.40
        }
    }


# ---------------------------------------------------------------------------
# FLASK
# ---------------------------------------------------------------------------

app = Flask(__name__)
CORS(app)


@app.get("/api/health")
def health():

    return jsonify(
        {
            "live": LIVE,
            "model": GROQ_MODEL if LIVE else None,
            "error": INIT_ERROR,
        }
    )


@app.post("/api/chat")
def chat():

    data = request.get_json(silent=True) or {}

    query = (data.get("query") or "").strip()
    mode = (data.get("mode") or "COMPRESSED RAG").upper()

    if not query:
        return jsonify(
            {
                "error": "query is required"
            }
        ), 400

    try:

        if not LIVE:
            return jsonify(
                demo_chat(query, mode)
            )

        if mode == "COMPRESSED RAG":

            result = run_pipeline(query)

        elif mode == "TRADITIONAL RAG":

            result = run_traditional_pipeline(query)

        else:

            return jsonify(
                {
                    "error": "Invalid mode"
                }
            ), 400

        return jsonify(result)

    except Exception as e:

        if is_api_key_error(e):

            return jsonify(
                {
                    "answer":
                        "⚠️ Groq API limit reached. Please try again later.",
                    "sources": [],
                    "mode": mode,
                    "live": LIVE,
                    "metrics": None,
                }
            )

        return jsonify(
            {
                "error": str(e)
            }
        ), 500


if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=8000,
        debug=False
    )