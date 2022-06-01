# Toy Robot Simulator -- a coding exercise
# Python 3.10 or higher required

__AUTHOR__ = 'Art Pashchuk'
__VERSION__ = '1.0.0'

TABLE_WIDTH = 5
TABLE_HEIGHT = 5


class Table:

    def __init__(self, width, height):
        # set table dimensions
        self.limits = {'x': width, 'y': height}
        self.robot = None  # not placed

    def listen(self):
        while True:  # forever loop
            self.process_command(input('> '))

    def process_command(self, command):
        cmd = command.upper().strip().split(' ')
        if len(cmd) == 1:  # no space = simple command without params
            if self.robot is None:
                print('Robot not placed. Please use PLACE command first to specify X, Y and F (facing)')
                return
            match cmd[0]:
                case 'MOVE':
                    self.robot.move()
                case 'LEFT' | 'RIGHT':
                    self.robot.rotate(cmd[0])
                case 'REPORT':
                    print(f'{self.robot.position["x"]},{self.robot.position["y"]},{self.robot.facing}')
                case 'PLACE':
                    print('This command requires parameters X,Y,F')
                case _:
                    print('Command not recognised')
                    return
        elif len(cmd) == 2:  # command + params
            params = cmd[1].split(',')
            if cmd[0] == 'PLACE':
                if len(params) != 3:
                    print('Invalid parameters. Use PLACE X,Y,F')
                    return
                valid_coordinates = [n for n in '01234']
                x, y, f = params[0].strip(), params[1].strip(), params[2].strip()
                if not (x in valid_coordinates and y in valid_coordinates):
                    print('Both coordinates must be within range from 0 to 4')
                    return
                if f not in ['NORTH', 'SOUTH', 'EAST', 'WEST']:
                    print('Robot can be facing NORTH, SOUTH, EAST or WEST')
                    return
                # all parameters validated, we can safely place robot
                self.robot = Robot(table=self, position={'x': int(x), 'y': int(y)}, facing=f)
        else:
            print('Wrong command format')
            return


class Robot:
    def __init__(self, table, position, facing):
        self.table = table
        self.position = position
        self.facing = facing
        self.increments = {'NORTH': {'x': 0, 'y': 1},
                           'EAST': {'x': 1, 'y': 0},
                           'SOUTH': {'x': 0, 'y': -1},
                           'WEST': {'x': -1, 'y': 0}
                           }

    def move(self):
        for coordinate in ['x', 'y']:
            self.position[coordinate] += self.increments[self.facing][coordinate]
            limit = self.table.limits[coordinate] - 1
            if self.position[coordinate] > limit:
                self.position[coordinate] = limit
            elif self.position[coordinate] < 0:
                self.position[coordinate] = 0

    def rotate(self, turn):
        directions = [key for key in self.increments]  # clockwise
        index = directions.index(self.facing)
        index += 1 if turn == 'RIGHT' else -1  # rotate clockwise or counter-clockwise
        if index == -1:
            index = 3
        elif index == 4:
            index = 0
        self.facing = directions[index]


if __name__ == '__main__':
    Table(TABLE_WIDTH, TABLE_HEIGHT).listen()
