import uuid


# Implements IdGenerator
class UuidGenerator:
    def gen(self) -> str:
        return str(uuid.uuid4())
