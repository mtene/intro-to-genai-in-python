# Exercise: DeepAgents CLI

⏱️ **Estimated time**: 45 minutes

## Learning Objectives

By the end of this exercise, you should be able to:

* Understand how LangChain DeepAgents compare to the other agents encountered in this course
* Define skills following the [agentskills.io](https://agentskills.io) specification
* Build agents with shell access, custom skills, todo list planning and task delegation capabilities
* Observe how the agent handles multi-step workflows

## Model Requirements

**DeepAgents requires capable models** for planning and routing:

* **< 8B parameters:** Will fail - models hallucinate instead of following the framework
* **8-20B parameters:** May understand but struggle to execute (describe actions instead of performing them)
* **20-70B parameters:** Works on simple tasks, may struggle with complex multi-skill planning
* **> 70B parameters:** Recommended - high success rate (e.g., Llama 3.3:70B, GPT-4, Claude 3.5+)

From testing, GPT-OSS 20B is the smallest local LLM that works with DeepAgents. For best results, switch to a remote LLM in `src/config.yaml`:

```yaml
llm_config:
  <<: *remote_llm_settings  # Change from local_llm_settings
```

Ensure your remote endpoint is configured and credentials are set as environment variables.

## Overview

In this exercise, you will create a **Study Guide Generator Agent** that helps students learn by creating flashcards and quiz questions from educational content.

Unlike previously, where you defined tools as Python functions, DeepAgents uses **skills** defined in natural language. Skills are typically defined in markdown files that are:

* Easy to share and version control
* Understandable by both humans and agents
* Independent of implementation language

**Skills over tools:**

Traditional tools (Python `@tool` or MCP) send full definitions with every API call (10 tools × ~1000 tokens = 10,000 tokens per call). Skills use progressive disclosure: only the skill name and description (~100 words each) from the front-matter stay in the system prompt permanently. The full skill instructions are loaded into context only when that specific skill is activated. This enables agents to work with 30+ skills while consuming just ~3,000 tokens at rest.

Run the [tests](tests.py) in the console to track progress.

## Motivation

### The Rise of CLI Agents

AI is transforming command-line interfaces from simple command executors into intelligent assistants. Modern terminal-based agents can understand intent, plan autonomously, access codebase context, and execute multi-step operations safely:

* **[Aider](https://aider.chat/)** - Pioneer of terminal AI pair programming
* **[Claude Code](https://claude.ai/code)** - Terminal agent with deep reasoning and session memory
* **[OpenCode](https://opencode.ai/)** - Open-source CLI supporting 75+ LLM providers

In contrast, **IDE-based agents** like [Cursor](https://cursor.com/) and [Windsurf](https://windsurf.com/) provide visual coding assistance with inline edits, while CLI agents excel at automation, git workflows, and composing with Unix tools.

This shift - from "tell me the command" to "do it for me intelligently" - represents the future of developer tools.

### From Custom Graphs to DeepAgents

Previously, you built a custom agent with an author-reviewer loop. While powerful, that agent had limitations:

* Fixed structure (always author → reviewer)
* No file system access
* No automatic planning for complex tasks
* Embedded in application code

[LangChain DeepAgents](https://docs.langchain.com/oss/python/deepagents/overview) extends the custom agent pattern with:

* **Planning**: Agents break down complex tasks into steps
* **File operations**: Agents can read, write, and organize files
* **Skills**: Modular capabilities defined in markdown
* **Persistence**: Built on LangGraph's state management
* **CLI-first design**: Meant to be run from the terminal

## What You'll Build

A study guide generator with two skills:

1. **generate-flashcards** - Creates Q&A flashcards from educational material
1. **create-quiz-questions** - Generates multiple choice quiz questions

## SKILL.md File Format

Skills are defined using the [agentskills.io](https://agentskills.io) specification. Each skill is a directory containing a `SKILL.md` file with:

### Structure

```markdown
---
name: skill-name
description: Clear description of when the agent should use this skill
---

# Human-Readable Skill Title

## Purpose
What this skill accomplishes

## Instructions
1. Step-by-step guide for the agent
1. Be specific about inputs and outputs
1. Include any important details

## Output Format
Show examples of the expected output

## Quality Guidelines
* Tips for producing good results
* Best practices
```

### Example: emoji-decorator

An example skill [`emoji-decorator`](skills/emoji-decorator/SKILL.md) is provided.

**Try it out:**

```plaintext
>>> Add some emojis to this text: I love learning about DeepAgents!
```

The agent will use the emoji-decorator skill to enhance your text. Study this skill's SKILL.md file to understand the format before creating your own!

## Your Tasks

### Task 1: Inspect the Chatbot (chatbot.py)

Study the [chatbot logic](chatbot.py), noting how DeepAgents are created and used:

* Skill front-matter is loaded using the `skills=` parameter with a POSIX-style path
* `Path.as_posix()` converts Windows paths to forward slashes (required by DeepAgents)
* `LocalShellBackend` with `virtual_mode=True` restricts file access to the lessons directory for security
* The agent is created with `create_deep_agent()` which includes built-in planning and file operations

### Task 2: Create the generate-flashcards Skill

In `skills/generate-flashcards/SKILL.md`, create a skill that:

* Extracts key concepts from educational content
* Creates question-answer pairs
* Formats them as markdown flashcards
* Generates 10 flashcards by default

**Output format suggestion:**

```markdown
# Flashcards for [Topic]

## Card 1
Q: [Question about a concept]
A: [Clear, concise answer]

## Card 2
Q: [Another question]
A: [Another answer]
```

### Task 3: Create the create-quiz-questions Skill

In `skills/create-quiz-questions/SKILL.md`, create a skill that:

* Analyzes educational content
* Generates multiple choice questions
* Provides 4 options (A-D) per question
* Includes the correct answer and explanation
* Creates 5 questions by default

**Output format suggestion:**

```markdown
# Quiz for [Topic]

## Question 1
[Question text]

A: [Option A]
B: [Option B]
C: [Option C]
D: [Option D]

**Answer:** [Correct option]
**Explanation:** [Why this is correct]
```

## Testing Your Implementation

Run `/test` in the console to check your implementation.

### Expected Test Results

As you work through the exercise, you'll see tests pass progressively:

| Test | When It Passes |
| ---- | -------------- |
| emoji-decorator | ✅ Immediately (example skill provided) |
| Generate flashcards | After defining generate-flashcards/SKILL.md |
| Generate quiz questions | After defining create-quiz-questions/SKILL.md |
| Use multiple skills | After both skills are complete |
| Generate specific number | After flashcards skill is robust |

**Initial state:** Only test 1 should pass (the emoji-decorator example).

**Goal:** All 5 tests passing means your implementation is complete!

### Debugging Failed Tests

If a test fails, the agent might:

* Not recognize when to use your skill → Check the `description` field
* Use the skill but produce wrong output → Review the `Instructions` section
* Skip the skill entirely → Make sure the SKILL.md file exists and is properly formatted

## Try These Prompts

After implementing, try:

```plaintext
>>> Create flashcards from this content: "LangGraph is a library for building stateful, multi-actor applications with LLMs. It extends LangChain with graphs and persistence."
```

```plaintext
>>> Generate a quiz about LLM tool calling
```

```plaintext
>>> Create a complete study guide for RAG with both flashcards and quiz questions
```

Watch the agent plan and execute! You'll see:

```bash
🧠 Thinking...
📝 Planning: Breaking task into steps
🔨 Calling generate_flashcards(content="...")
📦 generate_flashcards returned: [flashcards]
```

## Understanding DeepAgents vs Custom Agents

| Aspect | LangGraph Custom Agent | DeepAgent |
| ------ | ----------------------- | -------------------- |
| **Workflow** | Fixed graph (author→reviewer) | Dynamic planning |
| **Capabilities** | Only what you code | Planning + files + skills |
| **Tools** | Python @tool functions | SKILL.md files |
| **Complexity** | You manage state flow | Built-in state management |
| **Use Case** | Specific, predictable flows | Open-ended tasks |

## Further Reading

[Introduction to DeepAgents](https://docs.langchain.com/oss/python/deepagents/overview) - Official LangChain documentation covering architecture and use cases

[The agentskills.io Specification](https://agentskills.io) - Standard format for defining agent skills

[Planning in AI Agents](https://blog.langchain.com/planning-in-ai-agents/) - Deep dive into how agents decompose complex tasks

### DeepAgents CLI Tool

While this exercise integrates DeepAgents into our chatbot, [`deepagents-cli`](https://github.com/langchain-ai/deepagents) is also available as a companion terminal user interface (TUI) :

```bash
# Install and run
pip install deepagents-cli
deepagents "Create a summary of all Python files in src/"
```

The CLI provides real-time visualization of agent planning, interactive skill selection, file tree navigation with diff previews, and streaming output with syntax highlighting.

---

| 🏠 [Overview](/README.md) | ◀️ [Previous exercise](/src/chatbot/lessons/exercises/e08_custom_agent/README.md) | ✅ [Solution](/src/chatbot/lessons/solutions/s09_deep_agent/README.md) | ▶️ [Next exercise](/src/chatbot/lessons/exercises/e10_a2a/README.md) |
| --- | --- | --- | --- |
