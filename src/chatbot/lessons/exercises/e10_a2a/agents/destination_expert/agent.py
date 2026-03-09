"""Destination Expert Agent - Provides destination recommendations"""

from langchain_core.messages import AIMessage

# TODO: Replace this placeholder with a real agent implementation
# Use: from langchain.agents import create_agent
# Use: from chatbot.services.llm import LLM
#
# Create a system prompt for the destination expert that:
# - Recommends destinations based on interests and preferences
# - Suggests 2-3 specific destinations with explanations
# - Mentions the best time to visit
# - Highlights unique attractions
# - Keeps responses concise and actionable
# - Includes an example response format
#
# Then create the agent with:
# agent = create_agent(model=LLM(), system_prompt=_system_prompt)


# Placeholder agent that returns a not-implemented message
class _PlaceholderAgent:
    def invoke(self, *args, **kwargs):
        return {"messages": [AIMessage(content="I can't help you, not implemented!")]}


agent = _PlaceholderAgent()
