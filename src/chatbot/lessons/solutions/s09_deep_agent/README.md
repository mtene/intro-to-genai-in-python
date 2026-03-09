# Solution: DeepAgents CLI

This solution demonstrates how to build a DeepAgents-powered chatbot with custom skills for creating study materials.

## Implementation Overview

### ChatBot Class (chatbot.py)

The [implementation](chatbot.py) follows the standard `BaseChatBot` interface but uses `create_deep_agent()` instead of manually building a LangGraph:

```python
# Convert skills path to POSIX format (DeepAgents limitation on Windows)
skills_path = f"/{(Path(__file__).parent / 'skills').relative_to(root_path).as_posix()}/"

# Create the DeepAgent with skills parameter
self._agent = create_deep_agent(
    model=llm,
    skills=[skills_path],
    backend=LocalShellBackend(root_dir=root_path, virtual_mode=True),
    ...
)
```

**Skills loading is progressive:**

The `skills=` parameter requires POSIX-style paths (forward slashes), even on Windows. We use `Path.as_posix()` to convert Windows paths automatically.

DeepAgents uses a three-stage loading pattern:

1. **At startup:** Only skill front-matter (name + description) loads into system prompt (~100 words each)
2. **On activation:** Full SKILL.md body loads when the agent decides to use that skill
3. **On demand:** Files mentioned in SKILL.md load only when needed

This enables 30+ skills while consuming just ~3,000 tokens at rest.

**Filesystem security:**

The file system backend uses `virtual_mode=True` which:
- Restricts all file access to the lessons directory (root_dir)
- Uses virtual paths starting with `/` (e.g., `/solutions/s09_deep_agent/README.md`)
- Prevents access to files outside the root directory for security
- Allows the agent to access both `/exercises/` and `/solutions/` subdirectories

### Skills Implementation

Two complete skills are provided:

#### generate-flashcards

Creates Q&A flashcards optimized for studying:

* Extracts key concepts from content
* Formats as Q&A pairs
* Provides guidelines for effective questions (specific, unambiguous)
* Includes examples showing different question types

**Design choices:**

* Default to 10 cards (balanced between comprehensive and manageable)
* Mix question types (definitions, comparisons, processes)
* Focus on understanding over memorization

#### create-quiz-questions

Generates multiple choice assessments:

* Creates 4-option questions with one correct answer
* Includes detailed explanations
* Uses plausible distractors based on common misconceptions
* Defaults to 5 questions

**Design choices:**

* Avoid "all/none of the above" (often indicates weak questions)
* Parallel grammatical structure for all options
* Explanations clarify both correct and incorrect answers

### Skill Description Best Practices

Notice how the `description` field in the YAML front-matter is crafted:

```yaml
description: Creates question-answer flashcard pairs from educational content to help students study and memorize concepts. Use this when the user wants flashcards, study cards, or Q&A pairs from learning materials.
```

Effective descriptions:

* **State the purpose clearly** - what does this skill do?
* **Include trigger keywords** - "flashcards", "study cards", "Q&A pairs"
* **Specify use cases** - when should the agent use this?
* **Be specific but concise** - under 1024 characters

The agent uses ONLY the description to decide skill relevance, so this is critical!

## How DeepAgents Planning Works

When you give the agent a complex request like:

```plaintext
>>> Create a complete study guide for RAG with both flashcards and quiz questions
```

The agent:

1. **Analyzes** the request and identifies multiple sub-tasks
1. **Plans** a sequence of steps (read content → generate flashcards → generate quiz)
1. **Executes** each step, using the appropriate skill
1. **Tracks progress** and adjusts the plan if needed
1. **Returns** a final answer summarizing what was created

You'll see this in the console:

```plaintext
🧠 Thinking...
🔨 Calling generate_flashcards(content="...", num_cards=10)
📦 generate_flashcards returned: [flashcards created]
🔨 Calling extract_quiz_questions(content="...", num_questions=5)
📦 extract_quiz_questions returned: [quiz created]
```

## Comparison with Custom Agent

| Aspect | Custom Agent | DeepAgent |
| --- | --- | --- |
| Workflow | Fixed: author → reviewer → iterate | Dynamic: plan based on request |
| Capabilities | Only LLM generation | LLM + planning + file ops + skills |
| Tools | Python `@tool` functions | SKILL.md files |
| State Management | Manual (`GraphState`) | Built-in |
| Complexity | You design the graph | Framework handles it |
| Best for | Specific, predictable flows | Open-ended, complex tasks |

## Running the Solution

Try these example prompts:

```plaintext
>>> Create flashcards about the MCP protocol
```

```plaintext
>>> Generate a quiz to test my understanding of tool calling
```

```plaintext
>>> Create a complete study guide for custom LangGraph agents with both flashcards and quiz questions. Save it to study_guides/langgraph_agents
```

```plaintext
>>> Add some emojis to this: DeepAgents makes building AI agents much easier!
```

The last one demonstrates the emoji-decorator example skill.

## Key Takeaways

1. **SKILL.md format** is simple but powerful - no code needed for basic capabilities
1. **Description field** is critical - the agent's only way to know when to use a skill
1. **DeepAgents planning** enables complex multi-step tasks without manual graph design
1. **Skills are composable** - the agent can combine multiple skills intelligently

## Testing

Run `/test` in the console to verify:

* ✅ Emoji decorator example skill works
* ✅ Flashcard generation works
* ✅ Quiz question generation works
* ✅ Agent can plan and use multiple skills together

All tests should pass with this solution.

---

| 🏠 [Overview](/README.md) | ◀️ [Back to exercise](/src/chatbot/lessons/exercises/e09_deep_agent/README.md) | ▶️ [Next exercise](/src/chatbot/lessons/exercises/e10_observability/README.md) |
| --- | --- | --- |
