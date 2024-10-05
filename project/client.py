import socket
import threading
import sys
#ensures user enters the correct number of system arguments
if len(sys.argv) != 3:
    print("Usage: python3 chatclient.py <host> <port>")
    sys.exit()
#initializes host and port to the system arguments provided by user    
host = str(sys.argv[1])
port = int(sys.argv[2])

#creates client socket and connects to chat server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))

#method for receiving messages from the chat server.
def receive():
    while True:
        try:
            message = client.recv(2048).decode('ascii')
            if message == 'close':
                client.close()
                break
            else:
                print(message)
        except:
            print("An error occured")
            client.close()
            break

#method for sending messages to the chat server, waits for user input and then sends to server.        
def send():
    while True:
        message = f'{input("")}'
        if message == "QUIT":
            client.send(message.encode('ascii'))
            break
        else:
            client.send(message.encode('ascii'))
            
#starts threads for incoming and outgoing messages           
receive_thread = threading.Thread(target=receive)
receive_thread.start()
send_thread = threading.Thread(target=send)
send_thread.start()