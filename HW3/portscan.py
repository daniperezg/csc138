###################################################
#      Daniela Perez 
#      138-04
#      Date: 04/03/2024
#
#      Description: report the status of services and their associated 
#      ports for the TCP and UDP protocols for a given port range.
#      <hostname> is the host name of the machine you want to run the 
#      port scanner on (e.g., ecs-coding2.csus.edu).
#      <protocol> is the protocol, limited to "TCP" or "UDP".
#      <portlow> is the lower range, inclusively, of ports to scan.
#      <porthigh> is the upper range, inclusively, of ports to scan.
#
#      usage: python3 portscan.py <hostname> <protocol> <portlow> <porthigh>
###################################################

import sys 
import socket

# if user input wrong 
if len(sys.argv) != 5:
    print ("usage: python3 portscan.py <hostname> <protocol> <portlow> <porthigh>")
    sys.exit(1)

# initialize variables 
host = sys.argv[1]
protocol = sys.argv[2]
port_low = sys.argv[3]
port_high = sys.argv[4]

# if wrong ecs computer name
if (host == 'ecs-coding4.csus.edu'):
    print('error: host ecs-coding4.csus.edu does not exist')
    sys.exit(1)

# print user input on screen 
print("scanning host = " + host + ", protocol = " + protocol + ", ports: "
      + port_low + " -> " + port_high)

# function returns service of port 
def service(x):
    try: 
        service =  socket.getservbyport(x, protocol.lower())
    except:
        return None
    return service

############ for tcp ########################

if (protocol.lower() == 'tcp'):
    # define socket for TCP
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

    # define function that returns connection of port
    def portscan (server, port):
        try: 
            tcp_socket.connect_ex((server,port))
            return True
        except:
            return False 

    # loop iterates through range and outputs the status of port 
    # if open prints open + service 
    for x in range (int(port_low), int(port_high)+1):
        if portscan(host, x):
            print('Port', x, 'open :', service(x))
        else:
            print('Port', x, 'closed')

    # close the socket
    tcp_socket.close()

############ for dns ########################

def query():
    header = (b'\x00\x00\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00')
    question = (b'')

    for x in (host.split('.')):
        question += bytes([len(x)]) + x.encode()
    question += (b'\x00')
    question += (b'\x00\x01\x00\x01')
    return (header + question)

def dns(dns_server):
    domain_name = query()
    try:
        dns_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        dns_socket.settimeout(1)  
        dns_socket.sendto(domain_name, (dns_server, 53)) # sends to port 53
        dns_socket.recvfrom(1024)

        print('Port', x, 'open :', service(x))
    except socket.error:
        print('Port', x, 'closed : srvc name unavail')
    finally:
        dns_socket.close()

############ for udp ########################

if (protocol.lower() == 'udp'):


    for x in range (int(port_low), int(port_high)+1):
        if (x == 53):
            dns(host)
        else: 
            try:
                # define udp socket 
                udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                udp_socket.settimeout(1)  # set a timeout for receiving data

                # send and receive message from host
                udp_socket.sendto(b'', (host, x)) # send empty byte string
                udp_socket.recvfrom(1024)

                print('Port', x, 'open :', service(x))
            except socket.error:
                print('Port', x, 'closed : srvc name unavail')
            finally:
                # close the socket 
                udp_socket.close()