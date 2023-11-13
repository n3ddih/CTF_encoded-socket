import base64
import string
import socket
import threading
import random

# Define the host and port where your server will run
# define the number of questions and the time limit per question
NUM_QUESTIONS = 100
TIME_LIMIT = 90
HOST = '0.0.0.0'
PORT = 12345
FLAG = 'flag{test_flag}'

# Initialize a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(200)  # You can adjust the number of connections you want to allow

# List to keep track of connected clients
connected_clients = []

# Function to generate encoded string
def encode(input, base):
    if base == 2:
        return ''.join(bin(byte)[2:].zfill(8) for byte in input.encode())
    if base == 8:
        return ''.join(oct(byte)[2:].zfill(3) for byte in input.encode())
    if base == 16:
        return ''.join(hex(byte)[2:].zfill(2) for byte in input.encode())
    if base == 32:
        return base64.b32encode(input.encode()).decode()
    if base == 64:
        return base64.b64encode(input.encode()).decode()

# Function to handle a client's connection
def handle_client(client_socket, client_IP, client_PORT):
    try:
        # Set a timeout for client connection
        client_socket.settimeout(TIME_LIMIT)

        # Add the client to the list of connected clients
        connected_clients.append(client_socket)

        # Send a welcome message to the client
        client_socket.send(b"Welcome to the quiz game! You will be asked 100 encoded strings. You need to answer correctly to go to the next question. You have 90 seconds to solve the challenge. Good luck!\n")

        # initialize the score and the question number
        score = 0
        question_num = 1

        while question_num <= NUM_QUESTIONS:
            # generate a random string of length 10
            rand_str = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
            # generate random
            base = random.choice([2, 8, 16, 32, 64])
            # encode the number using the base
            encoded = encode(rand_str, base)
            # send the question to the client
            client_socket.send(f"Question {question_num}: What is the answer for {base}:{encoded}?\n".encode())
            # receive the answer from the client
            answer = client_socket.recv(1024).decode().strip()  # Adjust the buffer size as needed
            # check if the answer is correct
            if answer == rand_str:
                # increment the score and send a positive feedback
                score += 1
                # increment the question number
                question_num += 1
                client_socket.send(b"Correct!\n")
            else:
                # send a negative feedback then end the challenge
                client_socket.send(f"Wrong! The correct answer is {rand_str}.\n".encode())
                break

        if score == NUM_QUESTIONS:
            client_socket.send(f"Congratulation! Here is your flag: {FLAG}\n".encode())

    
    except socket.timeout:
        print(f"Client timed out at {client_IP}:{client_PORT}")
    except Exception as e:
        print(f"Error handling client: {str(e)}")
    finally:
        client_socket.close()
        print(f"Closed connection from {client_IP}:{client_PORT}")
        connected_clients.remove(client_socket)

# Main server loop
while True:
    client_socket, client_address = server_socket.accept()
    print(f"Accepted connection from {client_address[0]}:{client_address[1]}")
    
    # Create a new thread to handle the client
    client_thread = threading.Thread(target=handle_client, args=(client_socket,client_address[0],client_address[1],))
    client_thread.start()
