---
name: create-quiz-questions
description: Generates multiple choice quiz questions with explanations from educational content to test student comprehension. Use this when the user wants quiz questions, multiple choice tests, or assessment questions.
---

# Create Quiz Questions

## Purpose
Create effective multiple choice quiz questions that assess understanding of educational material, with clear options and detailed explanations to support learning.

## Instructions
1. Read and analyze the provided educational content
1. Identify testable concepts that are important for understanding the topic
1. For each concept, write a clear, unambiguous question
1. Create 4 plausible options (A-D) where:
   * One option is clearly correct
   * Other options (distractors) are plausible but incorrect
   * Distractors should reflect common misconceptions when possible
1. Identify the correct answer
1. Write an explanation that clarifies why the correct answer is right and why others are wrong
1. Generate 5 questions by default, unless the user specifies otherwise
1. Vary question types: definitions, applications, comparisons, scenarios

## Input
The user will provide:
* Educational content to create questions from
* Optionally, the number of questions to generate
* Optionally, specific topics or difficulty level

## Output Format
Create a markdown file with this structure:

```markdown
# Quiz for [Topic Name]

Generated from: [Brief description of source content]
Number of questions: [N]

---

## Question 1
[Question text that clearly states what is being asked]

A: [First option]
B: [Second option]
C: [Third option]
D: [Fourth option]

**Answer:** [Correct letter]
**Explanation:** [Why the correct answer is right, and optionally why common wrong answers are incorrect]

---

## Question 2
[Next question...]

A: [Option A]
B: [Option B]
C: [Option C]
D: [Option D]

**Answer:** [Correct letter]
**Explanation:** [Detailed explanation]

---

[Continue for remaining questions...]
```

## Quality Guidelines
* **Questions must be clear and unambiguous** - only one correct interpretation
* **All options should be grammatically parallel** - same structure and length when possible
* **Avoid "all of the above" or "none of the above"** - they're often crutches for weak questions
* **Distractors should be plausible** - based on common misconceptions or partial understanding
* **Explanations should teach** - reinforce the concept and clarify confusion
* **Vary difficulty** - include both recall and application questions
* **One concept per question** - don't test multiple ideas in a single question
* **Avoid negative phrasing** when possible (e.g., "Which is NOT...")

## Examples

### Example 1: Definition Question
**Question:** What is Retrieval Augmented Generation (RAG)?

A: A technique for generating random text using language models
B: A method that combines LLMs with external knowledge retrieval to improve accuracy
C: A way to fine-tune language models on domain-specific data
D: A prompt engineering technique for getting better outputs from LLMs

**Answer:** B
**Explanation:** RAG combines LLMs with external knowledge retrieval by finding relevant information from a knowledge base and including it in the prompt. This improves accuracy without requiring model fine-tuning. Option A is incorrect (RAG is not about random generation), Option C describes fine-tuning (a different approach), and Option D describes general prompt engineering (RAG is more specific).

### Example 2: Application Question
**Question:** When should you use the @tool decorator in LangChain?

A: When you want to change the LLM's temperature setting
B: When you want the LLM to be able to call a specific function
C: When you want to format the LLM's output as JSON
D: When you want to add system instructions to the LLM

**Answer:** B
**Explanation:** The @tool decorator is used to expose Python functions as tools that an LLM can call during its reasoning process. This is different from changing parameters (A), structured outputs (C), or system prompts (D), which serve other purposes in LangChain.

### Example 3: Comparison Question
**Question:** How does DeepAgents differ from a basic LangGraph agent?

A: DeepAgents uses a different LLM than LangGraph
B: DeepAgents adds planning, file operations, and skills to the base agent
C: DeepAgents is faster but less accurate than LangGraph agents
D: DeepAgents can only be used with local models

**Answer:** B
**Explanation:** DeepAgents extends basic LangGraph agents with built-in capabilities for planning (breaking tasks into steps), file system operations, and skill loading from SKILL.md files. Both use the same LLMs (A is incorrect), performance depends on use case not architecture (C is incorrect), and DeepAgents works with both local and remote models (D is incorrect).
