---
name: generate-flashcards
description: Creates question-answer flashcard pairs from educational content to help students study and memorize concepts. Use this when the user wants flashcards, study cards, or Q&A pairs from learning materials.
---

# Generate Flashcards

## Purpose
Extract key concepts from educational material and transform them into effective question-answer flashcards that help students test their understanding and retention.

## Instructions
1. Carefully read and analyze the provided educational content
1. Identify the most important concepts, definitions, and relationships
1. For each concept, formulate a clear, focused question that tests understanding
1. Write concise but complete answers (2-4 sentences maximum)
1. Prioritize concepts that students commonly struggle with or that are fundamental to the topic
1. Create 10 flashcards by default, unless the user specifies a different number
1. Order flashcards from foundational concepts to more advanced topics

## Input
The user will provide:
* Educational content (text, documentation, lesson materials, etc.)
* Optionally, the number of flashcards to generate
* Optionally, specific topics to focus on

## Output Format
Create a markdown file with this structure:

```markdown
# Flashcards for [Topic Name]

Generated from: [Brief description of source content]

---

## Card 1
Q: What is [concept]?
A: [Clear, concise definition or explanation]

## Card 2
Q: How does [concept] work?
A: [Process explanation with key steps]

## Card 3
Q: What is the difference between [concept A] and [concept B]?
A: [Comparison highlighting key distinctions]

## Card 4
Q: When should you use [technique/tool]?
A: [Use cases and scenarios]

## Card 5
Q: What are the key components of [system]?
A: [Enumeration with brief explanations]

[Continue for remaining cards...]
```

## Quality Guidelines
* **Questions should be specific and unambiguous** - avoid vague wording
* **Answers should be self-contained** - don't reference "the above" or assume prior context
* **Mix question types**: definitions, how-it-works, comparisons, use cases, examples
* **Use active voice** and clear language
* **Include concrete examples** in answers when helpful
* **Avoid yes/no questions** - prefer questions that require explanation
* **Test understanding, not memorization** - focus on "why" and "how" over "what"

## Examples

### Example 1: Technical Concept
Q: What is the purpose of the @tool decorator in LangChain?
A: The @tool decorator converts a Python function into a tool that can be called by an LLM. It automatically generates a JSON schema from the function's type annotations and docstring, making the function's signature and purpose understandable to language models.

### Example 2: Comparison
Q: What is the difference between LangChain and LangGraph?
A: LangChain provides building blocks for LLM applications (prompts, chains, tools), while LangGraph extends LangChain with stateful, graph-based workflows. LangGraph is specifically designed for building agents that need persistence, cycles, and complex control flow.

### Example 3: Process
Q: How does the ReAct agent pattern work?
A: The ReAct (Reasoning-Acting) pattern runs in a loop: the LLM receives a question, decides whether to call tools or provide a final answer, executes any requested tools, receives results, and repeats until no more tools are needed. This enables multi-step problem solving.
