from __future__ import annotations

from pydantic import BaseModel, Field


class From(BaseModel):
    id: int
    is_bot: bool
    first_name: str
    last_name: str
    language_code: str


class Chat(BaseModel):
    id: int
    first_name: str
    last_name: str
    type: str


class Message(BaseModel):
    message_id: int
    from_: From = Field(..., alias="from")
    chat: Chat
    date: int
    text: str


class TelegramEvent(BaseModel):
    update_id: int
    message: Message
