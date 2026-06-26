import json
import statistics
import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(__file__)
    )
)

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# =====================================================
# MODEL
# =====================================================

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
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

# =====================================================
# ANSWER RELEVANCE
# =====================================================

# Measures how well the generated answer
# addresses the original question.
# Score = cosine similarity between
# question embedding and answer embedding.

scores = []

for idx, (question, answer) in enumerate(
    zip(questions, answers),
    start=1
):

    print("=" * 60)

    print(
        f"Question {idx}/{len(questions)}"
    )

    q_emb = model.encode([question])

    a_emb = model.encode([answer])

    similarity = cosine_similarity(
        q_emb,
        a_emb
    )[0][0]

    scores.append(similarity)

    print(
        f"Answer Relevance : "
        f"{similarity:.4f}"
    )

# =====================================================
# SUMMARY
# =====================================================

avg_relevance = statistics.mean(scores)

min_relevance = min(scores)

max_relevance = max(scores)

print("\n" + "=" * 60)

print("ANSWER RELEVANCE")

print("=" * 60)

print(
    f"Average Relevance : "
    f"{avg_relevance:.4f}"
)

print(
    f"Min Relevance     : "
    f"{min_relevance:.4f}"
)

print(
    f"Max Relevance     : "
    f"{max_relevance:.4f}"
)
