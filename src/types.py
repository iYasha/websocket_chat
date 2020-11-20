from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, Undefined, config
from enum import Enum, unique
from typing import *
import json


@unique
class ErrorType(Enum):
    SUCCESS = 'success'
    SERVER_ERROR = 'server_error'
    EVENT_NOT_FOUND = 'event_not_found'
    MESSAGE_IS_NULL = 'message_is_null'
    TOKEN_VALIDATION_ERROR = 'token_validation_error'
    CHAT_NOT_EXISTS = 'chat_not_exists'


@unique
class EventType(Enum):
    GET_HISTORY = 'get_history'
    SEND_MESSAGE = 'send_message'
    SEND_FILE = 'send_file'


@unique
class MessageType(Enum):
    TEXT = 'text'
    IMAGE = 'image'
    FILE = 'file'


@dataclass
@dataclass_json(undefined=Undefined.EXCLUDE)
class Message:
    type: MessageType = field(metadata=config(encoder=lambda x: x.value, decoder=lambda x: MessageType(x)))
    text: Optional[str] = None
    created_at: Optional[int] = None
    file_url: Optional[str] = None
    username: Optional[str] = None
    chat_id: Optional[str] = None
    avatar: Optional[str] = None
    user_id: Optional[str] = None
    id: Optional[str] = None


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class Request:
    chat_id: str
    token: str
    event_type: EventType = field(metadata=config(encoder=lambda x: x.value, decoder=lambda x: EventType(x)))
    message: Optional[Message] = None


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class Response:
    type: ErrorType = field(metadata=config(encoder=lambda x: x.value, decoder=lambda x: ErrorType(x)))
    event_type: EventType = field(metadata=config(encoder=lambda x: x.value, decoder=lambda x: EventType(x)))
    messages: List[Message] = field(default_factory=list)
    detail: Optional[str] = None
