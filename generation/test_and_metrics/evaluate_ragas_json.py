import json
import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(__file__)
    )
)

from pipeline import run_pipeline
from src.retrieve import retrieve_context

questions = [

    # CR III

    "Why was Regulation EU 2024/1623 introduced?",
    "What is the purpose of the Basel III output floor?",
    "What percentage is used for the output floor?",
    "Why were changes made to the Standardised Approach for credit risk?",
    "How does the new operational risk framework differ from previous approaches?",

    # FATF

    "What is the purpose of the FATF Recommendations?",
    "What is the risk-based approach under FATF Recommendation 1?",
    "What is Customer Due Diligence according to FATF?",
    "What is the purpose of targeted financial sanctions under Recommendation 6?",
    "Why are non-profit organisations addressed in Recommendation 8?"
]

ground_truth = [

    "The regulation was introduced to implement the remaining Basel III reforms and improve banking resilience.",

    "The output floor limits excessive reductions in capital requirements produced by internal models.",

    "The output floor is set at 72.5 percent of standardized capital requirements.",

    "The Standardised Approach was revised because it was not sufficiently risk-sensitive.",

    "The new framework replaces previous operational risk approaches with a single standardized approach.",

    "The FATF Recommendations provide an international framework for combating money laundering and terrorist financing.",

    "The risk-based approach requires institutions to identify, assess and mitigate risks proportional to their severity.",

    "Customer Due Diligence requires identifying and verifying customers and understanding risk.",

    "Recommendation 6 requires freezing assets of designated terrorists and terrorist organisations.",

    "Recommendation 8 prevents misuse of non-profit organisations for terrorist financing."
]

answers = []
contexts = []

for q in questions:

    print(f"Generating -> {q}")

    retrieved = retrieve_context(q)

    ctx = [
        chunk["text"]
        for chunk in retrieved
    ]

    answer = run_pipeline(q)

    answers.append(answer)
    contexts.append(ctx)

data = {
    "question": questions,
    "answer": answers,
    "contexts": contexts,
    "ground_truth": ground_truth
}

with open("ragas_dataset.json", "w", encoding="utf-8") as f:
    json.dump(
        data,
        f,
        indent=2,
        ensure_ascii=False
    )

print("\nDataset exported -> ragas_dataset.json")