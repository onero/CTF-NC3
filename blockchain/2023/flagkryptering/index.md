+++
title = 'Flagkryptering'
categories = ['Blockchain']
date = 2023-12-09T10:12:15+01:00
+++

## Challenge Name:

Flagkryptering

## Category:

Blockchain

## Challenge Description:

Nisserne har fundet frem til den smart contract, nissebanditten bruger til at kryptere sine flag på blockchainen.

De har yderligere opsnappet et krypteret flag:

`0xc3523b9a72a40978afbab042b0b5f2d41167c2760491b52925cd727d581ac802`

Kan du dekryptere flaget, så nisserne snart kan gå på juleferie?

## Approach

We were [given a Solidity smart contract](scripts/EncryptedFlag.sol) named EncryptFlag. This contract is for use on the Ethereum blockchain and includes two primary functions: encrypt and generateKey. The goal appears to be to understand and exploit the contract's functionality to retrieve the encrypted flag.

The ```encrypt``` function performs an XOR operation on a key and a flag and returns the ciphertext.
```sol
function encrypt(bytes32 key, bytes32 flag) pure  public returns (bytes32) {
    bytes32 ciphertext = key ^ flag;
    return ciphertext;
}
```
Since we already know the ciphertext we only need the key in order to decrypt and find the flag.
Looking at the ```generateKey``` method we notice that the ```block number``` global variable is used in generating the key.
```sol
function generateKey() view public returns (bytes32) {
    bytes32 key;
    if (block.number > 0) {
        key = bytes32(keccak256(abi.encodePacked(uint256(block.number-1))));
    
    } else {
        key = bytes32(keccak256(abi.encodePacked(uint256(block.number))));           
    }

    return key;
}
```
Ignoring the if statements and focusing on the key generation, we see that:
[uint256(block.number)](units-and-global-variables.html) is redundant as block.number already has the ```uint``` type.

Next up the block.number is passed to [abi.encodePacked](https://docs.soliditylang.org/en/v0.8.11/abi-spec.html). The primary purpose of ```abi.encodePacked``` is to concatenate and pack multiple values together into a single byte array. When used with a single value, it essentially performs a byte convertion, converting the uint to a byte array.

The result is then passed to a ```keccak256``` method also known as [SHA-3](https://en.wikipedia.org/wiki/SHA-3) converting the byte array into a hash and then once again doing a redundant type convertion as ```keccak256``` already returns a ```byte32```.

It therefore seems that the key can be decrypted from the unknown block number and cipher text.

In an Etherium setting, blocks can't be mined faster than [once a second](https://github.com/rolandkofler/blocktime). This means that brute-forcing the network may require an impractical amount of time, particularly if the block number is sufficiently high.

I chose not to risk implementing the contract on the Ethereum network and instead opted to implement the corresponding logic in Python.

Luckily python has a web3 library with a lot of features allowing us to implement the logic without too much hassle. Below is the corresponding python code:

```python
class EncryptFlag:
    def __init__(self):
        pass

    def encrypt(self, key, flag):
        ciphertext = bytes([a ^ b for a, b in zip(key, flag)])
        return ciphertext

    def generate_key(self, block_number):
        if block_number > 0:
            minus_one_block_number_bytes = (block_number-1).to_bytes(32, byteorder='big')
            key = Web3.keccak(minus_one_block_number_bytes)
        else:
            block_number_bytes = block_number.to_bytes(32, byteorder='big')
            key = Web3.keccak(block_number_bytes)
        return key
```
after replicating the code in python we start the brute force using the following code: 
```python
hex_string = "0xc3523b9a72a40978afbab042b0b5f2d41167c2760491b52925cd727d581ac802"
flag = bytes.fromhex(hex_string[2:])

while True:
    key = encrypt_flag.generate_key(block_number)

    ciphertext = encrypt_flag.encrypt(key, flag)
    
    # Convert ciphertext to string to check for 'NC3{'
    ciphertext_str = ciphertext.decode('utf-8', errors='ignore')
    if ciphertext_str.startswith('NC3{'):
        print(f"Found at block number: {block_number}, Ciphertext: {ciphertext_str}")
        break
```

Considering the computational complexity of other challenges, particularly 'in-my-prime', I decided to immediately implement block number save logic. However, this turned out to be unnecessary as the flag was located in the lower blocks.

Log from [Decrypt.py](./scripts/Decrypt.py) script:
```python
Searched blocknumbers: 1
...
...
Found at block number: 16, Ciphertext: NC3{you_replicated_the_key}
```

## Flag

```text
NC3{you_replicated_the_key}
```

## Reflections and Learnings
One can gain valuable insights into setting up a local development blockchain using [Ganache](https://trufflesuite.com/ganache/), learn how to use Python for interacting with Web3, and acquire a fundamental understanding of the Solidity language.

I think it is crucial to thoroughly read and comprehend the underlying logic and documentation before beginning to implement solutions, especially when tackling new subjects. Taking the time to research the topic extensively, going beyond the immediate needs of problem-solving, can prove to be highly rewarding and enriching even when facing time constraints.