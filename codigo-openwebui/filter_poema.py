from typing import List, Optional
from pydantic import BaseModel


def get_last_user_message(messages: List[dict]) -> str:
    for message in reversed(messages):
        if message["role"] == "user":
            if isinstance(message["content"], list):
                for item in message["content"]:
                    if item["type"] == "text":
                        return item["text"]
            return message["content"]
    return None


class Filter:
    class Valves(BaseModel):
        prefix: str = "Crie um poema de uma estrofe de "

    def __init__(self):
        self.name = "Prefix of X"

        self.valves = self.Valves(**{})
        pass

    async def inlet(self, body: dict, user: Optional[dict] = None) -> dict:
        messages = body["messages"]
        user_message = get_last_user_message(messages)
        updated_message = self.valves.prefix.strip() + " " + user_message
        for message in reversed(messages):
            if message["role"] == "user":
                message["content"] = updated_message
                break

        body = {**body, "messages": messages}
        return body

    async def outlet(self, body: dict, user: Optional[dict] = None) -> dict:
        return body
