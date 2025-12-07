# Chatbot Testing

Testing and evaluation are critical for building reliable LLM applications. Unlike traditional software where correctness is binary, LLM outputs are non-deterministic and subjective. This guide provides systematic approaches to measuring and improving your chatbot's performance.

## Why Testing Matters

LLM applications are inherently non-deterministic. The same input can produce different outputs across runs. This makes traditional unit testing insufficient. You need strategies to:

1. **Quantify quality**: Measure objective aspects (speed, token usage, success rate)
2. **Assess subjective quality**: Evaluate tone, coherence, requirement adherence
3. **Track regressions**: Ensure changes don't break existing functionality
4. **Compare approaches**: Decide between implementation alternatives
5. **Optimize iteratively**: Systematically improve performance

## Quick Start

The fastest way to test your chatbot is using the console:

```powershell
# Start the exercise console
uv run exercise-1

# Run the test suite
>>> /test
```

This automatically loads and runs the test suite defined in `tests.py`.

## Core Concepts

### TestSuite Data Structures

The framework uses three typed data structures:

* **`TestCase`**: Defines a single test case with expected outcomes
* **`PassingCriteria`**: Defines criteria for determining overall pass/fail
* **`TestSuite`**: Combines test cases and passing criteria into a complete suite

#### TestCase Fields

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| `id` | Yes | str | Unique identifier for the test |
| `question` | Yes | str | The input query to send to the chatbot |
| `expected_keywords` | No | List[str] | Keywords that should appear in answer (case-insensitive) |
| `reset_chatbot` | No | bool | Whether to reset chatbot state before this test (default: True) |

#### PassingCriteria Fields

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| `min_success_rate` | No | float | Minimum fraction of tests that must succeed (default: 0.8) |
| `max_avg_time` | No | float | Maximum average execution time in seconds |

#### TestSuite Fields

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| `test_cases` | Yes | List[TestCase] | List of test cases to run |
| `passing_criteria` | Yes | PassingCriteria | Criteria for determining overall pass/fail |
| `repetitions` | No | int | Number of times to run each test case (default: 1) |

### Writing Custom Tests

Each exercise and solution has a `tests.py` file where tests are defined as follows:

```python
# Define test cases
TEST_CASES = [
    TestCase(
        id="simple_factual",
        question="What is the capital of France?",
        expected_keywords=["Paris"],
    ),
]

# Define passing criteria
PASSING_CRITERIA = PassingCriteria(
    min_success_rate=0.8,
)

# Create the test suite
TEST_SUITE = TestSuite(test_cases=TEST_CASES, passing_criteria=PASSING_CRITERIA, repetitions=1)
```

**Using repetitions**: When `repetitions > 1`, each test case runs multiple times. This is useful for:

* Testing consistency of non-deterministic LLM outputs
* Identifying flaky tests
* Measuring variance in execution time
* Validating that `temperature=0` truly produces deterministic results

**Testing multi-turn conversations**: by default, each test case starts with a fresh chatbot state (`reset_chatbot=True`). This flag should be set to `False` for multi-turn tests where the conversation history has to be persisted.

### Recommended Workflow

1. **Implement the chatbot functionality**
2. **Test manually** in console mode with a few queries
3. **Run automated tests** with `/test` command
4. **Review results** to identify which tests failed and why
5. **Extend tests** by adding edge cases to `tests.py`
6. **Optimize** based on test results
7. **Re-test** to confirm improvements
8. **Compare to solution** by running solution tests

## Troubleshooting

**Tests failing with connection errors**:

* Check that your LLM service is accessible
* Ensure connection parameters are configured correctly
* Verify that credentials are present

**Evaluation is too slow**:

* Use a smaller model for rapid iteration
* Reduce test case repetitions during development
* Run comprehensive tests after solution is mature

**Results are inconsistent across runs**:

* Set `temperature = 0` for deterministic outputs
* Use `seed` parameter for reproducibility
* Run tests multiple times and set a realistic success rate

## Further Reading

[How to Test GenAI Applications When There's No Correct Answer](https://medium.com/@brunelli.stefano.eu/how-to-test-genai-applications-when-theres-no-correct-answer-with-real-use-cases-26caf0ef9ac1) explores strategies for writing effective tests for non-deterministic LLM applications with real-world use cases.

[DeepEval](https://github.com/confident-ai/deepeval) is an evaluation framework for LLM applications that provides metrics for assessing response quality, factual accuracy, hallucination detection and RAG performance.

[OpenAI Evals](https://github.com/openai/evals) offers an open-source framework for evaluating LLMs with pre-built test suites, custom evaluation templates and community-contributed benchmarks.

[RAGAS](https://github.com/explodinggradients/ragas) provides specialized metrics for evaluating Retrieval Augmented Generation systems, including context precision, context recall, faithfulness and answer relevance.

[OpenLLMetry](https://github.com/traceloop/openllmetry) is an open-source observability SDK for LLM applications built on OpenTelemetry, enabling distributed tracing and performance monitoring in production.

[LangSmith](https://docs.smith.langchain.com/) is LangChain's commercial platform for evaluation, debugging and observability, offering features like prompt versioning, dataset management and collaborative testing workflows.

🏠 [Overview](/README.md) | ◀️ [Introduction](/src/chatbot/lessons/exercises/e00_intro/README.md)
---|---
