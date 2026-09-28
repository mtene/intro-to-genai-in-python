# Solution: Custom agent

One possible [solution](chatbot.py) to the [`author`](author.py)-[`reviewer`](reviewer.py) task wires them in a loop, as shown in the diagram.

![Graph for author-reviewer agent](/images/author_reviewer_graph.png)

## Implementation: LangGraph design

The initial state contains:

* an empty `text`
* `feedback` hand-populated to "create the first draft"
* loop `iteration` set to 1
* the questions and answers exchanged so far in `messages`, where the latest question is last (in case the query references an earlier message)

The author is instructed to amend the `text` based on the `feedback`.

The reviewer is asked to produce the following structured output

* a boolean verdict, `text_meets_or_exceeds_requirements`
* textual `feedback` for the author

These two nodes are called in a loop with up to 3 iterations, which can end early if the reviewer assesses that the text fulfills all requirements (captured in the state by `feedback` being blank). As extra protection, another iteration is also issued if the `text` is blank, e.g. due to author hallucination or error occurrence.

## Further improvement

**Major weakness**: the [`author`](author.py) can directly overwrite the state's text. Any hallucinations cause regressions - there's no guarantee quality improves monotonically with each iteration.

**More robust approach**: extend the state with `revised_text`. Before replacing `text`, verify that `revised_text` represents an improvement.

**Implementation options** include:

1. **3-value reviewer verdict**: change the [`reviewer`](reviewer.py) verdict to a 3-value enum (ACCEPT, REVISE, REJECT)
1. **Dedicated revision approver**: add a `revision_approver` node, which loops back to the author on regression

The second approach is more robust, since regression requires both `author` and `revision_approver` to hallucinate. It also keeps the reviewer simpler, avoiding the subtle distinction between REVISE and REJECT that challenges small language models.

![More robust graph for author-reviewer agent](/images/author_reviewer_graph_v2.png)

The implementation and further exploration is left as an exercise for the reader.

## Testing and evaluation

Send queries for short post-its, telegrams, letters or postcards and observe the interaction. With small language models, the reviewer may accept the text on the first turn or keep requesting revisions, sometimes inventing additional criteria despite the system prompt rules.

Evaluate observable graph behavior deterministically when possible, and use narrow rubrics for subjective final drafts. Account for the extra latency and cost of author-reviewer loops.

---

🏠 [Overview](/README.md) | ◀️ [Back to exercise](/src/chatbot/lessons/exercises/e09_custom_agent/README.md) | ▶️ [Next exercise](/src/chatbot/lessons/exercises/e10_deep_agent/README.md)
---|---|---
