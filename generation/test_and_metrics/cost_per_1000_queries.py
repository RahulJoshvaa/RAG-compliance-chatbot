import json
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
from prompt_builder import build_prompt

# =====================================================
# CONFIG
# =====================================================

genai.configure(
    api_key=GEMINI_API_KEY
)

model = genai.GenerativeModel(
    GEMINI_MODEL
)

# Gemini 1.5 Flash pricing (USD per 1M tokens)
# Update these if your GEMINI_MODEL differs

INPUT_COST_PER_1M = 0.075

OUTPUT_COST_PER_1M = 0.30

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
# SAMPLE TOKEN USAGE
# =====================================================

prompt_tokens_list = []

output_tokens_list = []

print("\nSampling token usage...\n")

for idx, query in enumerate(
    questions,
    start=1
):

    print("=" * 60)

    print(
        f"Question {idx}/{len(questions)}"
    )

    prompt = build_prompt(query)

    response = model.generate_content(
        prompt
    )

    usage = response.usage_metadata

    p_tok = usage.prompt_token_count

    o_tok = usage.candidates_token_count

    prompt_tokens_list.append(p_tok)

    output_tokens_list.append(o_tok)

    print(
        f"Prompt Tokens  : {p_tok}"
    )

    print(
        f"Output Tokens  : {o_tok}"
    )

# =====================================================
# COST CALCULATION
# =====================================================

avg_prompt = statistics.mean(
    prompt_tokens_list
)

avg_output = statistics.mean(
    output_tokens_list
)

input_cost_per_query = (
    avg_prompt / 1_000_000
) * INPUT_COST_PER_1M

output_cost_per_query = (
    avg_output / 1_000_000
) * OUTPUT_COST_PER_1M

total_cost_per_query = (
    input_cost_per_query +
    output_cost_per_query
)

cost_per_1000 = total_cost_per_query * 1000

# =====================================================
# SUMMARY
# =====================================================

print("\n" + "=" * 60)

print("COST PER 1000 QUERIES")

print("=" * 60)

print(
    f"Avg Prompt Tokens     : "
    f"{avg_prompt:.1f}"
)

print(
    f"Avg Output Tokens     : "
    f"{avg_output:.1f}"
)

print(
    f"Input Cost / Query    : "
    f"${input_cost_per_query:.6f}"
)

print(
    f"Output Cost / Query   : "
    f"${output_cost_per_query:.6f}"
)

print(
    f"Total Cost / Query    : "
    f"${total_cost_per_query:.6f}"
)

print(
    f"Cost / 1000 Queries   : "
    f"${cost_per_1000:.4f}"
)

print(
    f"(Model: {GEMINI_MODEL})"
)
