"""Budget Expert Agent - Provides travel budget advice"""

from langchain_core.messages import AIMessage

# TODO: Replace this placeholder with a real agent implementation
# Use: from langchain.agents import create_agent
# Use: from chatbot.services.llm import LLM
#
# Create a system prompt for the budget expert that:
# - Estimates realistic daily budgets for destinations
# - Breaks down costs (accommodation, food, transport, activities)
# - Mentions seasonal pricing patterns
# - Keeps responses concise (3-5 sentences)
# - Includes an example response format
#
# Then create the agent with:
# agent = create_agent(model=LLM(), system_prompt=_system_prompt)


# Placeholder agent that returns a not-implemented message
class _PlaceholderAgent:
    def invoke(self, *args, **kwargs):
        return {"messages": [AIMessage(content="I can't help you, not implemented!")]}


agent = _PlaceholderAgent()
