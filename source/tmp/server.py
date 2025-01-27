import socket
import time
from io import BytesIO
import numpy as np
import os

def serve_sokoban(tcp_ip, tcp_port, dataset_path, timeout_ms):

    # Create a socket and bind it to the specified address and port
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((tcp_ip, tcp_port))
    server_socket.listen(1)

    print(f"Server listening on {tcp_ip}:{tcp_port}")

    while True:
        # Accept a connection from a client
        conn, addr = server_socket.accept()
        print(f"Connection from {addr}")

        try:

            # Get random int
            randint = np.random.randint(100)
            
            with open(os.path.join(dataset_path, str(randint), "question.txt"), 'r') as f:
                question = f.read().strip()
            with open(os.path.join(dataset_path, str(randint), "solution.txt"), 'r') as f:
                solution = f.read().strip()
            image_path = os.path.join(dataset_path, str(randint), "image.jpg")
            print(f"Expected answer: {solution}")

            # Load the image
            image = Image.open(image_path)

            # Convert image to bytes
            img_bytes = BytesIO()
            image.save(img_bytes, format='JPEG')
            img_data = img_bytes.getvalue()


            banner = \
            f"Welcome back!\n\nProvide the answer in the format: XXXXXXXX\nFor instance, 12345678 is a correct answer format.\nTime's ticking!\n\n>>> Press enter to receive your challenge in JPG format."

            conn.sendall(banner.encode('utf-8'))

            conn.recv(1024).decode('utf-8').strip()

            # Send the image to the client
            conn.sendall(img_data)

            time.sleep(0.5)

            # Record the start time
            start_time = time.time()

            # Send the question
            conn.sendall(f"\n\n\n\nQuestion is: {question}\n".encode('utf-8'))
            
            time.sleep(0.2)

            # Ask for answer
            conn.sendall(f"\nAnswer?\n>>> ".encode('utf-8'))

            time.sleep(0.2)
            
            # Receive the answer from the client
            answer = conn.recv(1024).decode('utf-8').strip()
            print(f"Received answer: {answer}")

            # Calculate the elapsed time
            elapsed_time = (time.time() - start_time) * 1000

            print(':'.join(hex(ord(x))[2:] for x in answer))
            print(':'.join(hex(ord(x))[2:] for x in solution))
            print(answer==solution)
            # Check if the answer is correct and within the specified timeout
            if (answer == solution) and (elapsed_time < timeout_ms):
                print(f"Correct!")
                with open('flag.txt', 'r') as f:
                    flag = f.read()
                conn.sendall(f"Correct! Here's the flag: {flag}".encode('utf-8'))
            elif answer != solution:
                print(f"Wrong answer!")
                conn.sendall(f"Wrong answer!".encode('utf-8'))
            elif answer == solution and elapsed_time >= timeout_ms:
                print(f"Correct but too late :(")
                conn.sendall(f"Too late :(".encode('utf-8'))

        finally:
            # Close the connection
            conn.close()

if __name__ == "__main__":
    # Set server IP, port, image path, and timeout in milliseconds
    server_ip = "0.0.0.0"
    server_port = 12345
    dataset_path = "../sudoku-generator/sudoku-images"
    timeout_ms = 8000  # 5 seconds

    serve_sokoban(server_ip, server_port, dataset_path, timeout_ms)
