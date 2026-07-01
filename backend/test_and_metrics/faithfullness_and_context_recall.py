import json
import re
import statistics
import time
import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(__file__)
    )
)

from groq import Groq
from config import GROQ_API_KEY

# =====================================================
# CONFIG
# =====================================================

MODEL = "openai/gpt-oss-120b"

client = Groq(
    api_key=GROQ_API_KEY
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


def ask_llm(prompt):

    response = client.chat.completions.create(
        model=MODEL,
        temperature=0,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content.strip()


# =====================================================
# FAITHFULNESS
# =====================================================

def faithfulness_score(
    answer,
    contexts
):

    context_text = "\n\n".join(contexts)

    prompt = f"""
You are evaluating a Retrieval-Augmented Generation (RAG) system.

Task:
Determine whether the Generated Answer is supported by the Retrieved Context.

Rules:
- Compare ONLY the Generated Answer against the Retrieved Context.
- Ignore wording differences.
- Consider paraphrases and semantically equivalent information as supported.
- Ignore information that is not relevant.

Scoring:
1.0 = completely supported
0.8 = mostly supported
0.5 = partially supported
0.0 = unsupported

Return ONLY one number:
1.0
0.8
0.5
0.0

Retrieved Context:
{context_text}

Generated Answer:
{answer}
"""

    return extract_score(
        ask_llm(prompt)
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
You are evaluating Context Recall for a Retrieval-Augmented Generation (RAG) system.

Task:
Determine how much of the factual information contained in the Ground Truth is present in the Retrieved Context.

Rules:
- Compare ONLY the Ground Truth and the Retrieved Context.
- Ignore wording differences.
- Consider paraphrases and semantically equivalent facts as present.
- Ignore additional information in the Retrieved Context.
- Judge only whether the Ground Truth can be completely derived from the Retrieved Context.

Scoring:
1.0 = All important facts are present.
0.8 = Most important facts are present.
0.5 = Some important facts are present.
0.0 = None of the important facts are present.

Return ONLY one number:
1.0
0.8
0.5
0.0

Ground Truth:
{ground_truth}

Retrieved Context:
{context_text}
"""

    return extract_score(
        ask_llm(prompt)
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
answers = data["answer"]
contexts = data["contexts"]
ground_truths = data["ground_truth"]

# =====================================================
# EVALUATION
# =====================================================

faithfulness_scores = []
recall_scores = []

print("\nRunning Mock RAGAS...\n")

for i in range(len(questions)):

    print("=" * 60)
    print(f"Question {i+1}/{len(questions)}")

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

    print(f"Faithfulness   : {faith:.2f}")
    print(f"Context Recall : {recall:.2f}")

    # Helps avoid hitting rate limits
    time.sleep(0.5)


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
    f"Faithfulness   : {avg_faithfulness:.3f}"
)

print(
    f"Context Recall : {avg_recall:.3f}"
)

print(
    f"Overall Score  : {overall:.3f}"
)