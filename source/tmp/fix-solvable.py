import os
import re
import time
from multiprocessing import Process
import sys
import collections
import numpy as np
import heapq
import time
import json




def process_puzzles(input_file):
    """Process puzzles from a file, solving each with a timeout."""


    with open(input_file, "r") as f:
        data = json.load(f)
    
    for key in data.keys():
        print(key)
        print(data[key]["layout"])

        # Count leading space on second line
        line2 = data[key]["layout"][1]
        spaces = len(line2) - len(line2.lstrip(' '))
        print("Spaces missing:", spaces)

        # If spaces and only 1 wall size after, add spaces
        if spaces != 0:
            next_wall_size = len(re.sub(r'[^#]', ' ', line2).strip().split(" ")[0])
            print("Wall size:", next_wall_size)
            if next_wall_size == 1:
                print("Before:", data[key]["layout"])
                data[key]["layout"][0] = ' '*spaces + data[key]["layout"][0]
                print("After-:", data[key]["layout"])
            elif next_wall_size > 1:
                print("Before:", data[key]["layout"])
                data[key]["layout"][0] = ' '*(spaces + next_wall_size - 1) + data[key]["layout"][0]
                print("After-:", data[key]["layout"])

            print(data[key])
        else:
            next_wall_size = len(re.sub(r'[^#]', ' ', line2).strip().split(" ")[0])
            print("Before:", data[key]["layout"])
            data[key]["layout"][0] = ' '*(next_wall_size - 1) + data[key]["layout"][0]
            print("After-:", data[key]["layout"])


    with open('solvable-fixed.json', 'w') as f:
        json.dump(data, f, indent=4)






if __name__ == "__main__":
    global  layout
    process_puzzles("solvable.json")
