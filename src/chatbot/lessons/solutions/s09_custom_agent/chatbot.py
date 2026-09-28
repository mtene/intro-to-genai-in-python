import uuid
from typing import override, Dict
from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph, START, END
from langgraph.graph.state import CompiledStateGraph
from langgraph.checkpoint.memory import MemorySaver
from chatbot.chatbot_base import BaseChatBot
from chatbot.chat_context import ChatContext
from .author import author
from .reviewer import reviewer
from .state import GraphState


# node that updates the loop iteration
def _update_iteration(state: GraphState) -> Dict:
    """Simple loop iteration increment"""
    return {"iteration": state.iteration + 1}


# loop end condition
def _end_condition(state: GraphState, config: RunnableConfig) -> str:
    """returns 'continue' or 'finish', stopping the process after 3 loop iterations or when there is no more feedback"""
    update_status = ChatContext.from_config(config)
    if state.iteration > 3:
        update_status("✋ EndCondition: number of turns exhausted (3), stopping...")
        return "finish"
    if not state.text:
        update_status("🔄 EndCondition: text is blank, continuing...")
        return "continue"
    if not state.feedback:
        update_status("✋ EndCondition: text approved, stopping...")
        return "finish"
    update_status("🔄 EndCondition: feedback needs to be addressed, continuing...")
    return "continue"


# Chat bot implementation
class ChatBot(BaseChatBot):
    """Uses an LLM in a custom graph"""

    def __init__(self):
        # model behavior based on a custom graph
        self._agent = self._build_agent()
        self._thread_id = str(uuid.uuid4())

    def _build_agent(self) -> CompiledStateGraph[GraphState]:
        """Builds a graph with 3 personas in a loop: author, reviewer, supervisor"""
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
        # build graph with checkpointer for conversation memory
        return graph_builder.compile(checkpointer=MemorySaver())

    @override
    def reset(self) -> None:
        """Reset chatbot to initial state"""
        # Generate new thread ID to start fresh conversation
        self._thread_id = str(uuid.uuid4())

    @override
    def get_answer(self, question: str, ctx: ChatContext) -> str:
        """
        Produce the assistant's reply to the provided user question.
        Can use ctx to emit status updates, which will be displayed in the UI.
        """
        ctx.update_status("🧠 Thinking...")

        # Create the initial state with new user message
        # Checkpointer automatically loads previous messages
        initial_state = GraphState(
            messages=[HumanMessage(content=question)], feedback="create the first draft"
        )
        # Invoke the graph with thread_id for conversation memory
        final_state = self._agent.invoke(
            initial_state,
            config={
                **self.get_config(ctx),
                "configurable": {"thread_id": self._thread_id},
            },
        )
        # Extract the answer from the text field of the final state
        answer = final_state["text"]

        return answer
