import socket
import subprocess
from functions.useful_functions import useful_functions
import datetime
import json

def input_validation(input):
    alphabet = [" ", "-", ",", "=", "'", '*', '@', ":", "$", ".", ")", "("] #list of allowed characters
    for x in range(48, 58): #numbers
        alphabet.append(chr(x))
    for x in range(65, 91): #uppercase
        alphabet.append(chr(x))
    for x in range(97, 123): #lowercase
        alphabet.append(chr(x))
    cleaned_string = ''
    if len(input) > 500:
       cleaned_string = "echo Too long"
    elif input[0] == chr(32):
        cleaned_string = "echo Don't start with a space"
    else:
        for char in input:
            if char in alphabet:
                cleaned_string += char
    return(cleaned_string)

def get_all_recv_data(conn):
    final_data = bytearray()

    while True:
            print(f'json server {datetime.datetime.now()} While step')
            data = conn.recv(buffer_size)
            if not data or "Finished sending" in data.decode():
                print(f'json server {datetime.datetime.now()} No data received, closing connection')
                break
            final_data.extend(data)
    return final_data


def execute_command(command: str):
    result = subprocess.run(['powershell', str(command)], capture_output=True, text=True)
    print("json server ")
    print(result.stdout)
    return result.stdout

ip = 'localhost'
port = 9998
buffer_size = 6000
secret_key = 1234
encrypter = useful_functions()

while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((ip, port))
        print(f'json server {datetime.datetime.now()} binding step')
        server_socket.listen()
        print(f'json server {datetime.datetime.now()} listen step')
        
        conn, addr = server_socket.accept()
        print(f'json server {datetime.datetime.now()} Connected by {addr}')

        with conn:
           
           final_data = get_all_recv_data(conn)
           
           decoded_message = encrypter.shiftstring(final_data.decode(), direction="backward")
           if str(secret_key) in decoded_message:   
                print("json server ")
                print(decoded_message)
                message_dict = json.loads(decoded_message)
                command = message_dict.get("command", {}).get("command", "")
                print(f'json server {datetime.datetime.now()} Received command: {command}')

                response_dict = {
                    "response": command,
                }
                print("json server ")
                print(response_dict)
                response_json = json.dumps(response_dict)
                encoded_message = encrypter.shiftstring(response_json)
                print(f'json server {datetime.datetime.now()} Response sent')

                if 'Kerberos' not in command:
                    command = input_validation(command)
                
                result = execute_command(command)
                print("json server", len(result), result)
                if result != "":
                    conn.sendall(result.encode())
                    print('json server Command execution result sent')
                else:
                    conn.sendall("error".encode())
                    print('json server error sent')
           else:
                print("json server Secret key does not match")
                print(ip, addr)