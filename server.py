import socket  # Provides low-level networking interface
import threading  # Allows for concurrent operations
import random  # Implements pseudo-random number generators for various distributions
import time  # Provides various time-related functions
import os  # Provides a way of using operating system dependent functionality
import struct  # Provides functions to interpret strings as packed binary data

# Read server configurations
with open('server.in', 'r') as f:
    SERVER_PORT = int(f.readline().strip())  # Reads the server port number
    WINDOW_SIZE = int(f.readline().strip())  # Reads the window size for the protocol
    RANDOM_SEED = int(f.readline().strip())  # Reads the seed for random number generation
    PACKET_LOSS_PROBABILITY = float(f.readline().strip())  # Reads the probability of packet loss

random.seed(RANDOM_SEED)  # Sets the seed for random number generation

def simulate_packet_loss():
    return random.random() < PACKET_LOSS_PROBABILITY  # Returns True if a packet should be lost based on probability

def compute_checksum(data):
    if len(data) % 2 == 1:
        data += b'\0'  # Pads data with a null byte if its length is odd
    checksum = 0
    for i in range(0, len(data), 2):
        word = data[i] + (data[i+1] << 8)  # Combines two bytes into one word
        checksum += word
        checksum = (checksum & 0xffff) + (checksum >> 16)  # Adds overflow bits to checksum
    return ~checksum & 0xffff  # Returns one's complement of the checksum

class Server:
    def __init__(self, port):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Creates a UDP socket
        self.server_socket.bind(('', port))  # Binds the socket to the specified port
        self.window = {}  # Initializes an empty dictionary to manage sliding window
        self.lock = threading.Lock()  # Creates a lock for thread synchronization

    def handle_client(self, addr, filename):
        file_path = os.path.join(os.getcwd(), filename)  # Constructs the absolute path of the file
        try:
            with open(file_path, 'rb') as f:
                seq_num = 0
                while True:
                    data = f.read(512)  # Reads up to 512 bytes from the file
                    if not data:
                        break  # Exits the loop if end of file is reached

                    packet = self.create_packet(seq_num, data)  # Creates a packet with sequence number and data
                    self.send_packet(packet, addr, seq_num)  # Sends the packet to the client
                    seq_num += 1  # Increments the sequence number
        except FileNotFoundError:
            print(f"File {filename} not found at {file_path}.")  # Prints an error if the file is not found

    def create_packet(self, seq_num, data):
        checksum = compute_checksum(seq_num.to_bytes(4, byteorder='big') + data)  # Computes the checksum for the packet
        print(f"Computed checksum for packet {seq_num}: {checksum}")
        header = struct.pack('!I H', seq_num, checksum)  # Packs the sequence number and checksum into a header
        return header + data  # Returns the complete packet (header + data)

    def send_packet(self, packet, addr, seq_num):
        if simulate_packet_loss():
            print(f"Packet {seq_num} lost.")  # Simulates packet loss
            return

        self.server_socket.sendto(packet, addr)  # Sends the packet to the client's address
        print(f"Sent packet {seq_num} to {addr} with checksum {struct.unpack('!H', packet[4:6])[0]}")
        print(f"ACK = True")  # Indicates that the packet was sent

        timer = threading.Timer(1.0, self.resend_packet, [packet, addr, seq_num])  # Sets a timer for retransmission
        timer.start()  # Starts the timer

    def resend_packet(self, packet, addr, seq_num):
        with self.lock:  # Acquires the lock to ensure thread-safe operation
            if seq_num in self.window:  # Checks if the packet is still in the window
                self.send_packet(packet, addr, seq_num)  # Retransmits the packet

    def run(self):
        print("Server is running...")
        while True:
            try:
                data, addr = self.server_socket.recvfrom(1024)  # Receives data from the client
                filename = data.decode('utf-8')  # Decodes the received data to get the filename
                print(f"Received request for file {filename} from {addr}")
                self.handle_client(addr, filename)  # Handles the client's request
            except Exception as e:
                print(f"An error occurred: {e}")  # Prints any errors that occur

if __name__ == "__main__":
    server = Server(SERVER_PORT)  # Creates a Server object with the specified port
    server.run()  # Runs the server
