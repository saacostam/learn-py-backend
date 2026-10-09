from openai import AsyncOpenAI

from lab.apps.bare_agent.shared.adapters.domain import (
    LLMProvider,
    Message,
    OutputT,
)


class OpenAiLLMProvider(LLMProvider):
    def __init__(self, client: AsyncOpenAI, model: str = "gpt-6-luna") -> None:
        self._client = client
        self._model = model

    async def generate(
        self,
        messages: list[Message],
        output_schema: type[OutputT],
    ) -> OutputT:
        response = await self._client.responses.parse(
            model=self._model,
            input=[
                {
                    "role": message.role.value,
                    "content": message.content,
                }
                for message in messages
            ],
            text_format=output_schema,
        )

        result = response.output_parsed

        if result is None:
            raise ValueError("OpenAI did not return a structured output.")

        return result
