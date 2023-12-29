+++
title = 'flagkryptering'
categories = ['blockchain']
date = 2024-12-09T10:12:15+01:00
scrollToTop = true
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

The ```encrypt``` function performs an XOR operation on a key and a flag and returns some ciphertext.
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
Lets ignore the if statements for now an focus on the key generation itself.
```uint256(block.number)``` is redundant as block.number already has the ```uint``` type.

Next up is ```abi.encodePacked```. The primary purpose of ```abi.encodePacked``` is to concatenate and pack multiple values together into a single byte array. When used with a single value, it essentially performs a byte convertion, converting the uint to a byte array.

The result is then passed to a ```keccak256``` method also known as ```SHA-3``` converting the byte array into a hash and then once again doing a redundant type convertion as ```keccak256``` already returns a ```byte32```.
https://en.wikipedia.org/wiki/SHA-3
https://docs.soliditylang.org/en/v0.8.11/abi-spec.html
https://docs.soliditylang.org/en/latest/units-and-global-variables.html


Log from script:
```python
Searched blocknumbers: 1
Searched blocknumbers: 3
Searched blocknumbers: 5
Searched blocknumbers: 7
Searched blocknumbers: 9
Searched blocknumbers: 11
Searched blocknumbers: 13
Searched blocknumbers: 15
Found at block number: 16, Ciphertext: NC3{you_replicated_the_key}
```

## Flag

```
NC3{you_replicated_the_key}
```

## Reflections and Learnings
