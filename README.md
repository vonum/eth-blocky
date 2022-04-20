# eth-blocky
Package providing date utilities for finding blocks.

With `eth-blocky`, you can:
1. Find the closest block to a given timestamp that happened before
2. Find the closest block to a given timestamp that happened at the exact same
   time or after

### Installation
1. `pip install eth-blocky`

### Usage
Provide a timestamp for which you want to find the closest block, and as a
result you will get the block object. For more information check out [web3
docs](https://web3py.readthedocs.io/en/stable/)

```Python
from eth_blocky import EthBlocky

client = EthBlocky(NODE_URL)

# 2021-03-11T12:00:00
timestamp = 1615464000

block = client.closest_block(timestamp, before=True)
print(block.number)
# 12017166

block = client.closest_block(timestamp)
print(block.number)
# 12017167
```

### Method
`eth-blocky` works as an optimized binary search.
Start with finding the first and latest block as the boundry. Left and right
block.

Steps:
1. Get left and right block and their timestamps
2. Calculate the average time for blocks to being mined in this time range
3. Estimate distance from start block based on timestamps [1, 3, 10] -> 0.3
4. Estimate wanted block based on distance
5. Calculate potential error
6. Repeat from step 1 with [estimated block - error, estimated block + error] as
   the left and right block

The process is repeated until left block is equal to right block.
