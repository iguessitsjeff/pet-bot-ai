from enum import StrEnum
from typing import List, Optional

from pydantic import BaseModel, Field, TypeAdapter

from src.utils.decode import decode_and_uncompress


class LexStates(StrEnum):
    IN_PROGRESS = "InProgress"
    READY_FOR_FULLFILLMENT = "ReadyForFulfillment"
    FAILED = "Failed"
    FULFILLED = "Fulfilled"
    WAITING = "Waiting"
    FULLFILLMENT_IN_PROGRESS = "FulfillmentInProgress"


class DialogAction(BaseModel):
    type: str | None = None


class Value(BaseModel):
    original_value: str | None = Field(None, alias="originalValue")
    interpreted_value: str | None = Field(None, alias="interpretedValue")
    resolved_values: List[str] | None = Field(None, alias="resolvedValues")


class Adjective(BaseModel):
    value: Value | None = None


class Subject(BaseModel):
    value: Value | None = None


class ImageDescriptor(BaseModel):
    value: Value | None = None


class Slots(BaseModel):
    adjective: Adjective | None = Field(None, alias="Adjective")
    subject: Subject | None = Field(None, alias="Subject")
    image_descriptor: ImageDescriptor | None = Field(None, alias="ImageDescriptor")


class Intent(BaseModel):
    name: str | None = None
    slots: Slots | None = None
    state: LexStates


class SessionState(BaseModel):
    intent: Optional[Intent] = None


class LexMessage(BaseModel):
    content: str
    content_type: str = Field(alias="contentType", default=None)


class LexResponse(BaseModel):
    input_mode: str | None = Field(alias="inputMode", default=None)
    content_type: str = Field(alias="contentType", default=None)
    messages: str
    interpretations: str | None = None
    session_state: str | None = Field(alias="sessionState", default=None)
    request_attributes: str | None = Field(alias="requestAttributes", default=None)
    session_id: str | None = Field(alias="sessionId", default=None)
    input_transcript: str | None = Field(alias="inputTranscript", default=None)
    recognized_bot_member: str | None = Field(alias="recognizedBotMember", default=None)

    unpacked_messages: list[LexMessage] | None = None
    unpacked_session_state: SessionState | None = None

    def decode_fields(self):
        self.messages = decode_and_uncompress(self.messages)
        self.session_state = decode_and_uncompress(self.session_state)

        messages_ta: TypeAdapter = TypeAdapter(list[LexMessage])
        self.unpacked_messages = messages_ta.validate_json(self.messages)
        self.unpacked_session_state = SessionState.model_validate_json(
            self.session_state
        )

    def get_text_back(self) -> str:
        text_back: str = ""
        for message in self.unpacked_messages:
            text_back = f"{text_back}{message.content}\n"

        return text_back

    def get_prompt(self) -> str:
        slots = self.unpacked_session_state.intent.slots
        prompt: str = f"{slots.image_descriptor.value.interpreted_value} {slots.adjective.value.interpreted_value} {slots.subject.value.interpreted_value}"
        return prompt
