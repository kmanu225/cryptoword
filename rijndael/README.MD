# [AES (Advanced Encryption Standard)](https://www.nist.gov/publications/advanced-encryption-standard-aes-0)

<div align="left">
      <a href="https://www.youtube.com/watch?v=O4xNJsjtN6E">
         <img src="http://img.youtube.com/vi/O4xNJsjtN6E/0.jpg" style="width:100%;">
      </a>
</div>

AES is a symmetric 128-bit block encryption algorithm devised by Joan Daemen and Vincent Rijmen, two Belgian cryptographers. The algorithm, also called Rijndael (after the authors' names), was selected as the winner of the NIST 197 competition, whose goal was to find a successor to DES (Data Encryption Standard). DES had become vulnerable to brute-force attacks as computers became increasingly powerful and efficient. AES was specified by NIST in 2001 in **FIPS 197**, which is available on the NIST website. As an encryption algorithm, the purpose of AES is to ensure confidentiality between two parties communicating over a public channel.

# Security Measures  

The security of AES relies on a shared secret key between the parties involved in the confidential communication. Therefore, the key must remain secret.  

- [**Brute Force Attacks**](https://eprint.iacr.org/2022/053):  
AES is inherently vulnerable to brute-force attacks. However, current computers are not efficient enough and do not have sufficient storage to make these attacks feasible.  Intrinsecally AES is not vulnerable to collision attack (see [Birthday paradox](https://en.wikipedia.org/wiki/Birthday_problem#Cast_as_a_collision_problem)) as it is a [PRP (Pseudorandom Permutation)](https://en.wikipedia.org/wiki/Pseudorandom_permutation) function. It is the introduction of nonce or initialization vector (IV) which makes it vulnerable to that attack. 

- [**Biclique Attack**](https://eprint.iacr.org/2011/449.pdf):
The biclique attack, inspired by the Meet-in-the-Middle (MITM) attack, is a cryptanalysis technique that slightly reduces the computational complexity of breaking AES compared to a brute-force attack. This method exploits structural symmetries in AES to efficiently analyze parts of the key schedule and encryption process. While the biclique attack offers a theoretical improvement over brute force, the reduction in computational effort is minimal, making it impractical for real-world use. Additionally, the attack requires an extremely large amount of storage for intermediate computations, further limiting its feasibility in practice.

- [**Quantum Computing**](https://www.polytechnique-insights.com/tribunes/science/lordinateur-quantique-tout-comprendre-en-15-minutes/):  
The potential advent of quantum computers could pose a threat to AES-128 and AES-192 by implementing [Grover's algorithm](https://blog.cr.yp.to/20171017-collisions.html), which could reduce the effective key strength by half. AES-256, however, is considered more resistant to such attacks.  

- [**Implementation Vulnerabilities**](https://ronan.lashermes.0nline.fr/others/poly_AHP.pdf):  
AES can be vulnerable to side-channel attacks if implemented inadequately. These attacks include:
  - **CPA (Correlation Power Analysis)**  
  - **DPA (Differential Power Analysis)**  
  - **NUEVA (Non Uniform Error Value Analysis)**  

Proper implementation and mitigation techniques, such as masking and constant-time operations, are necessary to protect against these vulnerabilities. Below we give a sum up about the efficiency of the attack we described.

| `Attacks`                                                       | `Computational complexity` | `Memory complexity` |
| --------------------------------------------------------------- | -------------------------- | ------------------- |
| Classical computers brute force theoric                         | $O(2^{\|K\|})$             |                     |
| Classical computers brute force pratical (birthday anniversary) | $O(2^{\frac{\|K\|}{2}})$   |                     |
| Quantum computers brute force theoritical (Grover)              | $O(2^{\frac{\|K\|}{2}})$   |                     |
| Quantum computers brute force practical (BHT)                   | $O(2^{\frac{\|K\|}{3}})$   |                     |
| Biclique attack AES-128                                         | $O(2^{\frac{126.1}{2}})$   |                     |
| Biclique attack AES-192                                         | $O(2^{\frac{189.7}{2}})$   |                     |
| Biclique attack AES-256                                         | $O(2^{\frac{254.4}{2}})$   |                     |
| Side channel                                                    | $O(\|K\|)$                 |                     |


# Algorithm

The encryption and decryption process goes as described on the image below.

- $`m`$ is the 128 bits message to encrypt.
- $`c`$ is the encrypted form of $`m`$.
- $`K`$ is the secret key (16, 24 or 32 bytes long).
- $`N`$ is the number of rounds (10, 12, 14).

| Type    | Block Size (bits) | Key Length (bits) | Number of Rounds (N) |
| ------- | ----------------- | ----------------- | ---------------- |
| AES-128 | 128               | 128               | 10               |
| AES-192 | 128               | 192               | 12               |
| AES-256 | 128               | 256               | 14               |

We denote:

```math
m = \begin{bmatrix}
m_0 & m_4 & m_8 & m_{12} \\
m_1 & m_5 & m_9 & m_{13} \\
m_2 & m_6 & m_{10} & m_{14} \\
m_3 & m_7 & m_{11} & m_{15}
\end{bmatrix}
```

![alt text](/rijndael/ressources/aes.drawio.png)

## AddRoundKey

AddRoundKey is a XOR cipher function based on the secret round key. Is is equal to its reciprocal used in the deciphering process ($\oplus = \oplus^{-1}$).

## SubBytes

SubBytes brings the confusion property. It guaranties that each byte is a non-linear and complex transformation of the input. For each byte $c$ :

$\text {SubByte}(c) = M \cdot c^{-1} \oplus v$

Where
$`M = \begin{bmatrix}1&0&0&0&1&1&1&1\\1&1&0&0&0&1&1&1\\1&1&1&0&0&0&1&1\\1&1&1&1&0&0&0&1\\1&1&1&1&1&0&0&0\\0&1&1&1&1&1&0&0\\0&0&1&1&1&1&1&0\\0&0&0&1&1&1&1&1\end{bmatrix}`$

- $`v = \begin{bmatrix} 1 & 1 & 0 & 0 & 0 & 1 & 1 & 0 \end{bmatrix} = 63_{16}`$
- $`c^{-1}`$ is the multiplicative inverse of $`c`$ in the Rinjdael field ($GF(2^{8})/x^{8}+x^{4}+x^{3}+x+1$)

By reduction, $`\text {SubByte}(c)=c^{-1}\oplus (c^{-1} \lll 1)\oplus (c^{-1}\lll 2)\oplus (c^{-1}\lll 3)\oplus (c^{-1}\lll 4)\oplus v`$.

A look up table called the [Sbox](https://en.wikipedia.org/wiki/Rijndael_S-box) can be used to find the SubByte image of a byte.

## ShiftRows

This function brinds diffusion on rows.

```math
\text {ShiftRows}(m) = \begin{bmatrix}
m_0 & m_4 & m_8 & m_{12} \\
m_5 & m_9 & m_{13}&m_1 \\
m_{10} & m_{14}&m_2 & m_6 \\
m_{15}&m_3 & m_7 & m_{11}
\end{bmatrix}
```

## MixColumns

MixColums brings confusion on the columns.

```math
\text {MixColumns}(m) =  \begin{bmatrix}
02 & 03 & 01 & 01 \\
01 & 02 & 03&01 \\
01 & 01&02 & 03 \\
03&01& 02 & 02
\end{bmatrix}.m
```

ShiftRows and MixColumns are made such that every single byte is related to all the other bytes.

Due to confusion and diffusion, AES respect the [Shannon conditions](https://www.iacr.org/museum/shannon45.html) for devising a block cipher algorithm.

## Key expansion

The key expansion or key scheduling is used to generate different keys for each round of AES. Each round key is derived from the previous round key using a series of transformations. Side channel attacks take advantage of this property to find the initial secret key. That is the reason why each round key should be keept secret.. The key expansion process ensures that each round key is unique and contributes to the overall security of the encryption process.

We denote:

- $`N`$ as the length of the key in 32-bit words
- $`K_0, K_1, ... K_{N-1}`$ as the 32-bit words of the original key
- $`R`$ as the number of round keys needed
- $`W_0, W_1, ... W_{4R-1}`$ as the 32-bit words of the expanded key

We define for $`W =  \begin{bmatrix}
B_0 & B_1 & B_2 & B_3
\end{bmatrix} `$ a 32-bits word:

- $`\text {RotWord}(W) = \begin{bmatrix}B_1 & B_2 & B_3 & B_0\end{bmatrix}`$ a one byte circular shift;
- $`\text {SubWord}(W) = \begin{bmatrix}
S(B_0) & S(B_1) & S(B_2) & S(B_3)
\end{bmatrix}`$ an SBox transformation to each of the 4 bytes of the word.
These functions bring diffusion and confusion during the key expansion.

We also need to introduce the round constants denoted $`rcon_i = \begin{bmatrix}
(rc_i)_{16} & 00_{16} & 00_{16} & 00_{16}
\end{bmatrix}`$ for $`i =1 ... Q`$. $`rcon_i`$ is a 32-bits word. 
$`rc_i`$ is computed in the Rinjdael field ($`GF(2^{8})/x^{8}+x^{4}+x^{3}+x+1)`$

```math
rc_{i}={\begin{cases}01_{16}&{\text{if }}i=1\\rc_{i-1}\ll 1&{\text{if }}i>1{\text{ and }}rc_{i-1}<80_{16}\\(rc_{i-1}\ll 1)\oplus {\text{11B}}_{16}&{\text{if }}i>1{\text{ and }}rc_{i-1}\geq 80_{16}\end{cases}}
```
rcon_i is used to mask the original bits. This is a function similar to stream encryption.

| Type    | Number of words in key (N) | Number of round keys (R) | Number of $`rc_i`$ used (Q) |
| ------- | ----------------- | ----------------- |----------------- |
| AES-128 | 4               | 11               | 10              |
| AES-192 | 6               | 13               |8               |
| AES-256 | 8               | 15               |7               |


$`W_i`$ is defined as :
```math
W_{i}={\begin{cases}K_{i}&{\text{if }}i < N\\W_{i-N}\oplus \text {SubWord} (\text {RotWord} (W_{i-1}))\oplus rcon_{i/N}&{\text{if }}i\geq N{\text{ and }}i\equiv 0{\pmod {N}}\\W_{i-N}\oplus \text {SubWord} (W_{i-1})&{\text{if }}i\geq N{\text{, }}N > 6{\text{, and }}i\equiv 4{\pmod {N}}\\W_{i-N}\oplus W_{i-1}&{\text{otherwise.}}\\\end{cases}}
```

Below we give an illustration of key scheduling for AES-256.

![alt text](/rijndael/ressources/keyscheduling.drawio.png)

# Data length
AES is a 128-bit block encryption. As a consequence, the data to be processed must be exactly 128 bits in size for one call of the AES encryption. Therefore, alternatives are necessary if one wishes to encrypt a chunk of data that is a different size from 128 bits. Fortunately, there are solutions: padding for data shorter than 128 bits, and different modes of operation for data longer than 128 bits.

## Padding
Suppose we need to encrypt the message "`DEADBEEF`" (`0x4445414442454546`). This is a 64-bit message. Without padding, we would not be able to encrypt this message, as its size is smaller than 128 bits. To make it suitable for encryption, we need to modify the message by adding arbitrary data. Adding the additional bits is called padding.

The question is how to choose the bits to add to the message. There are many ways to pad a message, and the most commonly used method for AES is [PKCS#7 padding](https://datatracker.ietf.org/doc/html/rfc5652#section-6.3).

![alt text](/rijndael/ressources/pkcs7.drawio.png)

## Mode of operation

Modes of operation are useful when we need to work with data larger than 128 bits. There are two categories of operation modes: AEAD (Authenticated Encryption with Associated Data) and non-authenticated modes of operation. A mode of operation is evaluated on the following point:
- Its capacity to resist cryptanalysis attacks.
- Its ability to be parallelize during computation.
- Its complexity.


## Non authenticated mode of operation
These mode of operation can not guarantie authenticity of the encrypted data. They are a bunch of operation of this kind see illustration below taken from [Wikipedia](https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation).
![alt text](/rijndael/ressources/aes_modes.png)
Let's point out the specificity of ECB (Electronic Code Book). This is the most natural mode of operation. In this mode, the long message to encrypt (≥ 128 bits long) is divided into multiples of 128 bits (using padding if necessary) and then encrypted independently.
Advantages:
- Easy to compute
- Decryption works the same as encryption

Drawbacks:
- Vulnerable to CPA (Chosen Plaintext Attack) due to the absence of an IV (Initialization Vector)
- Data integrity issues: no errors are detected during the decryption process, and each block is independent of the others.

## Authenticated Mode of Encryption with Associated Data (AEAD)
Theses modes of operation bring authenticity during the encryption process. 


| Mode                                   | Short Comment                                                                                                                                                                                | Known Vulnerability                                                                                                                                                          |
|---------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [AES-CCM](https://www.di.ens.fr/~fouque/pub/acns08.pdf)       | This is a rather complex encryption mode. The length of the message and associated data must be known in advance. It cannot pre-process associated data as it is processed after the message. | [Variable-Length Authentication Tags](https://csrc.nist.gov/csrc/media/projects/block-cipher-techniques/documents/bcm/comments/800-38-series-drafts/ccm/rw_ccm_comments.pdf) |
| [AES-EAX](https://en.wikipedia.org/wiki/EAX_mode)            | Designed as a replacement for AES-CCM.                                                                                                                                                       |                                                                                                                                                                            |
| [AES-GCM](https://en.wikipedia.org/wiki/Galois/Counter_Mode) | The nonce must not be reused.                                                                                                                                                                | [Forbidden Attack](https://eprint.iacr.org/2016/475.pdf)                                                                                                                     |
| [AES-GCM-SIV](https://en.wikipedia.org/wiki/AES-GCM-SIV)     | A countermeasure against nonce reuse vulnerability of AES-GCM.                                                                                                                                        |                                                                                                                                                                            |


# Impementation optimization
Most of systems worldwide are design with hardware optimization to enhance so as to accelerate the processing time of AES. These are some specific instructions called [AES-NI](https://en.wikipedia.org/wiki/AES_instruction_set) listed below.


| **Instruction**        | **Description**                                                                 |
|-------------------------|---------------------------------------------------------------------------------|
| **AESENC**             | Perform one round of an AES encryption flow                                     |
| **AESENCLAST**         | Perform the last round of an AES encryption flow                                |
| **AESDEC**             | Perform one round of an AES decryption flow                                     |
| **AESDECLAST**         | Perform the last round of an AES decryption flow                                |
| **AESKEYGENASSIST**    | Assist in AES round key generation                                       |
| **AESIMC**             | Assist in AES decryption round key generation. Applies Inverse Mix Columns to round keys. |


