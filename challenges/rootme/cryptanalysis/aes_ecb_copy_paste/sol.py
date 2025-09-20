from pwn import *

# -------------------------------
# Define menu commands for the service
# -------------------------------
LOGIN_CMD = b'1'  # Option to log in
REGISTER_CMD = b'2'  # Option to register a new account
QUIT_CMD = b'3'  # Option to quit

# -------------------------------
# AES block / padding info
# -------------------------------
PADDING_LEN = 16          # AES block size in bytes
# Each byte is represented by 2 hex digits in hex strings
HEX_PADDING_LEN = PADDING_LEN * 2

# -------------------------------
# Define the target "admin" JSON we want after decryption
# -------------------------------
crafted_admin_json = b'{"username": "admin", "isAdmin": true, "fakeKey": "myFakeEntry"}'
len_crafted_admin_json = len(crafted_admin_json)
# For hex tokens, each byte is represented by 2 hex digits
hex_len_crafted_admin_json = len_crafted_admin_json * 2

# -------------------------------
# Craft a username to align "isAdmin": true in a ciphertext block
# This is critical for the AES-ECB cut-and-paste attack
# -------------------------------
my_username = b'admin", "isAdmin": true, "fakeKey": "myFakeEntry"}padpadpadpad'

# -------------------------------
# Connect to the remote challenge service
# -------------------------------
conn = remote('challenge01.root-me.org', 51060)

# -------------------------------
# Read initial server banner/menu
# -------------------------------
data = conn.recv(4096, timeout=1)
# print banner and the chosen option
print(data.decode(), REGISTER_CMD.decode())

# -------------------------------
# Register the "admin-like" account
# -------------------------------
conn.sendline(REGISTER_CMD)  # send "2" to select Register option

# Receive prompt for username
data = conn.recv(4096, timeout=1)
print(data.decode(), my_username)

# Send crafted username
conn.sendline(my_username)

# Receive server response containing the token
data = conn.recv(4096, timeout=1)
print(data.decode())

# -------------------------------
# Extract the token returned by the server
# -------------------------------
# The server typically responds like: "Token: <hex_string>\n"
my_token = data.split(b': ')[1].split(b'\n')[0]

# -------------------------------
# Craft the admin token by combining blocks
# -------------------------------
# - Take the first part corresponding to the JSON we want (hex_len_crafted_admin_json)
# - Take the last block (padding) to ensure valid PKCS#7 padding
crafted_admin_token = my_token[:hex_len_crafted_admin_json] + \
    my_token[-HEX_PADDING_LEN:]
# print("crafted token:", crafted_admin_token)  # Optional: debug

# -------------------------------
# Log in using the crafted token
# -------------------------------
conn.sendline(LOGIN_CMD)  # send "1" to select Login option

# Read server prompt for token input
print(conn.recv(4096, timeout=1).decode(), crafted_admin_token.decode())

# Send crafted token to attempt admin login
conn.sendline(crafted_admin_token)

# Receive server response (hopefully contains the flag)
data = conn.recv(4096, timeout=1)
print(data.decode())
FLAG = data.split(b": ")[1].split(b"\n")[0]


# -------------------------------
# Quit the service
# -------------------------------
conn.sendline(QUIT_CMD)
data = conn.recv(4096, timeout=1)
print(data.decode())

# Close connection
conn.close()


print("""
# -------------------------------
# FLAFG EXTRACTION COMPLETE
# -------------------------------\n""", "\n", FLAG, "\n", """
# -------------------------------
# VERIFICATION STEPS (not part of exploit)
# -------------------------------
# """)
