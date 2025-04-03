# AES (Advanced Encryption Standard) Implementation in Python

This repository provides an implementation of the AES algorithm and various modes of operation (including ECB and AEAD modes) in Python. The goal is to demonstrate how AES encryption and decryption work, along with its key scheduling, padding mechanisms, and encryption modes.

The main objective is to show the internals of AES through source code. If you want to learn more about AES and its concepts, feel free to visit my blog at KEM-seculab: [Rijndael on KEM-seculab](https://kem.gitbook.io/cybersecurity/cryptography/rijndael).

## Features

- **AES Algorithm**: Core AES encryption and decryption implementation.
- **Key Expansion**: Generates round keys for each round during encryption/decryption.


## Modes of Operation

- **ECB (Electronic Codebook)**: Encrypts each block independently (vulnerable to certain attacks).
- **GCM (Galois/Counter Mode)**: Provides both encryption and integrity verification (AEAD mode).
