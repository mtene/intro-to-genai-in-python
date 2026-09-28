# Exercise: Testing and evaluation

⏱️ **Estimated time**: 20-25 minutes

## Learning objectives

By the end of this exercise, you should be able to:

* Define reference datasets
* Select exact, pattern, or LLM-as-judge evaluation based on the expected output
* Run all evaluation suites with the existing `/test` command
* Interpret scores, thresholds, reasons, and trade-offs

## Overview

You previously learned how to prompt an LLM. Now you will measure that chatbot's behavior.

This course uses [DeepEval](https://deepeval.com/) to define and run evaluations. Define your evaluations in [tests.py](tests.py): refine prompts, expected outputs, patterns, criteria, and thresholds. Enter `/test` in the console to execute the tests and review their results.

```powershell
uv run exercise-2

>>> /test
```

## Why evaluate?

Testing makes expected behavior explicit, detects deviations from it, and helps compare implementation alternatives. Traditional software tests can often assert one expected output for a given input. LLM applications pose a different challenge: outputs can vary between runs, and many answers may be acceptable. Under these conditions, evaluations allow us to define clear expectations, measure behavior repeatedly, identify weak cases, and decide whether a change to the prompt, model, or implementation is an improvement.

## Evaluation approaches

Evaluation approaches differ in how much variation they accept. The following approaches progress from strict, deterministic checks to more flexible semantic judgments:

1. **Exact matching** applies when there is exactly one valid response. For the question "What is the capital of France?", a test expecting "Paris is the capital of France" accepts that response. However, it rejects the equally correct "The capital of France is Paris," making it too strict for many natural-language answers. In DeepEval, this type of check is performed using `ExactMatchMetric`.
2. **Keyword matching** checks whether expected words or phrases appear in the response. It is fast and transparent: checking for `programming` accepts the correct answer "Python is a programming language." However, it also accepts the incorrect "Python is not a programming language," while rejecting the correct "Python is a general-purpose language used to build software." DeepEval's `PatternMatchMetric` can perform this check with a simple pattern.
3. **Pattern matching** applies when the output needs a known shape. For example, a pattern can verify that `2026-09-28` uses the expected date format. However, a loose pattern may also accept `2026-99-99` even though it is not a real date. DeepEval provides `PatternMatchMetric` for this type of evaluation.
4. **LLM as judge** handles open prose with multiple valid answers. It can recognize both "Python is a programming language" and "Python is a language used to build software" as relevant explanations. The score depends on clearly defined evaluation criteria; vague criteria can be interpreted differently. Because the judge is also an LLM, scores may vary between models or runs, and every judgment adds latency and cost. DeepEval offers `AnswerRelevancyMetric` for judging relevance and `GEval` for defining custom criteria.

More expressive does not always mean better. Prefer exact or pattern matching whenever the expected response can be described reliably in those terms.

## Exercise

The provided [tests.py](tests.py) starts with two deterministic evaluation suites: one checks an exact answer and the other checks an output pattern.

* Review the exact-match test for the French-capital response.
* Refine the German-translation pattern so it accepts the desired format without accepting unrelated text.

Then add the `semantic quality` suite:

1. Add a [reference example (`Golden`)](https://deepeval.com/docs/evaluation-datasets) for the one-sentence Python explanation.
2. Add [`AnswerRelevancyMetric`](https://deepeval.com/docs/metrics-answer-relevancy) with the supplied evaluation model. It judges whether the answer addresses the prompt without requiring an expected answer.
3. Add [`GEval`](https://deepeval.com/docs/metrics-llm-evals) with [`SingleTurnParams.INPUT`, `SingleTurnParams.ACTUAL_OUTPUT`, and `SingleTurnParams.EXPECTED_OUTPUT`](https://deepeval.com/docs/evaluation-test-cases). Define a focused rubric for correctness, directness, and sentence count.
4. Set a reasonable threshold and run `/test`.

The console reports each metric's score, threshold, result, reason, and latency. Refine the criteria and rerun the tests to see how the results change.

## Compare the judge metrics

`AnswerRelevancyMetric` is reference-free: it detects irrelevant answers but does not establish factual correctness. `GEval` uses a rubric and can compare an answer with an expected output. Both use the configured LLM as the judge.

After adding both metrics, run `/test` and compare their scores and reasons for the same answer. Check whether the answer can be relevant without fully satisfying the correctness rubric, then refine the `GEval` criteria or threshold and run the test again. A useful rubric focuses on the qualities that matter for that test instead of trying to assess everything at once.

## Test a poor implementation

You designed the evaluations using the completed prompting chatbot. As a final check, change the import in [chatbot.py](chatbot.py) from `solutions.s01_prompting` to `exercises.e01_prompting`, then run `/test` again. This switches to the dummy chatbot, which always answers `???`. Compare the results: useful evaluations should distinguish clearly between the completed chatbot and this known poor implementation.

## Further reading

Judge calibration against human examples, using a different judge model, repeated judging, bias, and cost optimization matter in production but are outside this introductory exercise. The [DeepEval documentation](https://deepeval.com/docs/) covers those topics, along with metrics for conversations, retrieval, tools, and safety.

---

🏠 [Overview](/README.md) | ◀️ [Previous exercise](/src/chatbot/lessons/exercises/e01_prompting/README.md) | ✅ [Solution](/src/chatbot/lessons/solutions/s02_evals/README.md) | ▶️ [Next exercise](/src/chatbot/lessons/exercises/e03_system_prompt/README.md)
---|---|---|---
