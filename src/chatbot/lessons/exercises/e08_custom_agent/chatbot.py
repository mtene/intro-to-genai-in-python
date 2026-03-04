from typing import override, Dict
from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph, START, END
from langgraph.graph.state import CompiledStateGraph
from chatbot.chatbot_base import BaseChatBot
from chatbot.chat_context import ChatContext
from chatbot.chat_history import (
    ChatHistory,
    assistant_message,
    user_message,
)
from .author import author
from .reviewer import reviewer
from .state import GraphState


# node that increments the loop iteration counter
def _update_iteration(state: GraphState) -> Dict:
    """Loop iteration increment"""
    return {"iteration": state.iteration + 1}


# end condition node
def _end_condition(state: GraphState, config: RunnableConfig) -> str:
    """returns 'continue' or 'finish'"""
    update_status = ChatContext.from_config(config)
    # TODO: add the logic to determine continue_loop
    continue_loop = False
    if continue_loop:
        update_status("🔄 EndCondition: continuing...")
        return "continue"
    else:
        update_status("✋ EndCondition: stopping...")
        return "finish"


# Chat bot implementation
class ChatBot(BaseChatBot):
    """Uses an LLM with a custom graph"""

    def __init__(self):
        self._agent = self._build_agent()
        self._chat_history = ChatHistory()

    def _build_agent(self) -> CompiledStateGraph[GraphState]:
        """Builds a custom graph"""
        graph_builder = StateGraph(GraphState)
        # define nodes
        graph_builder.add_node("Author", author)
        graph_builder.add_node("Reviewer", reviewer)
        graph_builder.add_node("UpdateIteration", _update_iteration)
        # define edges
        graph_builder.add_edge(START, "Author")
        graph_builder.add_edge("Author", "Reviewer")
        graph_builder.add_edge("Reviewer", "UpdateIteration")
        graph_builder.add_conditional_edges(
            "UpdateIteration", _end_condition, {"continue": "Author", "finish": END}
        )
        # build graph
        return graph_builder.compile()

    @override
    def reset(self) -> None:
        """Reset chatbot to initial state"""
        self._chat_history.clear()

    @override
    def get_answer(self, question: str, ctx: ChatContext) -> str:
        """
        Produce the assistant's reply to the provided user question.
        Can use ctx to emit status updates, which will be displayed in the UI.
        """
        # record question in chat history
        self._chat_history.add_message(user_message(question))
        # create the initial state
        initial_state = GraphState(
            messages=self._chat_history.messages, feedback="create the first draft"
        )
        # invoke the graph on the state with the context
        final_state = self._agent.invoke(initial_state, config=self.get_config(ctx))
        # extract the answer from the text field of the final state
        answer = final_state["text"]
        # record answer in chat history
        self._chat_history.add_message(assistant_message(answer))

        return answer
