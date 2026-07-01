import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(__file__)
    )
)


import re
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