import socket
import datetime
import json
from functions.useful_functions import useful_functions

def send_encrypted_command(command_text, ip='localhost', port=9998, secret_key=1234, buffer_size=1000):
    encrypter = useful_functions()
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((ip, port))
        print(f'{datetime.datetime.now()} connected')

        powershell_command = {'secret key': secret_key, 'command': str(command_text)}
        
        message_json = json.dumps({"command": powershell_command})
        print(message_json)
        
        encrypted_message = encrypter.shiftstring(message_json)
        
        for i in range(0, len(encrypted_message), buffer_size):
            chunk = encrypted_message[i:i + buffer_size]
            unscrambled = encrypter.shiftstring(chunk, direction="backward")
            print(unscrambled)
            print(f"{datetime.datetime.now()} Message: {unscrambled}")
            
            client.sendall(chunk.encode('utf-8'))

        print("jsonclient Finished sending and receiving data")
        client.sendall("Finished sending".encode())
        result = bytearray()
        while True:
            
            tempincomingdata = client.recv(buffer_size)
            result.extend(tempincomingdata)
            print('jsonclient data incoming chunk')
            print(len(result), len(tempincomingdata), tempincomingdata.decode())
            print('result printed')
            if not tempincomingdata:
                print('socket broke')
                break
        print(result.decode())
    return (result.decode())
