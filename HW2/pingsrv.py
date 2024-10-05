###################################################
#      Daniela Perez 
#      138-04
#      Date: 03/07/2024
#      Description: server will set up a UDP socket on the Internet (i.e., INET) domain and then wait
#      in an infinite loop listening for incoming UDP packets
#      Usage: python3 pingsrv.py <port number>
###################################################

from socket import *
import sys 
import random 

if len(sys.argv) != 2:
    print("Usage: python pingsvr.py <port>")
    sys.exit(1)
    
# You can take the port information of the provided argument and convert the string into integer
port = int(sys.argv[1])

#Declare the socket descriptor for UDP 
serverSocket = socket(AF_INET, SOCK_DGRAM)

# Binding the port and the IP address of the host 
serverSocket.bind(("0.0.0.0", port))

print('Server listening on port', port)

while True:
    #create random 
    rand_num = random.randint(0,10)

    # Receive the client packet along with the address it is coming from
    message, address = serverSocket.recvfrom(2048)

    # create 30% packet loss
    if rand_num < 4:
        modified_message = "Packet loss - Message dropped."
        print(modified_message)
        continue
    else:
        modified_message = "Recieved from"
        serverSocket.sendto(modified_message.encode(), address)
        print(f"Received from {address}: {message.decode()}")