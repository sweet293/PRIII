### messages.py ###
from dataclasses import dataclass
from typing import Optional
import socket
import json


@dataclass
class BaseMessage:
    term: int
    type: str


@dataclass
class RequestVoteMessage(BaseMessage):
    candidate_id: int

    @classmethod
    def create(cls, term: int, candidate_id: int):
        return cls(term=term, type="REQUEST_VOTE", candidate_id=candidate_id)


@dataclass
class VoteResponseMessage(BaseMessage):
    vote_granted: bool

    @classmethod
    def create(cls, term: int, vote_granted: bool):
        return cls(term=term, type="VOTE_RESPONSE", vote_granted=vote_granted)


@dataclass
class HeartbeatMessage(BaseMessage):
    leader_id: int

    @classmethod
    def create(cls, term: int, leader_id: int):
        return cls(term=term, type="HEARTBEAT", leader_id=leader_id)
