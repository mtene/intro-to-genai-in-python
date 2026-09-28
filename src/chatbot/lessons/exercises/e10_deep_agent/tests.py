# pyright: reportCallIssue=false
"""Evaluation smoke checks for this lesson."""

from deepeval.dataset import EvaluationDataset, Golden
from deepeval.metrics import PatternMatchMetric

EVAL_SUITES = {
    "emoji-decorator-skill": (
        EvaluationDataset(
            goldens=[
                Golden(
                    name="emoji-decorator-skill",
                    input="Add emojis to this text: I love Python programming and building AI agents",
                    additional_metadata={"reset_chatbot": True},
                )
            ]
        ),
        [PatternMatchMetric(pattern="(?s)(?=.*❤️)(?=.*🐍)(?=.*🤖).*", ignore_case=True)],
    ),
    "generate-flashcards-skill": (
        EvaluationDataset(
            goldens=[
                Golden(
                    name="generate-flashcards-skill",
                    input='Create 5 flashcards from this content:\n\n"Tool calling allows LLMs to invoke external functions. In LangChain, tools are defined\nusing the @tool decorator. The ReAct pattern enables agents to use tools in a loop until\nthe task is complete."\n\nInclude questions about tool definition, the @tool decorator, and the ReAct pattern.',
                    additional_metadata={"reset_chatbot": True},
                )
            ]
        ),
        [
            PatternMatchMetric(
                pattern="(?s)(?=.*Q:)(?=.*A:)(?=.*@tool)(?=.*ReAct).*", ignore_case=True
            )
        ],
    ),
    "create-quiz-questions-skill": (
        EvaluationDataset(
            goldens=[
                Golden(
                    name="create-quiz-questions-skill",
                    input='Create 3 quiz questions from this content:\n\n"RAG (Retrieval Augmented Generation) combines LLMs with external knowledge retrieval.\nIt involves chunking documents, creating embeddings, storing in a vector database,\nretrieving relevant chunks, and augmenting the LLM prompt."\n\nMake sure each question has 4 options (A-D) and an explanation.',
                    additional_metadata={"reset_chatbot": True},
                )
            ]
        ),
        [
            PatternMatchMetric(
                pattern="(?s)(?=.*A:)(?=.*B:)(?=.*C:)(?=.*D:)(?=.*Answer:)(?=.*Explanation:)(?=.*RAG).*",
                ignore_case=True,
            )
        ],
    ),
    "multiple-skills": (
        EvaluationDataset(
            goldens=[
                Golden(
                    name="multiple-skills",
                    input="Create a complete study guide about DeepAgents with:\n- 3 flashcards covering what DeepAgents is and how it differs from basic agents\n- 2 quiz questions testing understanding of skills and planning\n\nBoth flashcards and quiz should be included in your response.",
                    additional_metadata={"reset_chatbot": True},
                )
            ]
        ),
        [
            PatternMatchMetric(
                pattern="(?s)(?=.*flashcard)(?=.*quiz)(?=.*Q:)(?=.*A:)(?=.*Answer:)(?=.*DeepAgent).*",
                ignore_case=True,
            )
        ],
    ),
    "file-reading-with-skill": (
        EvaluationDataset(
            goldens=[
                Golden(
                    name="file-reading-with-skill",
                    input="Create 3 quiz questions for the README.md in exercise 9.",
                    additional_metadata={"reset_chatbot": True},
                )
            ]
        ),
        [
            PatternMatchMetric(
                pattern="(?s)(?=.*A\\.)(?=.*B\\.)(?=.*Correct\\ answer:)(?=.*skill).*",
                ignore_case=True,
            )
        ],
    ),
}

EVAL_REPETITIONS = 1
EVAL_MIN_PASS_RATE = 0.8
