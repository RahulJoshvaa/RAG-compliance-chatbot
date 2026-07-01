# =====================================================
# K TUNING USING CONTEXT RECALL
# =====================================================
import statistics
test_questions = [
    "Why was Regulation EU 2024/1623 introduced?",
    "What is the purpose of the Basel III output floor?",
    "Why were changes made to the Standardised Approach for credit risk?",
    "How does the new operational risk framework differ from previous approaches?",
    "What is the purpose of the FATF Recommendations?",
    "What is the risk-based approach under FATF Recommendation 1?",
    "What is Customer Due Diligence according to FATF?",
    "What is the purpose of targeted financial sanctions under Recommendation 6?",
    "Why are non-profit organisations addressed in Recommendation 8?"
]

ground_truths = [
    "The regulation was introduced to implement the remaining Basel III reforms and improve banking resilience.",
    "The output floor limits excessive reductions in capital requirements produced by internal models.",
    "The Standardised Approach was revised because it was not sufficiently risk-sensitive.",
    "The new framework replaces previous operational risk approaches with a single standardized approach.",
    "The FATF Recommendations provide an international framework for combating money laundering and terrorist financing.",
    "The risk-based approach requires institutions to identify, assess and mitigate risks proportional to their severity.",
    "Customer Due Diligence requires identifying and verifying customers and understanding risk.",
    "Recommendation 6 requires freezing assets of designated terrorists and terrorist organisations.",
    "Recommendation 8 prevents misuse of non-profit organisations for terrorist financing."
]

import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(__file__)
    )
)

from src.retrieve import retrieve_context
from test_and_metrics.context_recall import context_recall_score

def evaluate_k(k):

    recalls = []

    for question, gt in zip(
        test_questions,
        ground_truths
    ):

        contexts = retrieve_context(
            question,
            top_k=k
        )


        context_texts = [
            ctx["text"]
            for ctx in contexts
        ]

        recall = context_recall_score(
            context_texts,
            gt
        )
        print(
            f"Question: {question}"
        )
        print(
            f"Recall: {recall}"
        )
        print("-" * 50)

        recalls.append(recall)

    return statistics.mean(recalls)


candidate_ks = [1, 2, 3, 4, 5, 6, 8, 10]

results = {}

print("\nFinding Optimal K...\n")

for k in candidate_ks:

    avg_recall = evaluate_k(k)

    results[k] = avg_recall

    print(
        f"K = {k:<2} | "
        f"Average Recall = {avg_recall:.3f}"
    )

best_recall = max(
    results.values()
)

threshold = best_recall * 0.95

optimal_k = min(
    k
    for k, score in results.items()
    if score >= threshold
)

print("\n" + "=" * 50)

print(
    f"Best Recall : {best_recall:.3f}"
)

print(
    f"Optimal K   : {optimal_k}"
)

print("=" * 50)