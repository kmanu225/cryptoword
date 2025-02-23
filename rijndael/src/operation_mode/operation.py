from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes


class PrimitiveMode:
    def __init__(self, key: bytes, mode: str):
        self.key = key
        self.mode = mode.upper()
        self.block_size = AES.block_size
        self.cipher = None
        self.iv = None
        self.nonce = None

        # Validate key length
        if len(self.key) not in [16, 24, 32]:
            raise ValueError("Key length must be 16, 24, or 32 bytes!")

    def encrypt(self, plaintext: bytes):
        if self.mode in ["ECB", "CBC", "CFB", "OFB", "CTR"]:
            self.cipher = AES.new(self.key, getattr(AES, f"MODE_{self.mode}"))
            if self.mode == "CTR":
                self.nonce = self.cipher.nonce
            elif self.mode in ["CBC", "CFB", "OFB"]:
                self.iv = self.cipher.iv
        else:
            raise ValueError("Unsupported mode!")

        ciphertext = self.cipher.encrypt(pad(plaintext, self.block_size))
        return ciphertext

    def decrypt(self, ciphertext: bytes):
        if self.mode in ["CBC", "CFB", "OFB"]:
            if self.iv is None:
                raise ValueError("IV is required for decryption in this mode!")
            self.cipher = AES.new(
                self.key, getattr(AES, f"MODE_{self.mode}"), iv=self.iv
            )
        elif self.mode == "ECB":
            self.cipher = AES.new(self.key, AES.MODE_ECB)
        elif self.mode == "CTR":
            if self.nonce is None:
                raise ValueError("Nonce is required for decryption in CTR mode!")
            self.cipher = AES.new(self.key, AES.MODE_CTR, nonce=self.nonce)
        else:
            raise ValueError("Unsupported mode!")

        plaintext = unpad(self.cipher.decrypt(ciphertext), self.block_size)
        return plaintext


class AEADMode:
    def __init__(self, key: bytes, mode: str):
        self.key = key
        self.mode = mode.upper()
        self.nonce = None

        # Validate key length
        if len(self.key) not in [16, 24, 32]:
            raise ValueError("Key length must be 16, 24, or 32 bytes!")

    def encrypt(self, plaintext: bytes, associated_data: bytes = None):
        # Initialize cipher
        if self.mode in ["CCM", "EAX", "GCM", "SIV"]:
            if self.mode != "SIV" :
                self.cipher = AES.new(self.key, getattr(AES, f"MODE_{self.mode}"))
                self.nonce = self.cipher.nonce
            else: 
                self.nonce = get_random_bytes(16)
                self.key = self.key+self.key # Key length must be twice the required length for the cipher block (32bytes for AES-128)
                self.cipher = AES.new(self.key, getattr(AES, f"MODE_{self.mode}"), nonce=self.nonce)
                
        else:
            raise ValueError("Unsupported AEAD mode!")

        if associated_data:
            self.cipher.update(associated_data)

        ciphertext, tag = self.cipher.encrypt_and_digest(plaintext)
        return ciphertext, tag

    def decrypt(self, ciphertext: bytes, tag: bytes, associated_data: bytes = None):
        if self.mode in ["CCM", "EAX", "GCM", "SIV"]:
            self.cipher = AES.new(
                self.key, getattr(AES, f"MODE_{self.mode}"), nonce=self.nonce
            )
        else:
            raise ValueError("Unsupported AEAD mode!")

        if associated_data:
            self.cipher.update(associated_data)

        try:
            plaintext = self.cipher.decrypt_and_verify(ciphertext, tag)
            return plaintext
        except ValueError:
            raise ValueError("Key incorrect or message corrupted!")


