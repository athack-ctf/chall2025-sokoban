class SokobanVerifier:
    def __init__(self, level):
        self.grid = [list(row) for row in level.split("\n")]
        self.rows = len(self.grid)
        self.cols = max([len(row) for row in self.grid])
        self.player_pos = self.find_player()
        self.boxes, self.targets = self.find_boxes_and_targets()

        print(self.boxes)

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

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        print("Usage: python sokoban_verifier.py <level_file> <solution_file>")
        sys.exit(1)

    level_file = sys.argv[1]
    solution_file = sys.argv[2]

    with open(level_file, "r") as lf:
        level = lf.read()
        print(level)

    with open(solution_file, "r") as sf:
        solution = sf.read()

    verifier = SokobanVerifier(level)
    verifier.verify_solution(solution)