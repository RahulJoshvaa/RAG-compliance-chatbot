import json
import statistics

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(__file__)
    )
)


# =====================================
# MODEL
# =====================================

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

# =====================================
# LOAD DATA
# =====================================

with open(
    "ragas_dataset.json",
    "r",
    encoding="utf-8"
) as f:

    data = json.load(f)

questions = data["question"][:8]

# =====================================
# IMPORT YOUR PIPELINE
# =====================================

from pipeline import run_pipeline_wo_cache

# =====================================
# CONSISTENCY
# =====================================

scores = []

for idx, question in enumerate(questions):

    print(f"\nQuestion {idx+1}")

    answers = []

    # Generate 3 answers

    for _ in range(3):

        answer = run_pipeline_wo_cache(question)

        answers.append(answer)

    embeddings = model.encode(
        answers
    )

    sim12 = cosine_similarity(
        [embeddings[0]],
        [embeddings[1]]
    )[0][0]

    sim13 = cosine_similarity(
        [embeddings[0]],
        [embeddings[2]]
    )[0][0]

    sim23 = cosine_similarity(
        [embeddings[1]],
        [embeddings[2]]
    )[0][0]

    consistency = (
        sim12 +
        sim13 +
        sim23
    ) / 3

    scores.append(consistency)

    print(
        f"Consistency = {consistency:.4f}"
    )

# =====================================
# FINAL
# =====================================

overall = statistics.mean(scores)

print("\n==========================")
print("ANSWER CONSISTENCY")
print("==========================")

print(
    f"Average Consistency = "
    f"{overall:.4f}"
)