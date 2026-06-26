# RAG Compliance Chatbot [cite: 1]

## Overview
This repository contains the source code for a Retrieval-Augmented Generation (RAG) Compliance Chatbot [cite: 1]. The chatbot is designed to navigate and answer queries based on complex financial and operational resilience regulations [cite: 1].

## Knowledge Base
The chatbot retrieves context from the following core regulatory documents [cite: 1]:
* **CR III Regulation 2024** [cite: 1]
* **DORA EU 2554** (Digital Operational Resilience Act) [cite: 1]
* **FATF 40 Recommendations 2012** (Financial Action Task Force standards) [cite: 1]

## Repository Structure [cite: 1]

```text
RAG-compliance-chatbot-main/
├── FrontEnd/
│   └── index.js                 # Frontend application entry point
└── generation/                  # Core RAG backend (Python)
    ├── compress.py              # Context compression / summarization logic
    ├── control_group.py         # Evaluation and baseline testing controls
    ├── llm_client.py            # Client interface for the Large Language Model
    ├── mock_retriever.py        # Retriever module for testing/mocking document fetch
    ├── pipeline.py              # Main RAG execution pipeline
    ├── prompt_builder.py        # Logic for constructing LLM prompts with context
    ├── semantic_cache.py        # Caching layer for semantic query matching
    ├── requirements.txt         # Python dependencies
    └── src/
        └── data/                # Regulatory document corpus
            ├── CR III Regulation 2024.pdf
            ├── DORA EU 2554.pdf
            └── FATF 40 Recommendations 2012.pdf
```

## Architecture Inference
Based on the file structure [cite: 1], the backend operations follow a typical RAG architecture:
1. **Frontend:** A JavaScript-based user interface (`FrontEnd/index.js`) captures user queries [cite: 1].
2. **RAG Pipeline:** The query is routed to the Python backend (`generation/pipeline.py`) [cite: 1].
3. **Caching:** `semantic_cache.py` checks if a semantically similar query has been answered recently to optimize speed and cost [cite: 1].
4. **Retrieval & Compression:** Context is retrieved (supported by `mock_retriever.py`) from the regulatory PDFs and compacted using `compress.py` to extract only the most relevant text segments [cite: 1].
5. **Prompting & Generation:** `prompt_builder.py` combines the compressed context with the user query, and `llm_client.py` sends the structured prompt to the language model to generate the final response [cite: 1].

## Setup Instructions (Inferred)
**Backend:**
```bash
cd RAG-compliance-chatbot-main/generation
pip install -r requirements.txt
python pipeline.py
```

**Frontend:**
```bash
cd RAG-compliance-chatbot-main/FrontEnd
node index.js
```
