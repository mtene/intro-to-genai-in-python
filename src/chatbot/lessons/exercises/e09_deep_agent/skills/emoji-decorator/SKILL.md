---
name: emoji-decorator
description: Adds relevant emojis to text to make it more expressive and engaging. Use this when the user wants to enhance text with emojis or make content more visually appealing.
---

# Emoji Decorator

## Purpose
Enhance plain text by adding contextually relevant emojis that match the content's meaning and tone.

## Instructions
1. Read and understand the input text
1. Identify key concepts, emotions, and important phrases
1. Select emojis that accurately represent those concepts
1. Insert 1-2 emojis after relevant phrases
1. Preserve all original text - only add emojis, never modify words

## Input
Any plain text that the user wants to make more expressive.

## Output Format
Return the original text with emojis strategically placed:

```markdown
**Original:** I love learning about AI and building applications.

**Decorated:** I love ❤️ learning about AI 🤖 and building applications 🏗️.
```

## Quality Guidelines
* Use emojis that match the context and tone
* Don't overuse - aim for 1 emoji per sentence or major phrase
* Maintain readability - text should still be clear without the emojis
* Choose universally recognized emojis when possible
* Avoid ambiguous or potentially offensive emojis

## Examples

### Example 1: Technical Content
**Input:** "Python is great for data science and machine learning"
**Output:** "Python 🐍 is great for data science 📊 and machine learning 🤖"

### Example 2: Emotional Content
**Input:** "I'm so excited to start this new project!"
**Output:** "I'm so excited 🎉 to start this new project 🚀!"

### Example 3: Educational Content
**Input:** "Remember to save your work frequently and test your code"
**Output:** "Remember to save 💾 your work frequently and test ✅ your code"
