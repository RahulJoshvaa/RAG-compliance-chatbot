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


    # FATF

    "What is the purpose of the FATF Recommendations?",
    "What is the risk-based approach under FATF Recommendation 1?",
    "What is Customer Due Diligence according to FATF?",
    "When do the EBA Guidelines on the application of the definition of default become applicable?",
    "What is considered a technical past due situation under the EBA default guidelines?",
    "How should institutions treat payment schedules that are changed under contractual rights granted to the obligor?",

    # FCA
    "What are the four outcomes that make up the Consumer Duty framework?",
    "What does the FCA expect firms to do regarding customer outcomes under the Consumer Duty?",
    "Does the Consumer Duty apply only to existing customers?",

    # DORA
    "What is the main objective of DORA?",
    "Why was DORA introduced for the financial sector?",
    "What areas of ICT risk management are harmonised under DORA?"
]

ground_truth = [

    "The regulation was introduced to implement the remaining Basel III reforms and improve banking resilience.",

    "The output floor limits excessive reductions in capital requirements produced by internal models.",

    "The output floor is set at 72.5 percent of standardized capital requirements.",

    "The FATF Recommendations provide an international framework for combating money laundering and terrorist financing.",

    "The risk-based approach requires institutions to identify, assess and mitigate risks proportional to their severity.",

    "Customer Due Diligence requires identifying and verifying customers and understanding risk.",
     "The guidelines apply from 1 January 2021. Institutions should incorporate the requirements into their internal procedures and IT systems by that date.",

    "A technical past due situation may occur when the default status results from a data or system error, a payment transaction was not executed or was executed late, or a payment failed because of a payment system failure.",

    "If the contract allows the obligor to change, suspend, or postpone payments and the obligor acts within those rights, the affected instalments are not considered past due and days past due should be counted according to the new schedule.",

    # FCA
    "The four outcomes are Products and Services, Price and Value, Consumer Understanding, and Consumer Support.",

    "Firms should monitor and regularly review customer outcomes in practice and take action to address risks to good customer outcomes.",

    "No. The Consumer Duty applies to both prospective and actual retail customers, including communications, enquiries, and applications from potential customers.",

    # DORA
    "DORA establishes a framework to strengthen the digital operational resilience of financial entities through ICT risk management, incident reporting, resilience testing, and third-party risk management.",

    "DORA was introduced because increasing digitalisation and interconnected ICT systems have increased exposure to cyber threats and ICT disruptions, creating risks to financial stability.",

    "DORA harmonises ICT risk management, ICT-related incident reporting, digital operational resilience testing, and ICT third-party risk monitoring."



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