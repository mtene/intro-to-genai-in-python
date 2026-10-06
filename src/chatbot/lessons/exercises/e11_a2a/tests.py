# pyright: reportCallIssue=false
"""Evaluation smoke checks for this lesson."""

from deepeval.dataset import EvaluationDataset, Golden
from deepeval.metrics import PatternMatchMetric

_REFUSAL = (
    r"(?:not implemented|can't help|cannot provide|currently cannot|"
    r"can't retrieve|don't have the ability|I currently don't)"
)

EVAL_SUITES = {
    "budget_expert_routing": (
        EvaluationDataset(
            goldens=[
                Golden(
                    name="budget_expert_routing",
                    input="What's a realistic daily budget for visiting Rome?",
                    additional_metadata={"reset_chatbot": True},
                )
            ]
        ),
        [
            PatternMatchMetric(
                pattern=(
                    rf"(?s)(?!.*{_REFUSAL})(?=.*Rome)(?=.*\$\d+)"
                    r"(?=.*(?:accommodation|food|transport|activities|per day))"
                ),
                ignore_case=True,
            )
        ],
    ),
    "destination_expert_routing": (
        EvaluationDataset(
            goldens=[
                Golden(
                    name="destination_expert_routing",
                    input="Recommend destinations for someone who loves beaches and diving",
                    additional_metadata={"reset_chatbot": True},
                )
            ]
        ),
        [
            PatternMatchMetric(
                pattern=(
                    rf"(?s)(?!.*{_REFUSAL})(?=.*\b(?:Bali|Thailand|Maldives|Philippines|"
                    r"Indonesia|Fiji|Hawaii|Belize|Egypt|Komodo|Sipadan|Caribbean|"
                    r"Red Sea|Great Barrier Reef|Cancún|Cancun)\b)"
                ),
                ignore_case=True,
            )
        ],
    ),
    "multi_expert_coordination": (
        EvaluationDataset(
            goldens=[
                Golden(
                    name="multi_expert_coordination",
                    input="I have $150 per day to spend in Asia. Where should I go?",
                    additional_metadata={"reset_chatbot": True},
                )
            ]
        ),
        [
            PatternMatchMetric(
                pattern=(
                    rf"(?s)(?!.*{_REFUSAL})(?=.*\b150\b)(?=.*\$\d+)"
                    r"(?=.*\b(?:Thailand|Vietnam|Bali|Philippines|Japan|Taiwan|India|"
                    r"Malaysia|Nepal|Sri Lanka|Cambodia|Laos|Korea|Singapore|"
                    r"Hong Kong|Indonesia)\b)"
                ),
                ignore_case=True,
            )
        ],
    ),
}

EVAL_REPETITIONS = 1
EVAL_MIN_PASS_RATE = 0.8
