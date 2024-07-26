from pydantic import BaseModel


class Message(BaseModel):
    prompt: str
