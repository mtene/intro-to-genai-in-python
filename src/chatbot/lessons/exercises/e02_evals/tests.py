# pyright: reportCallIssue=false
"""Build evaluation suites for the completed prompting chatbot."""

from deepeval.dataset import EvaluationDataset, Golden
from deepeval.metrics import ExactMatchMetric, PatternMatchMetric


# Add one named suite for each evaluation mode described in the README.
EVAL_SUITES = {
    "exact output": (
        EvaluationDataset(
            goldens=[
                Golden(
                    input="Reply with only the capital of France.",
                    expected_output="Paris",
                )
            ]
        ),
        [ExactMatchMetric()],
    ),
    "output pattern": (
        EvaluationDataset(
            goldens=[
                Golden(
                    input="Write 'Merry Christmas' in German and output only the translation."
                )
            ]
        ),
        [PatternMatchMetric(pattern=r"(?i).+weihnachten[.!]?")],
    ),
    # Add a semantic-quality suite with AnswerRelevancyMetric and GEval.
}

EVAL_REPETITIONS = 1
EVAL_MIN_PASS_RATE = 0.8
