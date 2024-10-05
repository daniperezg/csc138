import threading
import socket
import sys

#check that user has entered the correct number of system arguments
if len(sys.argv) != 2:
    print("Usage: python3 chatserver.py <port>")
    sys.exit()

#declare host and port variables    
host = 'ecs-coding3.csus.edu'
port = int(sys.argv[1])

#create the server socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#bind server to host and user provided port and start listening on provided port
server.bind((host, port))
server.listen()

#create lists to hold active user's client information and usernames
clients= []
usernames = []

#broadcast method to send messgaes to all registered users
def broadcast(message):
    for client in clients:
        client.send(message)

#handle method for receiving client messages        
def handle(client):
    #start continous loop to receive messages from client
    while True:
        try:
            #receive message from client and depending on command execute if statements
            message = client.recv(2048).decode('ascii')
            #handles join requests from clients
            if message.startswith("JOIN"):
                #limits number of registered users to 10 at once
                if len(usernames) == 10:
                    #if chat is full sends client message and then closes connection
                    client.send("Sorry the chat is full, please try later".encode('ascii'))
                    client.send("close".encode('ascii'))
                    client.close()
                #checks that username is not already in use by another user
                else:
                    username = message.split(" ")[1]
                    if username in usernames:
                        client.send("That username is already taken. Enter JOIN followed by username: ".encode('ascii'))
                    else:
                        usernames.append(username)
                        clients.append(client)
                        print(f'{username} joined the chat!')
                        broadcast(f'SERVER: {username} joined the chat!'.encode('ascii'))
            #handles user broadcast message request
            elif message.startswith("BCST"):
                index = clients.index(client)
                username = usernames[index]
                broadcast(f'{username}: {message}'.encode('ascii'))
            #handles user private message request
            elif message.startswith("MESG"):
                index = clients.index(client)
                username = usernames[index]
                recipient = message.split(" ")[1]
                #check to ensure that the recipient of the message is a valid registered user
                if recipient not in usernames:
                    client.send("There is no user by that name. Please use MESG followed by a valid username.".encode('ascii'))
                else:
                    recipient_index = usernames.index(recipient)
                    send_to = clients[recipient_index]
                    send_to.send(f'{username}: {message}'.encode('ascii'))
            #handles user request for the list of currently registered users
            elif message.startswith("LIST"):
                active_users = ", ".join(usernames)
                client.send(f'Online: {active_users}'.encode('ascii'))
            #handles user quitting the chat. Closes connection to user and terminates their thread
            elif message.startswith("QUIT"):
                index = clients.index(client)
                clients.remove(client)
                client.send("close".encode('ascii'))
                client.close()
                username = usernames[index]
                print(f'{username} has left the chat')
                broadcast(f'{username} has left the chat'.encode('ascii'))
                usernames.remove(username)
                break
            #if user sends an invalid request to the server sends error message and list of valid requests
            else:
                client.send("SERVER: Unrecognized input, please use BCST, MESG, LIST or QUIT".encode('ascii'))
        #if their is an error with a client closes connection and removes them from the active users lists
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            username = usernames[index]
            print(f'{username} has left the chat')
            broadcast(f'{username} has left the chat'.encode('ascii'))
            usernames.remove(username)
            break

#method to handle client connections. When clients connect to server starts a thread for their connection            
def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with ({address})")
        client.send("Enter JOIN followed by your username: JOIN username".encode('ascii'))
        thread = threading.Thread(target = handle, args = (client, ))
        thread.start()

#prints port server is listening on and calls receive method to start handling client connections.        
print(f"Server is listening on {port}")
receive()
                
                