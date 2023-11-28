# PASSGEN
Easily manager your passwords with passgen

By using a name based short-cut for passwords, you can easily access your password that is stored in an encrypted file that cannot easily be unlocked.

The design of this manager is simple:

#### 1. Generate a strong password: use random letters, numbers, and punctuation with a total length of 20 characters.

#### 2. Quickly fetch passwords: let's use a dictionary with a name as a key for the passwords.

#### 3. Store the passwords in a file: let's format the dictionary into JSON structure.

#### 4. Keep the store JSON file a secret: let's encrypt the file using the `cryptography` library

This is the base design of this manager, however, I also wanted to make it instant in adding passwords so if the name you use is not found, I quickly generate a new password.
I also wanted to make it easy to use the password that you just created or fetched, so I paste the password to your clipboard for instant use.

Now, we can quickly generate, access, and use our passwords.






### If you wish to run this project across your machine in terminal, follow the link below


<a href="https://dbader.org/blog/how-to-make-command-line-commands-with-python" target="_blank">How to make command line commands with Python</a>

Also, on the last step from the link above, ensure that you input the path into the file that is run at the start of your terminal. Or do `source [file you wish to run]` which should run that file at the beginning of a terminal session.
