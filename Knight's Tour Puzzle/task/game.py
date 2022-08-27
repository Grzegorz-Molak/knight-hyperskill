# Write your code here
class ExceptionDimensions(Exception):
    pass


class Board:
    def __init__(self):
        self.dimensions = {"x": 0, "y": 0}
        self.knight_pos = {"x": 1, "y": 1}
        self.cell_size = 0

        self.get_dimensions()
        self.set_pos()

    def get_dimensions(self):
        while 1:
            try:
                dims = list(map(int, input("Enter your board dimensions: ").split()))
                dims = {"x": dims[0], "y": dims[1]}
                if(len(dims) != 2 or dims["x"] < 1 or dims["y"] < 1):
                    raise ExceptionDimensions
                self.dimensions = dims
                self.cell_size = len(str(self.dimensions['x']*self.dimensions['y']))
                # print(self.dimensions)
                return
            except (ValueError, IndexError, ExceptionDimensions):
                print("Invalid dimensions!")

    def set_pos(self):
        while 1:
            try:
                pos = list(map(int, input("Enter the knight's starting position: ").split()))
                pos = {"x": pos[0], "y": pos[1]}
                # print(pos)
                # print(pos["x"])
                if(len(pos) != 2 or pos["x"] < 1 or pos["y"] < 1 or pos["x"] > self.dimensions["x"] or pos["y"] > self.dimensions["y"]):
                    raise ExceptionDimensions
                self.knight_pos = pos
                return
            except (ValueError, IndexError, ExceptionDimensions):
                print("Invalid position!")

    def generate_knight_moves(self, y=None, x=None):
        result = []
        if x is None and y is None:
            x = self.knight_pos['x']
            y = self.knight_pos['y']
        # print(f"Analysing position: y: {y}, x: {x}")
        for dy in [-2, -1, 1, 2]:
            if y+dy in list(range(1, self.dimensions['y']+1)):
                if abs(dy) == 1:
                    for dx in [-2, 2]:
                        if x+dx in list(range(1, self.dimensions['x']+1)):
                            if not(x+dx == self.knight_pos['x'] and y+dy == self.knight_pos['y']):
                                result.append([y+dy, x+dx])
                                # print(f"Adding y: {y+dy}, x: {x+dx} as {y+dy} in {list(range(1, self.dimensions['y']+1))} and {x+dx} in {list(range(1, self.dimensions['x']+1))}")
                        # else:
                            # print(f"x+dx =  {x+dx} is not in x: {list(range(1, self.dimensions['x']+1))}")
                elif abs(dy) == 2:
                    for dx in [-1, 1]:
                        if x+dx in list(range(1, self.dimensions['x']+1)):
                            if not(x+dx == self.knight_pos['x'] and y+dy == self.knight_pos['y']):
                                result.append([y+dy, x+dx])
                                # print(f"Adding y: {y+dy}, x: {x+dx} as {y+dy} in {list(range(1, self.dimensions['y']+1))} and {x+dx} in {list(range(1, self.dimensions['x']+1))}")
                        # else:
                            # print(f"x+dx = {x+dx} is not in x: {list(range(1, self.dimensions['x']+1))}")
            # else:
                # print(f"y+dy = {y+dy} is not in y: {list(range(1, self.dimensions['y']+1))}")
        # print(result)
        # print('---------------------------')
        return result

    def add_element(self, char):
        return ' '*(self.cell_size-1)+str(char)

    def add_all_elements(self):
        board_copy = [['_'*self.cell_size]*self.dimensions['x'] for _ in range(self.dimensions['y'])]
        board_copy[self.knight_pos['y']-1][self.knight_pos['x']-1] = self.add_element('x')

        for square in self.generate_knight_moves():
            # board_copy[square[0]-1][square[1]-1] = self.add_element('o')
            board_copy[square[0]-1][square[1]-1] = self.add_element(len(self.generate_knight_moves(square[0], square[1])))
        return board_copy

    def draw_board(self):
        board_to_draw = self.add_all_elements()
        print(' '*len(str(self.dimensions['y']))+'-'*(self.dimensions['x']*(self.cell_size + 1) + 3))

        for y in range(self.dimensions["y"], 0, -1):
            print(' '*(len(str(self.dimensions['y'])) - len(str(y))), end="")
            print(f"{y}|", end=" ")
            for x in range(self.dimensions["x"]):
                print(board_to_draw[y-1][x], end=" ")
            print("|")

        print(' '*len(str(self.dimensions['y']))+'-'*(self.dimensions['x']*(self.cell_size + 1) + 3))
        print(' '*((len(str(self.dimensions['y']))) + 2), end="")
        print(*[' '*(self.cell_size-len(str(x)))+str(x) for x in range(1, self.dimensions['x']+1)])


# ###################################################
board = Board()
board.draw_board()


