from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class Participant(BaseModel):
    username: str
    id: str

class Participants(BaseModel):
    data: List[Participant]

class Conversation(BaseModel):
    participants: Participants
    id: str

class Cursors(BaseModel):
    after: str

class Paging(BaseModel):
    cursors: Optional[Cursors] = None
    next: Optional[str] = None

class ConversationsResponse(BaseModel):
    data: List[Conversation]
    paging: Optional[Paging] = None

class UserConversationResponse(BaseModel):
    data: List[Conversation]

class MessageFrom(BaseModel):
    username: str
    id: str

class MessageItem(BaseModel):
    text: str = Field(alias="message")
    from_: MessageFrom = Field(alias="from")
    created_time: str
    id: str

class Messages(BaseModel):
    data: List[MessageItem]
    paging: Optional[Paging] = None

class MessagesListResponse(BaseModel):
    messages: Optional[Messages] = None
    id: str


class MessageRecipient(BaseModel):
    id: str

class SendMessage(BaseModel):
    text: str

class SendMessageScheme(BaseModel):
    recipient: MessageRecipient
    message: SendMessage


# Webhook

class SenderUser(BaseModel):
    id: str

class RecipientUser(BaseModel):
    id: str

class IncomeMessage(BaseModel):
    mid: str
    text: str

class Value(BaseModel):
    sender: SenderUser
    recipient: RecipientUser
    timestamp: str
    message: IncomeMessage

class WebhookMessageResponse(BaseModel):
    field: str
    value: Value

