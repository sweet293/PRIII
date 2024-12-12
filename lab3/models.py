### models.py ###
from enum import Enum
from typing import Dict, List, Optional
import socket
import json

class NodeState(Enum):
    FOLLOWER = "FOLLOWER"
    CANDIDATE = "CANDIDATE"
    LEADER = "LEADER"

class NodeConfig:
    def __init__(self, node_id: int, host: str, port: int):
        self.node_id = node_id
        self.host = host
        self.port = port

    @property
    def address(self) -> tuple:
        return (self.host, self.port)

class RaftState:
    def __init__(self):
        self.current_term: int = 0
        self.voted_for: Optional[int] = None
        self.state: NodeState = NodeState.FOLLOWER
        self.votes_received: int = 0

    def reset_votes(self):
        self.votes_received = 0