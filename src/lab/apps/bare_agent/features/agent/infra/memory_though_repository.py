from lab.apps.bare_agent.features.agent.domain import ChainOfThough, LeanChainOfThough


class MemoryThoughRepository:
    def __init__(self) -> None:
        self._chains: list[ChainOfThough] = []

    async def create(self, cot: ChainOfThough) -> ChainOfThough:
        self._chains.append(cot)
        return cot

    async def get_all_by_chat_id(self, chat_id: str) -> list[LeanChainOfThough]:
        cots: list[LeanChainOfThough] = []

        for cot in self._chains:
            if cot.chat_id == chat_id:
                cots.append(cot)

        return cots

    async def get_by_id(self, chain_id: str) -> ChainOfThough | None:
        for cot in self._chains:
            if cot.id == chain_id:
                return cot

        return None

    async def remove(self, chain_id: str) -> str:
        self._chains = [cot for cot in self._chains if cot.id != chain_id]
        return chain_id

    async def update(self, chain_id: str, cot: ChainOfThough) -> ChainOfThough:
        self._chains = [
            cot if current.id == chain_id else current for current in self._chains
        ]
        return cot
