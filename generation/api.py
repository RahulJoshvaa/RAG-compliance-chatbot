"""
HTTP API that bridges the RAG generation pipeline with the FrontEnd.

Run:
    cd generation
    python api.py            # serves on http://localhost:8000

Endpoints:
    GET  /api/health         -> backend status + which mode is live
    POST /api/chat           -> { query, mode } => { answer, sources, metrics }

The server runs in one of two modes, chosen automatically at startup:

  * LIVE  — the full RAG stack is importable, GEMINI_API_KEY is set, and the
            Chroma index exists. Real retrieval + Gemini generation + real
            metrics (latency, tokens, retrieval relevance, cost).

  * DEMO  — anything above is missing. Returns clearly-labelled placeholder
            answers with plausible metrics so the UI is fully usable while the
            backend is being set up.
"""

import os
import sys
import time

sys.path.append(os.path.dirname(__file__))

from flask import Flask, request, jsonify
from flask_cors import CORS

from config import GEMINI_API_KEY, GEMINI_MODEL

# ---------------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """
You are a financial compliance assistant.

Rules:
1. Answer only using the provided context.
2. Do not hallucinate.
3. Be concise and accurate.
"""

# Gemini 2.5 Flash pricing (USD per 1M tokens). Update if GEMINI_MODEL differs.
INPUT_COST_PER_1M = 0.30
OUTPUT_COST_PER_1M = 2.50

BASE_DIR = os.path.dirname(__file__)
CHROMA_PATH = os.path.join(BASE_DIR, "src", "chroma_db")

# ---------------------------------------------------------------------------
# TRY TO LOAD THE LIVE RAG STACK
# ---------------------------------------------------------------------------

LIVE = False
INIT_ERROR = None

try:
    import google.generativeai as genai
    from sentence_transformers import util as st_util
    from src.retrieve import retrieve_context
    from compress import compress_context, model as embed_model

    if not GEMINI_API_KEY:
        raise RuntimeError(
            "GEMINI_API_KEY is not set (export it or add it to config.py)"
        )

    if not os.path.isdir(CHROMA_PATH):
        raise RuntimeError(
            "Chroma index not found — run `python ingest.py` inside generation/src"
        )

    genai.configure(api_key=GEMINI_API_KEY)
    gemini = genai.GenerativeModel(GEMINI_MODEL)

    LIVE = True
    print(f"[api] LIVE mode — model={GEMINI_MODEL}")

except Exception as e:  # noqa: BLE001 - any failure means we fall back to demo
    INIT_ERROR = str(e)
    print(f"[api] DEMO mode — {INIT_ERROR}")


# ---------------------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------------------

def is_compressed(mode):
    return str(mode).upper().startswith("COMP")


def build_metrics(latency, prompt_tok, out_tok, relevance, c_ratio):
    total_tok = prompt_tok + out_tok

    cost = (
        (prompt_tok / 1_000_000) * INPUT_COST_PER_1M
        + (out_tok / 1_000_000) * OUTPUT_COST_PER_1M
    )

    return {
        "latency": round(latency, 2),            # seconds
        "tokens": int(total_tok),                # total tokens this query
        "prompt_tokens": int(prompt_tok),
        "output_tokens": int(out_tok),
        "relevance": round(float(relevance), 3),  # 0-1 retrieval relevance
        "cost_per_1k": round(cost * 1000, 4),    # USD per 1000 queries
        "compression_ratio": round(float(c_ratio), 2),
    }


def dedupe_sources(chunks):
    seen = set()
    sources = []
    for c in chunks:
        key = (c.get("source"), c.get("page"))
        if key in seen:
            continue
        seen.add(key)
        sources.append(
            {"source": c.get("source"), "page": c.get("page")}
        )
    return sources


def is_api_key_error(err):
    """True when the failure looks like a Gemini key / quota / auth problem."""
    text = str(err).lower()
    signals = [
        "api key",
        "api_key",
        "quota",
        "resource_exhausted",
        "rate limit",
        "429",
        "permission_denied",
        "unauthenticated",
        "401",
        "403",
        "invalid",
        "expired",
        "not found",  # retired / unavailable model
    ]
    return any(s in text for s in signals)


def compute_relevance(query, chunk_texts):
    if not chunk_texts:
        return 0.0
    q = embed_model.encode(query, convert_to_tensor=True)
    cs = embed_model.encode(chunk_texts, convert_to_tensor=True)
    sims = st_util.cos_sim(q, cs)[0]
    return float(sims.mean())


# ---------------------------------------------------------------------------
# CHAT HANDLERS
# ---------------------------------------------------------------------------

def live_chat(query, mode):
    t0 = time.perf_counter()

    chunks = retrieve_context(query, top_k=4)
    chunk_texts = [c["text"] for c in chunks]

    if is_compressed(mode) and chunk_texts:
        comp = compress_context(query, chunks)
        context_text = comp.get("compressed_text", "")
        c_ratio = comp.get("c_ratio", 1.0)
    else:
        context_text = "\n\n".join(chunk_texts)
        c_ratio = 1.0

    prompt = f"""
{SYSTEM_PROMPT}

