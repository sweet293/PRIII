### config.py ###
import logging
import socket
import json

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Default node configurations
DEFAULT_NODES_CONFIG = [
    {"id": 1, "host": "127.0.0.1", "port": 5001},
    {"id": 2, "host": "127.0.0.1", "port": 5002},
    {"id": 3, "host": "127.0.0.1", "port": 5003}
]

# Timing configurations (in seconds)
HEARTBEAT_INTERVAL = 0.5
MIN_ELECTION_TIMEOUT = 1.5
MAX_ELECTION_TIMEOUT = 3.0