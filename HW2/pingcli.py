###################################################
#      Daniela Perez 
#      138-04
#      Date: 03/07/2024
#      Description: server will set up a UDP socket on the Internet (i.e., INET) domain and then wait
#      in an infinite loop listening for incoming UDP packets
#      Usage: python3 pingcli.py <server name> <port>
###################################################

import sys
from time import time as current_time
from socket import socket, AF_INET, SOCK_DGRAM, timeout
from socket import *

def send_ping_requests(server, port_number):
    
    # initializing variables
    round_trip_times = []
    total_received = 0
    total_sent = 0

    ping_socket = socket(AF_INET, SOCK_DGRAM)
    ping_socket.settimeout(1)   # timeout for 1 sec

    for attempt in range(10):
        total_sent += 1     # increment 
        ping_message = f"PING {attempt+1}"
        start_time = current_time()
        ping_socket.sendto(ping_message.encode(), (server, port_number))

        try:
            stop_time = current_time()
            rtt_ms = 1000 * (stop_time - start_time)
            round_trip_times.append(rtt_ms)   # add rtt to array
            reply, address = ping_socket.recvfrom(2048)
            total_received += 1
            print(f"Recieved from {address}: {reply.decode()} RTT: {rtt_ms:.2f} ms")

        except timeout:
            print(f"Request timed out for {ping_message}")

    # close
    ping_socket.close()

    missed_packets = (total_sent - total_received)
    packet_loss = 100 * ((total_sent - total_received) / total_sent)

    if round_trip_times:
        # used to calculate stats
        min_rtt = min(round_trip_times)
        average_rtt = sum(round_trip_times) / len(round_trip_times)
        max_rtt = max(round_trip_times)

        # ping stats (using .2f for percision)
        print(f"\n Ping Statistics:")
        print(f"   Packets: Sent = {total_sent}, Received = {total_received}, Lost = {missed_packets} ({packet_loss:.2f}% loss)")
       
       # rtt stats
        print(f"\n RTT Statistics:")
        print(f"   RTT: Minimum RTT: {min_rtt:.2f} ms, Maximum RTT: {max_rtt:.2f} ms, Average RTT: {average_rtt:.2f} ms")
    else:
        print("No responses received.")


# calling main()
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 script.py <host> <port>")
        sys.exit(1)
    
    # taking arguments
    server_port = int(sys.argv[2])
    server_host = sys.argv[1]
    send_ping_requests(server_host, server_port)