CONTEXT:
{context_text}

QUESTION:
{query}
"""

    response = gemini.generate_content(prompt)
    answer = response.text
    latency = time.perf_counter() - t0

    usage = getattr(response, "usage_metadata", None)
    if usage is not None:
        prompt_tok = usage.prompt_token_count
        out_tok = usage.candidates_token_count
    else:
        prompt_tok = len(prompt) // 4
        out_tok = len(answer) // 4

    relevance = compute_relevance(query, chunk_texts)

    return {
        "answer": answer,
        "sources": dedupe_sources(chunks),
        "mode": mode,
        "live": True,
        "metrics": build_metrics(
            latency, prompt_tok, out_tok, relevance, c_ratio
        ),
    }


def demo_chat(query, mode):
    t0 = time.perf_counter()
    compressed = is_compressed(mode)

    time.sleep(0.4)  # simulate retrieval + generation latency

    answer = (
        f'Demo response ({mode}). You asked: "{query}". '
        "The live RAG backend isn't fully configured yet, so this is a "
        "placeholder. Once GEMINI_API_KEY is set and the Chroma index is "
        "built, you'll get grounded, citation-backed answers from the "
        "compliance knowledge base."
    )

    latency = time.perf_counter() - t0

    base = len(query.split()) * 12 + 240
    prompt_tok = int(base * (0.6 if compressed else 1.0))
    out_tok = 90
    relevance = 0.82 if compressed else 0.77
    c_ratio = 0.55 if compressed else 1.0

    sources = [
        {"source": "DORA EU 2554.pdf", "page": 12},
        {"source": "FCA CONSUMER DUTY fg22-5.pdf", "page": 4},
    ]

    return {
        "answer": answer,
        "sources": sources,
        "mode": mode,
        "live": False,
        "metrics": build_metrics(
            latency, prompt_tok, out_tok, relevance, c_ratio
        ),
    }


# ---------------------------------------------------------------------------
# FLASK APP
# ---------------------------------------------------------------------------

app = Flask(__name__)
CORS(app)


@app.get("/api/health")
def health():
    return jsonify(
        {
            "live": LIVE,
            "model": GEMINI_MODEL if LIVE else None,
            "error": INIT_ERROR,
        }
    )


@app.post("/api/chat")
def chat():
    data = request.get_json(silent=True) or {}
    query = (data.get("query") or "").strip()
    mode = data.get("mode") or "COMPRESSED RAG"

    if not query:
        return jsonify({"error": "query is required"}), 400

    try:
        if LIVE:
            result = live_chat(query, mode)
        else:
            result = demo_chat(query, mode)
        return jsonify(result)
    except Exception as e:  # noqa: BLE001
        if is_api_key_error(e):
            # Friendly, user-facing message instead of a raw 500 / stack detail.
            return jsonify(
                {
                    "answer": (
                        "⚠️ The AI assistant is taking a quick breather. "
                        "This usually means the Gemini API key has hit its rate "
                        "limit or quota for now. Please wait a moment and try "
                        "your question again."
                    ),
                    "sources": [],
                    "mode": mode,
                    "live": LIVE,
                    "metrics": None,
                    "notice": "api_limit",
                }
            )
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=False)
