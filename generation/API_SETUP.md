# Backend API ↔ FrontEnd Integration

The FrontEnd talks to the RAG pipeline through a small Flask API (`generation/api.py`).
It runs in one of two modes, decided automatically at startup:

| Mode | When | Behaviour |
|------|------|-----------|
| **LIVE** | full deps installed **+** `GEMINI_API_KEY` set **+** Chroma index built | Real retrieval, Gemini generation, real metrics |
| **DEMO** | anything above missing | Placeholder answers + plausible metrics so the UI still works |

## Run it (DEMO mode — works immediately)

```bash
# Terminal 1 — backend
cd generation
pip install -r api_requirements.txt
python api.py                      # http://localhost:8000

# Terminal 2 — frontend
cd FrontEnd
npm install
npm run dev                        # http://localhost:5173
```

The Vite dev server proxies `/api/*` to `http://localhost:8000` (see `vite.config.js`),
so no CORS config is needed in the browser.

## Upgrade to LIVE mode

1. **Install the full backend deps:**
   ```bash
   cd generation
   pip install -r requirements.txt -r src/requirements.txt -r api_requirements.txt
   ```

2. **Set your Gemini key** (config.py reads it from the environment):
   ```bash
   # PowerShell
   $env:GEMINI_API_KEY = "your-key"
   # bash
   export GEMINI_API_KEY="your-key"
   ```
   Optionally override the model: `GEMINI_MODEL` (default `gemini-1.5-flash`).

3. **Build the vector index** (one-time, processes the PDFs in `src/data/`):
   ```bash
   cd generation/src
   python ingest.py               # creates chroma_db/ + parent_document_store.json
   ```

4. **Restart the API** — on startup it prints `[api] LIVE mode — model=…`.

## API reference

### `GET /api/health`
```json
{ "live": true, "model": "gemini-1.5-flash", "error": null }
```

### `POST /api/chat`
Request:
```json
{ "query": "What does DORA require for ICT risk?", "mode": "COMPRESSED RAG" }
```
`mode` is `"COMPRESSED RAG"` or `"TRADITIONAL RAG"`.

Response:
```json
{
  "answer": "…",
  "sources": [{ "source": "DORA EU 2554.pdf", "page": 12 }],
  "mode": "COMPRESSED RAG",
  "live": true,
  "metrics": {
    "latency": 0.84,
    "tokens": 1180,
    "prompt_tokens": 1040,
    "output_tokens": 140,
    "relevance": 0.91,
    "cost_per_1k": 0.12,
    "compression_ratio": 0.55
  }
}
```

The four StatsBar tiles map to `latency`, `tokens`, `relevance`, and `cost_per_1k`.

> **Note on "relevance":** true RAGAS context recall needs ground-truth answers,
> which aren't available at query time. The live `relevance` value is a
> retrieval-quality proxy — the mean cosine similarity between the query and the
> retrieved chunks (using the same BGE embedding model as the compressor). The
> ground-truth-based metrics live in `test_and_metrics/`.
