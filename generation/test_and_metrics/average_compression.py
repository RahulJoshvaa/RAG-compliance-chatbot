


import sys
import os
import json
sys.path.append(
    os.path.dirname(
        os.path.dirname(__file__)
    )
)

from src.retrieve import retrieve_context
from compress import compress_context

with open(
    "ragas_dataset.json",
    "r",
    encoding="utf-8"
) as f:

    data = json.load(f)

questions = data["question"]


def evaluate_compression():

    ratios = []

    for idx, query in enumerate(
        questions,
        start=1
    ):

        print("\n" + "=" * 70)
        print(f"Question {idx}")
        print(query)

        chunks = retrieve_context(query)

        result = compress_context(
            query,
            chunks
        )

        ratio = result[
            "c_ratio"
        ]

        ratios.append(ratio)

        print(
            f"Compression Ratio: "
            f"{ratio:.2f}"
        )

    average_ratio = (
        sum(ratios) /
        len(ratios)
    )

    average_reduction = (
        1 - average_ratio
    ) * 100

    print("\n" + "=" * 70)

    print(
        f"Average Compression Ratio: "
        f"{average_ratio:.2f}"
    )

    print(
        f"Average Token Reduction: "
        f"{average_reduction:.2f}%"
    )


if __name__ == "__main__":
    evaluate_compression()