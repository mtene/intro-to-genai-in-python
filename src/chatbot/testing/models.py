"""Adapters that let DeepEval use the course's configured LLM."""

from typing import Any, cast, override

from deepeval.models import DeepEvalBaseLLM

from chatbot.services.llm import LLM


class EvaluationModel(DeepEvalBaseLLM):
    """Use the same configured local or remote model as an LLM judge."""

    @override
    def load_model(self) -> Any:
        return cast(Any, LLM)(temperature=0)

    @override
    def generate(self, prompt: str, schema=None) -> Any:
        if schema is not None:
            return cast(Any, self.model).with_structured_output(schema).invoke(prompt)
        response = cast(Any, self.model).invoke(prompt)
        return str(response.content)

    @override
    async def a_generate(self, prompt: str, schema=None) -> Any:
        if schema is not None:
            return (
                await cast(Any, self.model)
                .with_structured_output(schema)
                .ainvoke(prompt)
            )
        response = await cast(Any, self.model).ainvoke(prompt)
        return str(response.content)

    @override
    def get_model_name(self) -> str:
        return str(cast(Any, self.model).model_name)
