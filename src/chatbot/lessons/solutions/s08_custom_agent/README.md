# Solution 8: Custom agent

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

## Verification

Send queries for short post-its, telegrams, letters or postcards and observe the interaction. With small LLMs, the behavior of the reviewer usually falls into two categories: it either accepts the text in the first turn or keeps asking for revisions, often making up additional criteria, despite the rules set out in the system prompt. This is due to the limited reasoning capabilities of small models, making them prone to ignore instructions or hallucinate.

## Further improvement

The chosen solution has one major weakness - the [`author`](author.py) is given the ability to directly overwrite the text in the state. Any hallucinations will cause regressions, therefore there is no guarantee that the level of quality increases monotonically with each iteration.

In a more robust system, the state is extended with a `revised_text`. Then a decision needs to be made if it is an improvement over `text`, in which case `revised_text` becomes its replacement.

This decision can be taken by the [`reviewer`](reviewer.py) by changing the type of their verdict into a 3-value enum: ACCEPT, REVISE, REJECT. Alternatively, a new `revision_approver` node can be introduced to make this binary decision and loop back to the author on regression. This is more robust, since a regression can now happen only if both `author` and `revision_approver` hallucinate. It also avoids making the reviewer more complex, as the distinction between REVISE and REJECT may be too subtle for small language models.

![More robust graph for author-reviewer agent](/images/author_reviewer_graph_v2.png)

The implementation and further exploration is left as an exercise for the reader.

🏠 [Overview](/README.md) | ◀️ [Back to exercise](/src/chatbot/lessons/exercises/e08_custom_agent/README.md)
---|---
