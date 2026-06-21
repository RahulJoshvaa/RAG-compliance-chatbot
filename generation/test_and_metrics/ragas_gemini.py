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

# =====================================================
# CONFIG
# =====================================================

GOOGLE_API_KEY = GEMINI_API_KEY

genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel(
    GEMINI_MODEL
)

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
# FAITHFULNESS
# =====================================================

def faithfulness_score(
    answer,
    contexts
):

    context_text = "\n\n".join(contexts)

    prompt = f"""
You are evaluating a RAG system.

CONTEXT:
{context_text}

ANSWER:
{answer}

Determine whether the answer is supported
by the retrieved context.

Scoring:

1.0 = completely supported

0.8 = mostly supported

0.5 = partially supported

0.0 = unsupported

Return ONLY a score in range 0 - 1.
"""

    response = model.generate_content(
        prompt
    )

    return extract_score(
        response.text
    )


# =====================================================
# CONTEXT RECALL
# =====================================================

def context_recall_score(
    contexts,
    ground_truth
):

    context_text = "\n\n".join(contexts)

    prompt = f"""
You are evaluating retrieval quality.

GROUND TRUTH:
{ground_truth}

RETRIEVED CONTEXT:
{context_text}

Determine how much of the ground truth
information is present inside the
retrieved context.

Scoring:

1.0 = everything present

0.8 = most present

0.5 = partially present

0.0 = absent

Return ONLY a score in range 0 - 1.
"""

    response = model.generate_content(
        prompt
    )

    return extract_score(
        response.text
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

questions = data["question"][:8]

answers = data["answer"][:8]

contexts = data["contexts"][:8]

ground_truths = data["ground_truth"][:8]

# =====================================================
# EVALUATION
# =====================================================

faithfulness_scores = []

recall_scores = []

print("\nRunning Mock RAGAS...\n")

for i in range(len(questions)):

    print("=" * 60)

    print(
        f"Question {i+1}/{len(questions)}"
    )

    faith = faithfulness_score(
        answers[i],
        contexts[i]
    )

    recall = context_recall_score(
        contexts[i],
        ground_truths[i]
    )

    faithfulness_scores.append(
        faith
    )

    recall_scores.append(
        recall
    )

    print(
        f"Faithfulness : {faith:.2f}"
    )

    print(
        f"Context Recall : {recall:.2f}"
    )

# =====================================================
# SUMMARY
# =====================================================

avg_faithfulness = statistics.mean(
    faithfulness_scores
)

avg_recall = statistics.mean(
    recall_scores
)

overall = (
    avg_faithfulness +
    avg_recall
) / 2

print("\n")
print("=" * 60)

print("FINAL RESULTS")

print("=" * 60)

print(
    f"Faithfulness     : "
    f"{avg_faithfulness:.3f}"
)

print(
    f"Context Recall   : "
    f"{avg_recall:.3f}"
)

print(
    f"Overall Score    : "
    f"{overall:.3f}"
)