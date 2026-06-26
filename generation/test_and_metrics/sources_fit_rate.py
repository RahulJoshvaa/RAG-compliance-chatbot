import json
import re
import statistics
import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(__file__)
    )
)

from config import GEMINI_API_KEY, GEMINI_MODEL
import google.generativeai as genai
from src.retrieve import retrieve_context

# =====================================================
# CONFIG
# =====================================================

genai.configure(
    api_key=GEMINI_API_KEY
)

model = genai.GenerativeModel(
    GEMINI_MODEL
)

# =====================================================
# LOAD DATA
# =====================================================

with open(
    "ragas_dataset.json",
    "r",
    encoding="utf-8"
) as f:

    data = json.load(f)

questions = data["question"]

# =====================================================
# HELPER
# =====================================================

def extract_score(text):

    match = re.search(
        r"([0-1](?:\.\d+)?)",
        text
    )

    if match:
        return float(match.group(1))

    return 0.0


# =====================================================
# SOURCES FIT RATE
# =====================================================

def source_fit_score(
    query,
    source_text
):

    prompt = f"""
You are evaluating retrieval quality
for a RAG system.

QUERY:
{query}

SOURCE CHUNK:
{source_text}

Determine whether this source chunk
contains information that is genuinely
useful for answering the query.

Scoring:

1.0 = directly useful

0.5 = partially useful

0.0 = not useful / off-topic

Return ONLY a score in range 0 - 1.
"""

    response = model.generate_content(
        prompt
    )

    return extract_score(
        response.text
    )


# =====================================================
# EVALUATION
# =====================================================

per_query_fit_rates = []

print("\nMeasuring sources fit rate...\n")

for idx, query in enumerate(
    questions,
    start=1
):

    print("=" * 60)

    print(
        f"Question {idx}/{len(questions)}"
    )

    chunks = retrieve_context(query)

    source_scores = []

    for chunk in chunks:

        text = chunk["text"]

        score = source_fit_score(
            query,
            text
        )

        source_scores.append(score)

    if source_scores:

        fit_rate = statistics.mean(
            source_scores
        )

    else:

        fit_rate = 0.0

    per_query_fit_rates.append(fit_rate)

    print(
        f"Sources Fit Rate : "
        f"{fit_rate:.3f} "
        f"({len(source_scores)} sources)"
    )

# =====================================================
# SUMMARY
# =====================================================

avg_fit_rate = statistics.mean(
    per_query_fit_rates
)

print("\n" + "=" * 60)

print("SOURCES FIT RATE")

print("=" * 60)

print(
    f"Average Sources Fit Rate : "
    f"{avg_fit_rate:.3f}"
)
