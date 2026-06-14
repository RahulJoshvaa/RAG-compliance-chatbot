
def retrieve(query: str):

    print(f"\nRetrieving chunks for: {query}")

    chunks = [
        {
            "text": """
Employees are entitled to carry forward any unused leave balance from the current leave year to the subsequent leave year, subject to a maximum limit of 10 leave days. This provision is intended to provide employees with flexibility in managing their leave while ensuring that leave is utilized regularly for rest, personal commitments, and overall well-being. Any accumulated leave exceeding the permitted carry-forward limit of 10 days at the end of the leave cycle will not be transferred to the next year and may lapse in accordance with the organization's leave management policies. Employees are therefore advised to monitor their leave balances periodically and plan their leave schedules effectively to make optimal use of their entitled leave benefits. The organization reserves the right to review, modify, or enforce carry-forward rules as necessary to align with business requirements, workforce planning considerations, and applicable company policies.

""",
            "section": "5.2",
            "title": "Carry Forward",
            "score": 0.95
        },

        {
            "text": """
Carry-forward requests require approval
from the reporting manager.
""",
            "section": "5.3",
            "title": "Approval Process",
            "score": 0.91
        }
    ]

    return chunks