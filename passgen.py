# Track passwords with

# Step 1: Generate a random password with the given function
# Step 2: Store the password within a file that we will encrypt
# Step 3: The file should be in JSON format so that we can read
#           it as a dictionary.

import sys
import string
import secrets
import json
import os
import pyperclip
from pathlib import Path
from cryptography.fernet import Fernet

# Generates a random password of letters and numbers
def generate_password():
    length = 20
    alphabet = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(alphabet) for i in range(length))
    return password

# Generate an encryption key in order to encrypt our password file
def get_encryption_key():
    key_file = Path('my_password_encryption_key.key')
    if not key_file.exists():
        key = Fernet.generate_key()
        with open(key_file, 'wb') as mykey:
            mykey.write(key)
        return key
    else:
        with open(key_file, 'r') as mykey:
            return mykey.read()

# encrypt the password file and then delete it
def encrypt_file(file):
    f = Fernet(get_encryption_key())
    with open(file, 'rb') as original_file:
        original = original_file.read()

    encrypted = f.encrypt(original)

    with open('enc_passwords.txt', 'wb') as encrypted_file:
        encrypted_file.write(encrypted)

    os.remove(file)

# Decrypt file and return dictionary of names and passwords
def decrypt_file():
    f = Fernet(get_encryption_key())
    with open('enc_passwords.txt', 'rb') as encrypted_file:
        encrypted = encrypted_file.read()

    decrypted = f.decrypt(encrypted)
    pw_dict = json.loads(decrypted)
    return pw_dict

# Fetch the password for the name given
def fetch_password_for_name(name):
    encryption_file = Path('enc_passwords.txt')
    if not encryption_file.exists():
        return ''
    pw_dict = decrypt_file()
    pw = pw_dict[name]
    return pw

# Checks if the file exists and adds the given nick name and pw if not
def check_if_pw_file_exists(nick_name, password):
    enc_passwords = Path('enc_passwords.txt')
    if not enc_passwords.exists():
        pw_dict = {nick_name : password}
        with open(enc_passwords, 'w') as file:
            file.write(json.dumps(pw_dict))
    else:
        f = Fernet(key)

# Requests a name for the password that matches to it
def add_password_with_name(name):
    enc_passwords = Path('enc_passwords.txt')
    if enc_passwords.exists():
        pw_dict = decrypt_file()
        pw_dict[name] = generate_password()
    else:
        pw_dict = {name : generate_password()}
    print(f'New password generated for {name}')
    new_file = Path('temp_pws.txt')
    with open(new_file, 'w') as raw_file:
        raw_file.write(json.dumps(pw_dict))
    encrypt_file(new_file)


# Main program starter for this file
def passgen(name):
    #name = input('pw name: ')
    pw = fetch_password_for_name(name)
    if pw == '':
        print(f'Password for {name} does not exist, generating new password!')
        add_password_with_name(name)
        pw = fetch_password_for_name(name)
    else:
        print("Password found")
    print('Password copied to clipboard.')
    pyperclip.copy(pw)

name = input("name of password: ")
passgen(name)
