### main.py ###
import threading
import time
from typing import List
from models import NodeConfig
from node import RaftNode
from config import DEFAULT_NODES_CONFIG
import socket
import json
import random




def create_peer_addresses(configs: List[dict], node_id: int) -> List[tuple]:
    """Create list of peer addresses excluding the current node."""
    return [(config["host"], config["port"])
            for config in configs if config["id"] != node_id]


def run_simulation(nodes_config: List[dict] = DEFAULT_NODES_CONFIG):
    """Run the RAFT simulation with the given configuration."""
    nodes = []
    threads = []

    # Create and start nodes
    for config in nodes_config:
        peer_addresses = create_peer_addresses(nodes_config, config["id"])

        node = RaftNode(
            config=NodeConfig(
                node_id=config["id"],
                host=config["host"],
                port=config["port"]
            ),
            peer_addresses=peer_addresses
        )

        random_integer = random.randint(5, 20)
        node.simulate_node_failure(random_integer)

        thread = threading.Thread(target=node.run)
        thread.start()

        nodes.append(node)
        threads.append(thread)

    return nodes, threads


if __name__ == "__main__":
    try:
        # Start the simulation
        nodes, threads = run_simulation()

        # Let it run for some time
        time.sleep(3000)

    finally:
        # Clean shutdown
        for node in nodes:
            node.stop()
        for thread in threads:
            thread.join()