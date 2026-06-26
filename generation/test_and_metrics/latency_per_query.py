import json
import statistics
import time
import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(__file__)
    )
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
# IMPORT PIPELINE
# =====================================================

from pipeline import run_pipeline_wo_cache

# =====================================================
# MEASURE LATENCY
# =====================================================

latencies_ms = []

print("\nMeasuring latency per query...\n")

for idx, query in enumerate(
    questions,
    start=1
):

    print("=" * 60)

    print(
        f"Question {idx}/{len(questions)}"
    )

    print(query[:80] + "...")

    start = time.perf_counter()

    run_pipeline_wo_cache(query)

    end = time.perf_counter()

    elapsed_ms = (end - start) * 1000

    latencies_ms.append(elapsed_ms)

    print(
        f"Latency : {elapsed_ms:.1f} ms"
    )

# =====================================================
# SUMMARY
# =====================================================

avg_latency = statistics.mean(
    latencies_ms
)

min_latency = min(latencies_ms)

max_latency = max(latencies_ms)

p50 = statistics.median(latencies_ms)

sorted_lat = sorted(latencies_ms)

p95_idx = int(
    len(sorted_lat) * 0.95
)

p95 = sorted_lat[
    min(p95_idx, len(sorted_lat) - 1)
]

print("\n" + "=" * 60)

print("LATENCY PER QUERY")

print("=" * 60)

print(
    f"Avg Latency  : "
    f"{avg_latency:.1f} ms"
)

print(
    f"Min Latency  : "
    f"{min_latency:.1f} ms"
)

print(
    f"Max Latency  : "
    f"{max_latency:.1f} ms"
)

print(
    f"P50 Latency  : "
    f"{p50:.1f} ms"
)

print(
    f"P95 Latency  : "
    f"{p95:.1f} ms"
)
