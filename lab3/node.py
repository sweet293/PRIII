### node.py ###
import time
import random
import logging
from typing import List, Dict, Any
from models import NodeState, NodeConfig, RaftState
from network import NetworkManager
from messages import RequestVoteMessage, VoteResponseMessage, HeartbeatMessage
from config import HEARTBEAT_INTERVAL, MIN_ELECTION_TIMEOUT, MAX_ELECTION_TIMEOUT
import socket
import json


class RaftNode:
    def __init__(self, config: NodeConfig, peer_addresses: List[tuple]):
        self.logger = logging.getLogger(f"Node-{config.node_id}")
        self.config = config
        self.peer_addresses = peer_addresses

        # Initialize state
        self.raft_state = RaftState()
        self.election_timeout = random.uniform(MIN_ELECTION_TIMEOUT, MAX_ELECTION_TIMEOUT)
        self.last_heartbeat = time.time()

        # Initialize network
        self.network = NetworkManager(config.host, config.port)

        # Control flag
        self.running = True

    def request_votes(self):
        """Send RequestVote RPCs to all peers."""
        self.raft_state.current_term += 1
        self.raft_state.voted_for = self.config.node_id
        self.raft_state.votes_received = 1  # Vote for self

        message = RequestVoteMessage.create(
            term=self.raft_state.current_term,
            candidate_id=self.config.node_id
        ).__dict__

        self.logger.info(f"Requesting votes for term {self.raft_state.current_term}")
        self.network.broadcast_message(message, self.peer_addresses)

    def send_heartbeat(self):
        """Send heartbeat messages to all peers."""
        message = HeartbeatMessage.create(
            term=self.raft_state.current_term,
            leader_id=self.config.node_id
        ).__dict__

        self.network.broadcast_message(message, self.peer_addresses)


    def handle_vote_request(self, message: Dict[str, Any], sender_address: tuple):
        """Handle incoming vote requests."""
        if message["term"] > self.raft_state.current_term:
            self.raft_state.current_term = message["term"]
            self.raft_state.state = NodeState.FOLLOWER
            self.raft_state.voted_for = None

        vote_granted = (message["term"] >= self.raft_state.current_term and
                        (self.raft_state.voted_for is None or
                         self.raft_state.voted_for == message["candidate_id"]))

        if vote_granted:
            self.raft_state.voted_for = message["candidate_id"]
            self.raft_state.current_term = message["term"]
            self.logger.info(f"Granted vote to node {message['candidate_id']}")
        else:
            self.logger.info(f"Rejected vote for node {message['candidate_id']}")

        response = VoteResponseMessage.create(
            term=self.raft_state.current_term,
            vote_granted=vote_granted
        ).__dict__

        self.network.send_message(response, sender_address)

    def handle_vote_response(self, message: Dict[str, Any]):
        """Handle responses to vote requests."""
        if message["term"] > self.raft_state.current_term:
            self.raft_state.current_term = message["term"]
            self.raft_state.state = NodeState.FOLLOWER
            self.raft_state.voted_for = None
            return

        if message["vote_granted"] and self.raft_state.state == NodeState.CANDIDATE:
            self.raft_state.votes_received += 1
            if self.raft_state.votes_received > len(self.peer_addresses) // 2:
                self.raft_state.state = NodeState.LEADER
                self.logger.info(f"Became leader for term {self.raft_state.current_term}")
                self.send_heartbeat()

    def handle_heartbeat(self, message: Dict[str, Any]):
        """Handle heartbeat messages from the leader."""
        if message["term"] >= self.raft_state.current_term:
            self.raft_state.current_term = message["term"]
            self.raft_state.state = NodeState.FOLLOWER
            self.raft_state.voted_for = None
            self.last_heartbeat = time.time()
            self.logger.info(f"Received heartbeat from leader {message['leader_id']}")

    def simulate_node_failure(self, duration):

        """Simulate node failure for a given duration in seconds."""
        logging.warning(f"Node {self.config.node_id} is simulating failure for {duration} seconds.")
        time.sleep(duration)
        self.running = False
        logging.info(f"Node {self.config.node_id} has recovered.")

    def run(self):
        """Main loop for the Raft node."""

        while self.running:
            try:
                # Check for timeout
                if (self.raft_state.state != NodeState.LEADER and
                        time.time() - self.last_heartbeat > self.election_timeout):
                    self.raft_state.state = NodeState.CANDIDATE
                    self.request_votes()
                    self.last_heartbeat = time.time()

                # Leader sends heartbeats
                if (self.raft_state.state == NodeState.LEADER and
                        time.time() - self.last_heartbeat > HEARTBEAT_INTERVAL):
                    self.send_heartbeat()
                    self.last_heartbeat = time.time()

                # Handle incoming messages
                try:
                    message, addr = self.network.receive_message()

                    if message["type"] == "REQUEST_VOTE":
                        self.handle_vote_request(message, addr)
                    elif message["type"] == "VOTE_RESPONSE":
                        self.handle_vote_response(message)
                    elif message["type"] == "HEARTBEAT":
                        self.handle_heartbeat(message)

                except socket.timeout:
                    continue
                except json.JSONDecodeError:
                    self.logger.error("Received malformed message")
                    continue

            except Exception as e:
                self.logger.error(f"Error in main loop: {e}")

    def stop(self):
        """Stop the Raft node."""
        self.running = False
        self.network.close()