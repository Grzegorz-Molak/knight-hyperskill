class ExceptionDimensions(Exception):
    pass


class Board:
    def __init__(self):
        self.dimensions = self.get_dimensions()
        self.knight_pos = self.set_pos()
        self.visited = [[self.knight_pos['x'], self.knight_pos['y']]]
        self.cell_size = len(str(self.dimensions['x'] * self.dimensions['y']))

    def get_dimensions(self):
        while 1:
            try:
                dims = list(map(int, input("Enter your board dimensions: ").split()))
                dims = {"x": dims[0], "y": dims[1]}
                if (len(dims) != 2 or dims["x"] < 1 or dims["y"] < 1):
                    raise ExceptionDimensions
                return dims
                # print(self.dimensions)
            except (ValueError, IndexError, ExceptionDimensions):
                print("Invalid dimensions!")

    def set_pos(self):
        while 1:
            try:
                pos = list(map(int, input("Enter the knight's starting position: ").split()))
                pos = {"x": pos[0], "y": pos[1]}
                # print(pos)
                # print(pos["x"])
                if len(pos) != 2 or pos["x"] < 1 or pos["y"] < 1 or pos["x"] > self.dimensions["x"] or pos["y"] > \
                        self.dimensions["y"]:
                    raise ExceptionDimensions
                return pos
            except (ValueError, IndexError, ExceptionDimensions):
                print("Invalid position!")

    def generate_knight_moves(self, visited, y=None, x=None):
        # print(visited)
        result = []
        if x is None and y is None:
            # x = self.knight_pos['x']
            # y = self.knight_pos['y']
            x = visited[len(visited) - 1][0]
            y = visited[len(visited) - 1][1]
        # print(f"Analysing position: y: {y}, x: {x}")
        for dy in [-2, -1, 1, 2]:
            if y + dy in list(range(1, self.dimensions['y'] + 1)):
                if abs(dy) == 1:
                    for dx in [-2, 2]:
                        if x + dx in list(range(1, self.dimensions['x'] + 1)):
                            if [x + dx, y + dy] not in visited:
                                result.append([y + dy, x + dx])
                                # print(f"Adding y: {y+dy}, x: {x+dx} as {y+dy} in {list(range(1, self.dimensions['y']+1))} and {x+dx} in {list(range(1, self.dimensions['x']+1))}")
                        # else:
                        # print(f"x+dx =  {x+dx} is not in x: {list(range(1, self.dimensions['x']+1))}")
                elif abs(dy) == 2:
                    for dx in [-1, 1]:
                        if x + dx in list(range(1, self.dimensions['x'] + 1)):
                            if [x + dx, y + dy] not in visited:
                                result.append([y + dy, x + dx])
                                # print(f"Adding y: {y+dy}, x: {x+dx} as {y+dy} in {list(range(1, self.dimensions['y']+1))} and {x+dx} in {list(range(1, self.dimensions['x']+1))}")
                        # else:
                        # print(f"x+dx = {x+dx} is not in x: {list(range(1, self.dimensions['x']+1))}")
            # else:
            # print(f"y+dy = {y+dy} is not in y: {list(range(1, self.dimensions['y']+1))}")
        # print(result)
        # print('---------------------------')
        return result

    def player_move(self):
        possible_moves = self.generate_knight_moves(self.visited)
        # print(f"There are possible {len(possible_moves)} moves")
        while 1:
            try:
                dims = list(map(int, input("Enter your next move: ").split()))
                dims = [dims[1], dims[0]]
                if len(dims) != 2 or dims not in possible_moves:
                    raise ExceptionDimensions
                self.visited = self.move_knight(self.visited, dims[1], dims[0])
                return
                # print(self.dimensions)
            except (ValueError, IndexError, ExceptionDimensions):
                print("Invalid move!", end=" ")

    def move_knight(self, visited, x, y):
        self.knight_pos |= {'x': x, 'y': y}
        # print(f"{visited} rrrrrrr")
        visited.append([x, y])
        # print(f"{visited} eeeee")
        return visited

    def find_solution(self, visited, playing=False):
        copy_visited = visited[:]
        # self.draw_board(copy_visited)
        possible_moves = self.generate_knight_moves(copy_visited)
        if len(possible_moves) == 0:
            if len(visited) == self.dimensions['x'] * self.dimensions['y']:
                if not playing:
                    print("Here's the solution!")
                    self.draw_board(copy_visited, True)
                return True
            else:
                return False
        elif len(possible_moves) == 1:
            copy_to_run = self.move_knight(copy_visited, possible_moves[0][1], possible_moves[0][0])
            return self.find_solution(copy_to_run, playing)

        else:
            possible_moves = self.generate_knight_moves(copy_visited)
            number_of_moves = []
            for square in possible_moves:
                number_of_moves.append(len(self.generate_knight_moves(copy_visited, square[0], square[1])))
            number_min = 8
            number_min_index = []
            for index, number in enumerate(number_of_moves):
                if number == number_min:
                    number_min_index.append(index)
                elif number_min > number > 0:
                    number_min = number
                    number_min_index = [index]
            # print(possible_moves)
            # print(number_of_moves)
            # print(number_min_index)

            for index in number_min_index:
                # input(f" going to {possible_moves[index][1]},{possible_moves[index][0]} ")
                # print('------------------------')
                copy_to_run = self.move_knight(copy_visited, possible_moves[index][1], possible_moves[index][0])
                if self.find_solution(copy_to_run, playing):
                    return True
        return False

    def add_element(self, char):
        return ' ' * (self.cell_size - len(str(char))) + str(char)

    def add_all_elements(self, visited):
        board_copy = [['_' * self.cell_size] * self.dimensions['x'] for _ in range(self.dimensions['y'])]
        for square in self.generate_knight_moves(visited):
            pass
            # board_copy[square[0]-1][square[1]-1] = self.add_element('o')
            board_copy[square[0] - 1][square[1] - 1] = self.add_element(len(self.generate_knight_moves(visited, square[0], square[1])))
        for square in visited:
            board_copy[square[1] - 1][square[0] - 1] = self.add_element('*')

        board_copy[self.knight_pos['y'] - 1][self.knight_pos['x'] - 1] = self.add_element('x')
        return board_copy

    def draw_board(self, visited=None, special=False):
        if visited is None:
            visited = self.visited

        if not special:
            board_to_draw = self.add_all_elements(visited)
        else:
            board_to_draw = [['_' * self.cell_size] * self.dimensions['x'] for _ in range(self.dimensions['y'])]
            for index, square in enumerate(visited):
                board_to_draw[square[1]-1][square[0]-1] = self.add_element(str(index+1))

        print(' ' * len(str(self.dimensions['y'])) + '-' * (self.dimensions['x'] * (self.cell_size + 1) + 3))

        for y in range(self.dimensions["y"], 0, -1):
            print(' ' * (len(str(self.dimensions['y'])) - len(str(y))), end="")
            print(f"{y}|", end=" ")
            for x in range(self.dimensions["x"]):
                print(board_to_draw[y - 1][x], end=" ")
            print("|")

        print(' ' * len(str(self.dimensions['y'])) + '-' * (self.dimensions['x'] * (self.cell_size + 1) + 3))
        print(' ' * ((len(str(self.dimensions['y']))) + 2), end="")
        print(*[' ' * (self.cell_size - len(str(x))) + str(x) for x in range(1, self.dimensions['x'] + 1)])

    def decide_result(self):
        if len(self.visited) == self.dimensions['x'] * self.dimensions['y']:
            return "What a great tour! Congratulations!"
        else:
            return f"No more possible moves! \nYour knight visited {len(self.visited)} squares!"


def game():
    board = Board()
    while 1:
        try:
            game_type = input("Do you want to try the puzzle? (y/n): ")
            if game_type == "y":
                knight_pos_save_x = board.knight_pos['x']
                knight_pos_save_y = board.knight_pos['y']
                if board.find_solution(board.visited, True):
                    board.knight_pos['x'] = knight_pos_save_x
                    board.knight_pos['y'] = knight_pos_save_y
                    board.visited = [[board.knight_pos['x'], board.knight_pos['y']]]
                    board.draw_board()
                    while len(board.generate_knight_moves(board.visited)) > 0:
                        board.player_move()
                        board.draw_board()

                    return board.decide_result()
                else:
                    return "No solution exists!"
            elif game_type == "n":
                if not board.find_solution(board.visited):
                    return "No solution exists!"
                else:
                    return
            else:
                raise ExceptionDimensions
        except (ValueError, ExceptionDimensions):
            print("Invalid input!", end=" ")
# ###################################################


print(game())

# board.draw_board()

