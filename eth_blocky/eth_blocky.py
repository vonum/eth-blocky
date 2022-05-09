import  arrow
from web3 import Web3


class EthBlocky:

    def __init__(self, url):
        self.web3 = Web3(Web3.HTTPProvider(url))

    def closest_block(self, timestamp, before=False):
        start_block = 1
        end_block = self.web3.eth.get_block("latest").number
        return self._closest_block(timestamp, start_block, end_block, before)

    def _closest_block(self, timestamp, start_block, end_block, before):
        start_timestamp = self._timestamp(start_block)
        end_timestamp = self._timestamp(end_block)

        if start_block == end_block:
            block = self._block(start_block)
            return self._best_match(timestamp,
                                    block,
                                    before)

        avg_block_time = self._average_block_time(start_block,
                                                  end_block,
                                                  start_timestamp,
                                                  end_timestamp)

        d = self._distance_from_block(timestamp, start_timestamp, end_timestamp)
        expected_block = self._expected_block(start_block, end_block, d)
        expected_timestamp = self._timestamp(expected_block)

        block_delta = self._estimated_blocks_to_target(timestamp,
                                                       expected_timestamp,
                                                       avg_block_time)
        expected_block += block_delta
        r = abs(block_delta)
        if r == 1: r = 0

        return self._closest_block(timestamp,
                                   expected_block - r,
                                   expected_block + r,
                                   before)

    # number of timestamps in range / number of blocks in range
    def _average_block_time(self, start_block, end_block,
                            start_timestamp, end_timestamp):
        return (end_timestamp - start_timestamp) / (end_block - start_block)

    # distance from from start to end block [0, 1]
    def _distance_from_block(self, timestamp, start_timestamp, end_timestamp):
        return (timestamp - start_timestamp) / (end_timestamp - start_timestamp)

    # moves start block by approximated distance
    def _expected_block(self, start_block, end_block, distance):
        return int(start_block + distance * (end_block - start_block))

    def _estimated_blocks_to_target(self, timestamp, expected_timestamp, avg_block_time):
        return int((timestamp - expected_timestamp) / avg_block_time)

    def _best_match(self, timestamp, block, before):
        if before:
            return self._best_before(timestamp, block)
        else:
            return self._best_eq_or_after(timestamp, block)

    def _best_before(self, timestamp, block):
        if block.timestamp == timestamp:
            return self._block(block.number - 1)
        elif block.timestamp > timestamp:
            while block.timestamp >= timestamp:
                block = self._block(block.number - 1)
            return self._block(block.number)
        elif block.timestamp < timestamp:
            while block.timestamp < timestamp:
                block = self._block(block.number + 1)
            return self._block(block.number - 1)

    def _best_eq_or_after(self, timestamp, block):
        if block.timestamp == timestamp:
            return block
        elif block.timestamp > timestamp:
            while block.timestamp > timestamp:
                block = self._block(block.number - 1)
            return self._block(block.number + 1)
        elif block.timestamp < timestamp:
            while block.timestamp < timestamp:
                block = self._block(block.number + 1)
            return self._block(block.number)

    def _block(self, block):
        return self.web3.eth.get_block(block)

    def _timestamp(self, block):
        return self._block(block).timestamp
