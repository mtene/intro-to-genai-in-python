import logging
from typing import override, List, Any, Callable, Dict
from uuid import UUID
from threading import Lock
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.callbacks.manager import CallbackManager
from langchain_core.runnables import RunnableConfig
from langchain_core.outputs import LLMResult
from langchain_core.messages import ToolMessage
from chatbot.config import config
from chatbot.chat_history import ChatMessage


class ChatContext(BaseCallbackHandler):
    """Can be used to post status update messages to the UI"""

    def __init__(self, status_update_func: Callable[[str], None] | None = None):
        self._status_update_func = status_update_func
        self._tool_call_registry: Dict[UUID, str] = {}
        self._lock = Lock()
        self._verbose = config.get_log_level() == logging.DEBUG

    @override
    def on_text(self, text: str, **kwargs: Any) -> None:
        """Updates status on demand from graph nodes"""
        self.update_status(text)

    @override
    def on_custom_event(self, name: str, data: dict, **_):
        if name == "text":
            text = data.get("text", "")
            self.update_status(text)

    @override
    def on_tool_start(
        self, serialized: Dict[str, Any], input_str: str, *, run_id: UUID, **kwargs
    ) -> None:
        """Updates status on tool call start"""
        tool_name = serialized.get("name", "tool")
        with self._lock:
            self._tool_call_registry[run_id] = tool_name
        max_output = 100
        args_str = input_str.strip('{}')
        args_str = f"{args_str[:max_output]}...[{len(args_str) - max_output} more]" if len(args_str) > max_output else args_str
        self.update_status(f"🔨 Calling {tool_name}({args_str})")

    @override
    def on_tool_end(self, output: Any, *, run_id: UUID, **kwargs) -> None:
        """Updates status on tool call end"""
        with self._lock:
            tool_name = self._tool_call_registry.pop(run_id, "tool")
        max_output = 100
        result_str = str(output.content) if isinstance(output, ToolMessage) else str(output)
        result_str = f"{result_str[:max_output]}...[{len(result_str) - max_output} more]" if len(result_str) > max_output else result_str
        self.update_status(f"📦 {tool_name} returned: {result_str}")

    @override
    def on_tool_error(
        self, error: BaseException, *, run_id: UUID, **kwargs: Any
    ) -> None:
        """Updates status on tool call error"""
        with self._lock:
            name = self._tool_call_registry.pop(run_id, "tool")
        self.update_status(f"❌ Failed {name}: {repr(error)}")

    @override
    def on_chat_model_start(
        self, serialized: Dict[str, Any], messages: List[List[ChatMessage]], **kwargs
    ):
        """Updates status on LLM request"""
        if not self._verbose:
            return
        self.update_status("=== CHAT REQUEST ===")
        for batch in messages:
            for message in batch:
                self.update_status(f"{message.type.upper()}: {message.content}")

    @override
    def on_llm_end(self, response: LLMResult, **kwargs):
        """Updates status on LLM response"""
        if not self._verbose:
            return
        self.update_status("=== CHAT RESPONSE ===")
        for gens in response.generations:
            for generation in gens:
                content = getattr(getattr(generation, "message", None), "content", None)
                assert content is not None
                self.update_status(content)

    @override
    def on_llm_error(self, error: BaseException, **kwargs):
        """Updates status on LLM error"""
        self.update_status(f"❌ LLM failed: {repr(error)}")

    def update_status(self, message: str) -> None:
        """Updates status with the provided message"""
        if self._status_update_func:
            self._status_update_func(message)

    @staticmethod
    def from_config(config: RunnableConfig) -> Callable[[str], None]:
        callback_mgr = CallbackManager.configure(config.get("callbacks"))
        return lambda text: callback_mgr.on_custom_event("text", {"text": text})
