from chatbot.testing.test_suite import TestSuite, PassingCriteria, TestCase


# Define test cases using TestCase objects
TEST_CASES = [
    # Test 1: Example skill (should pass in both exercise and solution)
    TestCase(
        id="emoji-decorator-skill",
        question="Add emojis to this text: I love Python programming and building AI agents",
        expected_keywords=[
            "❤️",  # Should add snake for "love"
            "🐍",  # Should add snake for "Python"
            "🤖",  # Should add heart for "AI agents"
        ],
    ),
    # Test 2: Generate flashcards (fails in exercise, passes in solution)
    TestCase(
        id="generate-flashcards-skill",
        question="""Create 5 flashcards from this content:

"Tool calling allows LLMs to invoke external functions. In LangChain, tools are defined
using the @tool decorator. The ReAct pattern enables agents to use tools in a loop until
the task is complete."

Include questions about tool definition, the @tool decorator, and the ReAct pattern.""",
        expected_keywords=[
            "Q:",
            "A:",
            "@tool",
            "ReAct",
        ],
    ),
    # Test 3: Generate quiz questions (fails in exercise, passes in solution)
    TestCase(
        id="create-quiz-questions-skill",
        question="""Create 3 quiz questions from this content:

"RAG (Retrieval Augmented Generation) combines LLMs with external knowledge retrieval.
It involves chunking documents, creating embeddings, storing in a vector database,
retrieving relevant chunks, and augmenting the LLM prompt."

Make sure each question has 4 options (A-D) and an explanation.""",
        expected_keywords=[
            "A:",
            "B:",
            "C:",
            "D:",
            "Answer:",
            "Explanation:",
            "RAG",
        ],
    ),
    # Test 4: Multi-skill planning (fails in exercise, passes in solution)
    TestCase(
        id="multiple-skills",
        question="""Create a complete study guide about DeepAgents with:
- 3 flashcards covering what DeepAgents is and how it differs from basic agents
- 2 quiz questions testing understanding of skills and planning

Both flashcards and quiz should be included in your response.""",
        expected_keywords=[
            "flashcard",
            "quiz",
            "Q:",
            "A:",
            "Answer:",
            "DeepAgent",
        ],
    ),
    # Test 5: File reading + skill usage (tests filesystem backend)
    TestCase(
        id="file-reading-with-skill",
        question="""Create 3 quiz questions for the README.md in exercise 9.""",
        expected_keywords=[
            "A.",
            "B.",
            "Correct answer:",
            "skill",
        ],
    ),
]

# Define passing criteria
PASSING_CRITERIA = PassingCriteria(
    min_success_rate=0.8,
)

# Create the complete test suite
TEST_SUITE = TestSuite(
    test_cases=TEST_CASES, passing_criteria=PASSING_CRITERIA, repetitions=1
)
