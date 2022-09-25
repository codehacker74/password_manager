#!/usr/bin/env python3


# Author: Andrew Masters

# Description: Easily create and retrieve passwords using this password generator


import argparse
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
    pw = pw_dict.get(name, '')
    return pw

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

# Remove a password from the encrypted file and
def passgen_remove_name(name):
    enc_passwords = Path('enc_passwords.txt')
    if enc_passwords.exists():
        pw_dict = decrypt_file()
    else:
        print("There are no passwords to delete.")
        return
    if pw_dict.get(name, '') == '':
        print(f'Password for {name} could not be deleted because it does not exist.')
        return

    del pw_dict[name]
    new_file = Path('temp_pws.txt')
    with open(new_file, 'w') as raw_file:
        raw_file.write(json.dumps(pw_dict))
    encrypt_file(new_file)
    print(f'Password for {name} has been deleted.')

# Fetch all names from the encrypted file
def fetch_names():
    encryption_file = Path('enc_passwords.txt')
    if not encryption_file.exists():
        print('Could not retrieve encrypted password file.')
        return
    pw_dict = decrypt_file()
    keys = pw_dict.keys()
    for key in keys:
        print(key)

def fetch_names_with_passwords():
    encryption_file = Path('enc_passwords.txt')
    if not encryption_file.exists():
        print('Could not retrieve encrypted password file.')
        return
    pw_dict = decrypt_file()
    keys = pw_dict.keys()
    for key, value in pw_dict.items():
        print(key, ' -> ', value)

def main():
    parser=argparse.ArgumentParser(description='Parse out the name.')
    parser.add_argument("-add_password", help="name associated with password", type=str)
    parser.add_argument("-show_names", nargs='?', const=True, help="view all names", type=bool)
    parser.add_argument("-show_passwords", nargs='?', const=True, help="show all passwords with their associated name", type=bool)
    parser.add_argument("-remove_password", help="remove the password of the given name", type=str)

    args = parser.parse_args()

    # Ensure that the name variable is not null
    if args.add_password is not None:
        passgen(args.name)

    if args.remove_password is not None:
        passgen_remove_name(args.remove_password)

    # Fetch all the password names if requested
    if args.show_names:
        fetch_names()

    # Fetch all names with their passwords
    if args.show_passwords:
        fetch_names_with_passwords()


if __name__=="__main__":
    main()
