# Solution: Testing and evaluation

This solution evaluates the completed prompting chatbot without changing its application code:

```powershell
uv run solution-2

>>> /test
```

## Three evaluation modes

[tests.py](tests.py) groups tests by the type of output being evaluated:

* **Exact output** uses `ExactMatchMetric` when only one literal answer is valid.
* **Output pattern** uses `PatternMatchMetric` when the response must follow a particular format.
* **Semantic quality** uses two LLM judges for an open-ended explanation: `AnswerRelevancyMetric` checks whether the response addresses the prompt, while `GEval` assesses it against the expected answer and rubric.

The console asks each question and reports the resulting score, threshold, pass/fail outcome, reason, and latency.

## Why not use one metric everywhere?

Exact and pattern matching are fast and deterministic, so prefer them whenever the expected response can be described reliably in those terms. Natural-language answers often allow many correct phrasings; an LLM judge is better suited to those cases, but its rubric and threshold need careful definition.

---

🏠 [Overview](/README.md) | ◀️ [Back to exercise](/src/chatbot/lessons/exercises/e02_evals/README.md) | ▶️ [Next exercise](/src/chatbot/lessons/exercises/e03_system_prompt/README.md)
---|---|---
