from Crypto.Util.number import long_to_bytes


def SP800_108_Feedback(
    k_in, key_len, prf, num_keys=None, label=b"", context=b"", iv=b"", with_counter=True
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
     iv (byte string):
        Optional initialization vector.

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
    k_input = iv
    while len(keys) < num_keys:
        info = k_input + (long_to_bytes(i, 4) * with_counter) + fixed_input_data
        k_input = prf(k_in, info)
        keys.append(k_input)
        i += 1
        if i > 0xFFFFFFFF:
            raise ValueError("Overflow in SP800 108 feedback mode")

    return keys


if __name__ == "__main__":
    from Crypto.Hash import HMAC, SHA256

    def prf(key, msg):
        return HMAC.new(key, msg, SHA256).digest()

    k_in = b"this is a key124"
    label = b"label"
    context = b"context"
    key_len = 16
    dk1, dk2 = SP800_108_Feedback(
        k_in, key_len, prf, num_keys=2, label=label, context=context
    )
    print("Derived key 1:", dk1.hex())
    print("Derived key 2:", dk2.hex())

    dk3, dk4 = SP800_108_Feedback(
        k_in, key_len, prf, num_keys=2, label=label, context=context, with_counter=False
    )
    print("Derived key 3:", dk3.hex())
    print("Derived key 4:", dk4.hex())

    
