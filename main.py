from cryptography.fernet import Fernet
import os
from time import sleep

def open_user():
    with open('user', 'r') as f:
        f_text = f.read().split(',')
        f.close()
    if len(f_text) > 1:
        return f_text
    else:
        return None

def write_user(content):
    with open('user', 'w') as f:
        f.write(content)
        f.close()

def append_user(content):
    with open('user', 'a') as f:
        f.write(content)
        f.close()

def new_passwd(passwd):
    key = Fernet.generate_key()
    cipher_suite = Fernet(key)
    cipher_passwd = cipher_suite.encrypt(passwd.encode())
    write_user(f'{key.decode()},{cipher_passwd.decode()},')

def decode_passwd():
    user = open_user()
    cipher_suite, passwd = Fernet(str.encode(user[0])), str.encode(user[1])
    decrypt_text = cipher_suite.decrypt(passwd)
    return decrypt_text.decode()

def encrypt_content(*args):
    user = open_user()
    cipher_suite = Fernet(str.encode(user[0]))
    encrypted_content = ''
    for arg in args:
        if arg == args[-1]:
            encrypted_content += f'{cipher_suite.encrypt(arg.encode()).decode()},'
        else:
            encrypted_content += f'{cipher_suite.encrypt(arg.encode()).decode()}:'
    return encrypted_content

def decrypt_content():
    content = open_user()
    cipher_suite, accounts = Fernet(str.encode(content[0])), content[2:-1]
    for account in accounts:
        decrypt_data = ''
        account = account.split(':')
        for data in account:
            if data == account[-1]:
                decrypt_data += f'{cipher_suite.decrypt(str.encode(data)).decode()}'
            else:
                decrypt_data += f'{cipher_suite.decrypt(str.encode(data)).decode()}\t\t'
        yield decrypt_data

def add_account(account, user, password):
    encrypted_content = encrypt_content(account, user, password)
    append_user(encrypted_content)
    print('Account added!')

def option_choice():
    os.system('cls')
    print('Choose the option below:')
    choice = input('[1] See all data\n[2] Insert new data\nYour option: ')
    if choice == '1':
        os.system('cls')
        all_data = decrypt_content()
        print('*' * 75)
        for data in all_data:
            print(data)
        print('*' * 75)
        input('Press any button to exit')
        os.system('cls')
        return None
    elif choice == '2':
        os.system('cls')
        identifier = input('Identifier: ')
        user = input('User/email: ')
        password = input('Password: ')
        add_account(identifier, user, password)
        sleep(0.5)
        option_choice()
    else:
        os.system('cls')
        print('Option not valid')
        sleep(0.5)
        os.system('cls')
        return None

def main():
    user_file = open_user()
    if user_file == None:
        os.system('cls')
        passwd = input('Insert new password: ')
        new_passwd(passwd)
        print('Password changed!')
        sleep(0.5)
        main()
    else:
        user_passwd = decode_passwd()
        os.system('cls')
        while True:
            passwd = input('Insert the password: ')
            if passwd == user_passwd:
                option = option_choice()
                if option == None:
                    break
            else:
                print('Incorrect password... try again')
                

if __name__ == '__main__':
    try:
        main()
    except:
        os.system('cls')
        pass
    