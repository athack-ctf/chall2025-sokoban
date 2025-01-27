# Sokoban
import json
import numpy as np
import socket
import time
import traceback
import string
import os






class SokobanVerifier:

    def __init__(self, level):
        self.allowed = set("UDLRudlr")
        self.grid = [list(row) for row in level.split("\n")]
        self.rows = len(self.grid)
        self.cols = max([len(row) for row in self.grid])
        for index, row in enumerate(self.grid):
            if len(row) < self.cols:
                for x in range(self.cols - len(row)):
                    self.grid[index].append(' ')

        print(self.grid)
        print(self.rows, self.cols)
        self.player_pos = self.find_player()
        self.boxes, self.targets = self.find_boxes_and_targets()

        print(self.boxes)

    def check_answer(self, answer):
        print(set(answer))
        print(self.allowed)
        return (set(answer) <= self.allowed)

    def find_player(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c] == "@":
                    return (r, c)
                elif self.grid[r][c] == "+":
                    return (r, c)

    def find_boxes_and_targets(self):
        boxes = set()
        targets = set()
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c] == "$":
                    boxes.add((r,c))
                elif self.grid[r][c] == ".":
                    targets.add((r,c))
                elif self.grid[r][c] == "*":
                    targets.add((r,c))
                    boxes.add((r,c))
                elif self.grid[r][c] == "+":
                    targets.add((r,c))
        return boxes, targets

    def is_valid_position(self, pos):
        r, c = pos
        return 0 <= r < self.rows and 0 <= c < self.cols and self.grid[r][c] != "#"

    def move_player(self, player, direction):
        dr, dc = direction
        return (player[0] + dr, player[1] + dc)

    def move_box(self, box, direction):
        dr, dc = direction
        return (box[0] + dr, box[1] + dc)

    def apply_move(self, move):
        direction_map = {
            "L": (0, -1), "R": (0, 1), "U": (-1, 0), "D": (1, 0),
            "l": (0, -1), "r": (0, 1), "u": (-1, 0), "d": (1, 0)
        }
        direction = direction_map[move]
        new_player = self.move_player(self.player_pos, direction)

        if not self.is_valid_position(new_player):
            print("ERROR: you are trying to make an invalid move")
            return False

        if move.islower():  # Player-only move
            self.player_pos = new_player
            return True

        if new_player in self.boxes:  # Push a box
            # Check if its uppercase
            if move.islower():
                print("ERROR: you are trying to push a box (should be UPPERCASE move)")
                return False
            new_box = self.move_box(new_player, direction)
            if not self.is_valid_position(new_box) or new_box in self.boxes:
                print("ERROR: this box cannot move in this direction")
                return False
            self.boxes.remove(new_player)
            self.boxes.add(new_box)

        self.player_pos = new_player
        return True

    def is_solved(self):
        return self.boxes == self.targets

    def verify_solution(self, solution):
        # Check if valid string
        if self.check_answer(solution):
            for move in solution:
                if not self.apply_move(move):
                    print("Invalid move:", move)
                    return False

            if self.is_solved():
                print("Solution is correct!")
                return True
            else:
                print("Solution is incorrect: Not all boxes are on targets.")
                return False
        else:
            print("ERROR: Invalid answer/moves detected.")
            return False





def handle_client(client_socket, client_address):
    print(f"Accepted connection from {client_address}")

    with open('solvable.json', 'r') as f:
        puzzles = json.load(f)

    key = np.random.choice(list(puzzles.keys()))
    print(puzzles[key])
    puzzle = puzzles[key]
    layout = '\n'.join(puzzle["layout"])

    client_socket.sendall(layout.encode('utf-8'))

    try:
        data = client_socket.recv(1024)

        client_response = data.decode().strip()

        print(client_response)

        # Example: Check if the client_response is correct
        
        verifier = SokobanVerifier(layout)

        if (verifier.verify_solution(client_response)):
            print(f"Client {client_address} provided a correct response: {client_response}")
            client_socket.sendall("Correct!\n".encode('utf-8'))
            return True
        else:
            print(f"Client {client_address} provided an incorrect response: {client_response}")
            client_socket.sendall("Wrong :(\n".encode('utf-8'))
            return False

    except Exception as e:
        print(f"Error handling client {client_address}: {str(e)}")
        print(traceback.format_exc())
        client_socket.close()
        return False



def serve_client(tcp_ip, tcp_port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((tcp_ip, tcp_port))
    server_socket.listen(5)

    print(f"Server listening on {tcp_ip}:{tcp_port}")

    while True:

        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address}")
        try:
            banner = \
                f"Hey there!\n\nThree sokoban puzzles ahead. Give me a solution for each of them, and I'll reward you.\nTime's ticking!\n\n>>> Press enter to start."
            client_socket.sendall(banner.encode('utf-8'))

            client_socket.recv(1024).decode('utf-8').strip()


            start_time = time.time()

            # Challenge 1
            chal1 = handle_client(client_socket, client_address)

            elapsed_time = (time.time() - start_time) * 1000
            if chal1:
                if elapsed_time < timeout_ms:
                    # Challenge 2
                    chal2 = handle_client(client_socket, client_address)

                    elapsed_time = (time.time() - start_time) * 1000
                    if chal2:           
                        if elapsed_time < timeout_ms:
                            # Challenge 3
                            chal3 = handle_client(client_socket, client_address)

                            elapsed_time = (time.time() - start_time) * 1000
                            if chal3 and elapsed_time < timeout_ms:
                                if elapsed_time < timeout_ms:
                                    with open('flag.txt', 'r') as f:
                                        flag = f.read()
                                    client_socket.sendall(f"Good job! Here's the flag: {flag}\n".encode('utf-8'))
                                    client_socket.close()
                                else:
                                    print("Too slow\n")
                                    client_socket.sendall(f"Too slow :(".encode('utf-8'))
                                    client_socket.close()
                        else:
                            print("Too slow\n")
                            client_socket.sendall(f"Too slow :(".encode('utf-8'))
                            client_socket.close()
                else:
                    print("Too slow\n")
                    client_socket.sendall(f"Too slow :(".encode('utf-8'))
                    client_socket.close()
        finally:
            client_socket.close()


if __name__ == "__main__":
    host = "0.0.0.0"  # Replace with your server's IP address
    port = int(os.environ["PORT"])  # Replace with your desired port number
    timeout_ms = int(os.environ["TIMEOUT"])

    serve_client(host, port)
    
