# pyright: reportCallIssue=false
"""Evaluation suites for the prompting chatbot from the previous lesson."""

from deepeval.dataset import EvaluationDataset, Golden
from deepeval.metrics import (
    AnswerRelevancyMetric,
    ExactMatchMetric,
    GEval,
    PatternMatchMetric,
)
from deepeval.test_case import SingleTurnParams

from chatbot.testing.models import EvaluationModel

EVALUATION_MODEL = EvaluationModel()

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
    "semantic quality": (
        EvaluationDataset(
            goldens=[
                Golden(
                    input="Explain what Python is in one sentence.",
                    expected_output="Python is a programming language.",
                )
            ]
        ),
        [
            AnswerRelevancyMetric(model=EVALUATION_MODEL, threshold=0.5),
            GEval(
                name="Correctness",
                criteria=(
                    "The answer correctly identifies Python as a programming language. "
                    "Wording may differ from the expected output."
                ),
                evaluation_params=[
                    SingleTurnParams.INPUT,
                    SingleTurnParams.ACTUAL_OUTPUT,
                    SingleTurnParams.EXPECTED_OUTPUT,
                ],
                model=EVALUATION_MODEL,
                threshold=0.7,
            ),
        ],
    ),
}

EVAL_REPETITIONS = 1
EVAL_MIN_PASS_RATE = 0.8
