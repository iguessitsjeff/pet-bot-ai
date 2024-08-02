from enum import StrEnum
from typing import Any, Dict, List, Optional

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


class Animal(BaseModel):
    value: Value | None = None


class ImageDescriptor(BaseModel):
    value: Value | None = None


class Slots(BaseModel):
    animal: Animal | None = Field(None, alias="Animal")
    image_descriptor: ImageDescriptor | None = Field(None, alias="ImageDescriptor")


class Intent(BaseModel):
    name: str | None = None
    slots: Slots | None = None
    state: LexStates
    confirmation_state: str | None = Field(None, alias="confirmationState")


class SessionState(BaseModel):
    dialog_action: Optional[DialogAction] = Field(None, alias="dialogAction")
    intent: Optional[Intent] = None
    session_attributes: Optional[Dict[str, Any]] = Field(
        None, alias="sessionAttributes"
    )
    originating_request_id: Optional[str] = Field(None, alias="originatingRequestId")


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
