from Crypto.Util.number import long_to_bytes


def SP800_108_Double_Pipeline(
    k_in, key_len, prf, num_keys=None, label=b"", context=b"", with_counter=True
):
    """Derive one or more keys from a k_in secret using
    a pseudorandom function in Counter Mode, as specified in
    `NIST SP 800-108r1 <https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-108r1.pdf>`_.

    Args:
     k_in (byte string):
        The secret value used by the KDF to derive the other keys.
        It must not be a password.
        The length on the secret must be consistent with the input expected by
        the :data:`prf` function.
     key_len (integer):
        The length in bytes of each derived key.
     prf (function):
        A pseudorandom function that takes two byte strings as parameters:
        the secret and an input. It returns another byte string.
     num_keys (integer):
        The number of keys to derive. Every key is :data:`key_len` bytes long.
        By default, only 1 key is derived.
     label (byte string):
        Optional description of the purpose of the derived keys.
        It must not contain zero bytes.
     context (byte string):
        Optional information pertaining to
        the protocol that uses the keys, such as the identity of the
        participants, nonces, session IDs, etc.
        It must not contain zero bytes.

    Return:
        - a byte string (if ``num_keys`` is not specified), or
        - a tuple of byte strings (if ``num_key`` is specified).
    """

    if num_keys is None:
        num_keys = 1

    if context.find(b"\x00") != -1:
        raise ValueError("Null byte found in context")

    output_len = key_len * num_keys
    output_len_encoding = long_to_bytes(output_len * 8, 4)

    i = 1
    fixed_input_data = label + b"\x00" + context + output_len_encoding
    keys = []
    a_i = fixed_input_data
    while len(keys) < num_keys:
        a_i = prf(
            k_in, a_i
        )  # A(0) = PRF(K,|| Label || 0x00 || Context || [output length]) Firt pipeline
        info = a_i + (long_to_bytes(i, 4) * with_counter) + fixed_input_data
        keys.append(
            prf(k_in, info)
        )  # K(i) = PRF(K, A(i) || {[i]} || Label || 0x00 || Context || [output length]) Second pipeline
        i += 1
        if i > 0xFFFFFFFF:
            raise ValueError("Overflow in SP800 108 double pipeline mode")

    return keys


if __name__ == "__main__":
    from Crypto.Hash import HMAC, SHA256

    def prf(key, msg):
        return HMAC.new(key, msg, SHA256).digest()

    k_in = b"this is a key123"
    label = b"label"
    context = b"context"
    key_len = 16

    # Derive a single key
    key = SP800_108_Double_Pipeline(k_in, key_len, prf, label=label, context=context)
    print("Key:", key[0].hex())

    # Derive multiple keys
    keys = SP800_108_Double_Pipeline(
        k_in, key_len, prf, num_keys=3, label=label, context=context
    )
    for idx, k in enumerate(keys):
        print(f"Key {idx+1}:", k.hex())
