from passlib.hash import msdcc


secret = "password"
username = "Administrator"

print(msdcc.raw(secret, username).hex())
