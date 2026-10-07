from lab.apps.bare_agent.features.agent.domain import ChainOfThought, LeanChainOfThought


class MemoryThoughtRepository:
    def __init__(self) -> None:
        self._chains: list[ChainOfThought] = []

    async def create(self, cot: ChainOfThought) -> ChainOfThought:
        self._chains.append(cot)
        return cot

    async def get_all_by_chat_id(self, chat_id: str) -> list[LeanChainOfThought]:
        cots: list[LeanChainOfThought] = []

        for cot in self._chains:
            if cot.chat_id == chat_id:
                cots.append(cot)

        return cots

    async def get_by_id(self, chain_id: str) -> ChainOfThought | None:
        for cot in self._chains:
            if cot.id == chain_id:
                return cot

        return None

    async def remove(self, chain_id: str) -> str:
        self._chains = [cot for cot in self._chains if cot.id != chain_id]
        return chain_id

    async def update(self, chain_id: str, cot: ChainOfThought) -> ChainOfThought:
        self._chains = [
            cot if current.id == chain_id else current for current in self._chains
        ]
        return cot
