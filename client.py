import socket  # Provides low-level networking interface
import struct  # Provides functions to interpret strings as packed binary data

# Read client configurations
with open('client.in', 'r') as f:
    SERVER_IP = f.readline().strip()  # Reads the server IP address
    SERVER_PORT = int(f.readline().strip())  # Reads the server port number
    CLIENT_PORT = int(f.readline().strip())  # Reads the client port number
    FILENAME = f.readline().strip()  # Reads the name of the file to be requested
    WINDOW_SIZE = int(f.readline().strip())  # Reads the window size for the protocol

def compute_checksum(data):
    if len(data) % 2 == 1:
        data += b'\0'  # Pads data with a null byte if its length is odd
    checksum = 0
    for i in range(0, len(data), 2):
        word = data[i] + (data[i+1] << 8)  # Combines two bytes into one word
        checksum += word
        checksum = (checksum & 0xffff) + (checksum >> 16)  # Adds overflow bits to checksum
    return ~checksum & 0xffff  # Returns one's complement of the checksum

class Client:
    def __init__(self, server_ip, server_port, client_port):
        self.server_ip = server_ip  # Initializes the server IP address
        self.server_port = server_port  # Initializes the server port number
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Creates a UDP socket
        self.client_socket.bind(('', client_port))  # Binds the socket to the client port

    def request_file(self, filename):
        try:
            self.client_socket.sendto(filename.encode('utf-8'), (self.server_ip, self.server_port))  # Sends the file request to the server
            print(f"Requested file {filename} from server {self.server_ip}:{self.server_port}")
            self.receive_file()  # Calls the method to receive the file
        except Exception as e:
            print(f"An error occurred while requesting the file: {e}")  # Prints any errors that occur during the request

    def receive_file(self):
        try:
            while True:
                packet, addr = self.client_socket.recvfrom(1024)  # Receives a packet from the server
                if packet:
                    header = packet[:6]  # Extracts the header from the packet
                    seq_num, checksum = struct.unpack('!I H', header)  # Unpacks the sequence number and checksum from the header
                    data = packet[6:]  # Extracts the data from the packet
                    print(f"Received packet {seq_num} from {addr} with checksum {checksum}")
                    if compute_checksum(header[:4] + data) == checksum:  # Verifies the checksum
                        print(f"Checksum verified for packet {seq_num}")
                    else:
                        print(f"Checksum mismatch for packet {seq_num}. Expected {checksum}, calculated {compute_checksum(header[:4] + data)}")
                        # Here you would request retransmission if needed
        except Exception as e:
            print(f"An error occurred while receiving the file: {e}")  # Prints any errors that occur during the reception

if __name__ == "__main__":
    client = Client(SERVER_IP, SERVER_PORT, CLIENT_PORT)  # Creates a Client object with the specified server and client ports
    client.request_file(FILENAME)  # Requests the specified file from the server
