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
# MEASURE TOKENS PER QUERY
# =====================================================

prompt_tokens_list = []

output_tokens_list = []

total_tokens_list = []

for idx, query in enumerate(
    questions,
    start=1
):

    print("=" * 60)

    print(
        f"Question {idx}/{len(questions)}"
    )

    print(query[:80] + "...")

    prompt = build_prompt(query)

    response = model.generate_content(
        prompt
    )

    usage = response.usage_metadata

    p_tok = usage.prompt_token_count

    o_tok = usage.candidates_token_count

    t_tok = usage.total_token_count

    prompt_tokens_list.append(p_tok)

    output_tokens_list.append(o_tok)

    total_tokens_list.append(t_tok)

    print(
        f"Prompt Tokens  : {p_tok}"
    )

    print(
        f"Output Tokens  : {o_tok}"
    )

    print(
        f"Total Tokens   : {t_tok}"
    )

# =====================================================
# SUMMARY
# =====================================================

avg_prompt = statistics.mean(
    prompt_tokens_list
)

avg_output = statistics.mean(
    output_tokens_list
)

avg_total = statistics.mean(
    total_tokens_list
)

print("\n" + "=" * 60)

print("TOKENS PER QUERY")

print("=" * 60)

print(
    f"Avg Prompt Tokens  : "
    f"{avg_prompt:.1f}"
)

print(
    f"Avg Output Tokens  : "
    f"{avg_output:.1f}"
)

print(
    f"Avg Total Tokens   : "
    f"{avg_total:.1f}"
)
