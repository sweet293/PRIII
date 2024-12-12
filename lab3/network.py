### network.py ###
import socket
import json
import logging
from typing import List, Dict, Any, Tuple
import json

class NetworkManager:
    def __init__(self, host: str, port: int):
        self.logger = logging.getLogger(f"Network-{port}")
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((host, port))

    def send_message(self, message: Dict[str, Any], address: Tuple[str, int]):
        """Send a UDP message to a specific address."""
        try:
            self.socket.sendto(json.dumps(message).encode(), address)
        except Exception as e:
            self.logger.error(f"Error sending message to {address}: {e}")

    def broadcast_message(self, message: Dict[str, Any], peer_addresses: List[Tuple[str, int]]):
        """Send a message to all peers."""
        for peer in peer_addresses:
            self.send_message(message, peer)

    def receive_message(self, timeout: float = 0.1) -> Tuple[Dict[str, Any], Tuple[str, int]]:
        """Receive and parse a message."""
        self.socket.settimeout(timeout)
        data, addr = self.socket.recvfrom(1024)
        return json.loads(data.decode()), addr

    def close(self):
        """Close the socket."""
        self.socket.close()
