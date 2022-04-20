import os
from dotenv import load_dotenv

import arrow
from eth_blocky import EthBlocky

load_dotenv()

NODE_URL = os.getenv("NODE_URL")

# check timestamps
# check timestamp difference

def test_closest_block_before():
    timestamp = arrow.get('2021-03-11T12:00:00').timestamp()
    client = EthBlocky(NODE_URL)

    block = client.closest_block(timestamp, before=True)

    assert block.number == 12017166
    assert block.timestamp < timestamp
    assert timestamp - block.timestamp < 60

def test_closest_block_after():
    timestamp = arrow.get('2021-03-11T12:00:00').timestamp()
    client = EthBlocky(NODE_URL)

    block = client.closest_block(timestamp)

    assert block.number == 12017167
    assert block.timestamp > timestamp
    assert block.timestamp - timestamp < 60
