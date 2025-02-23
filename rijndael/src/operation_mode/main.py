from operation import *

    
if __name__ == "__main__":
    AES256_KEY = b'rijndaelrijndaelrijndaelrijndael'
    AES192_KEY = b'rijndaelrijndaelrijndael'
    AES128_KEY = b'rijndaelrijndael'
    KEYS = [AES128_KEY, AES192_KEY, AES256_KEY]
    
    PLAINTEXT = b"crypto{AES}"
    
    for key in KEYS:
        try:
            Primitive_Mode = ["ECB", "CBC", "CFB", "OFB", "CTR"]
            for mode in Primitive_Mode:
                # Example: AES-256 in CBC mode
                aes = PrimitiveMode(key, mode)
                ciphertext = aes.encrypt(PLAINTEXT)
                print(f"AES-{len(key*8)}-{mode} Ciphertext: {ciphertext}")

                decrypted_text = aes.decrypt(ciphertext)
                assert decrypted_text == PLAINTEXT

            AEAD = ["CCM", "EAX", "GCM", "SIV"]
            associated_data = b"Associated data"
            for mode in AEAD:
                aes = AEADMode(key, mode)
                ciphertext, tag = aes.encrypt(PLAINTEXT, associated_data)
                print(f"AES-{len(key*8)}-{mode} Ciphertext: {ciphertext}, Tag: {tag}")

                decrypted_text = aes.decrypt(ciphertext, tag, associated_data)
                assert decrypted_text == PLAINTEXT
        except Exception as e:
            print(f"Error: {e}")
