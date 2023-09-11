from queue import PriorityQueue
import copy


class State:
    def __init__(self, red_car, cars, parent=None, row=None, column=None):
        self.red_car = red_car
        self.cars = cars
        self.board = None
        self.parent = parent
        if self.parent is not None:
            self.g = parent.g + 1
            self.row = parent.column
            self.column = parent.column
        else:
            self.g = 0
            self.row = row
            self.column = column

    def f(self):
        return self.g + self.h()

    def h(self):
        if self.board is None:
            self.make_board()

        return sum(self.board[self.red_car.y][self.red_car.x + self.red_car.length:])

    def make_board(self):
        self.board = [[0 for _ in range(self.column)] for _ in range(self.row)]
        for car in self.cars + [self.red_car]:
            if car.dir == 'h':
                for i in range(car.x, car.x + car.length):
                    self.board[car.y][i] = 1
            else:
                for j in range(car.y, car.y - car.length, -1):
                    self.board[j][car.x] = 1

    def state_str(self):
        state_str = f"{self.red_car.x}{self.red_car.y}"
        for i in self.cars:
            state_str = state_str + f"{i.x}{i.y}"
        return state_str

    def total_state(self):
        node, count = self, []
        while node:
            count.append(node)
            node = node.parent
        return count

    def solved(self):
        return self.h() == 0

    def create_children(self):
        children = []
        for i in range(len(self.cars)):
            car_to_move = self.cars[i]
            if car_to_move.dir == 'h':
                for j in range(car_to_move.x + car_to_move.length, self.column):
                    if self.board[car_to_move.y][j] == 0:
                        cars_copy = self.cars[0:i] + [copy.deepcopy(car_to_move)] + self.cars[i + 1:]
                        cars_copy[i].set_x(j - car_to_move.length + 1)
                        child = State(self.red_car, cars_copy, self)
                        children.append(child)
                    else:
                        break
                for j in range(car_to_move.x - 1, -1, -1):
                    if self.board[car_to_move.y][j] == 0:
                        cars_copy = self.cars[0:i] + [copy.deepcopy(car_to_move)] + self.cars[i + 1:]
                        cars_copy[i].set_x(j)
                        child = State(self.red_car, cars_copy, self)
                        children.append(child)
                    else:
                        break
            else:
                for j in range(car_to_move.y + 1, self.row):
                    if self.board[j][car_to_move.x] == 0:
                        cars_copy = self.cars[0:i] + [copy.deepcopy(car_to_move)] + self.cars[i + 1:]
                        cars_copy[i].set_y(j)
                        child = State(self.red_car, cars_copy, self)
                        children.append(child)
                    else:
                        break
                for j in range(car_to_move.y - car_to_move.length, -1, -1):
                    if self.board[j][car_to_move.x] == 0:
                        cars_copy = self.cars[0:i] + [copy.deepcopy(car_to_move)] + self.cars[i + 1:]
                        cars_copy[i].set_y(j + car_to_move.length - 1)
                        child = State(self.red_car, cars_copy, self)
                        children.append(child)
                    else:
                        break

        for j in range(self.red_car.x + self.red_car.length, self.column):
            if self.board[self.red_car.y][j] == 0:
                red_copy = copy.deepcopy(self.red_car)
                red_copy.set_x(j - self.red_car.length + 1)
                child = State(red_copy, self.cars, self)
                children.append(child)
            else:
                break
        for j in range(self.red_car.x - 1, -1, -1):
            if self.board[self.red_car.y][j] == 0:
                red_copy = copy.deepcopy(self.red_car)
                red_copy.set_x(j)
                child = State(red_copy, self.cars, self)
                children.append(child)
            else:
                break

        return children


class Car:
    def __init__(self, x, y, length, dir):
        self.x = x
        self.y = y
        self.length = length
        self.dir = dir

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y


def solve(s_state):
    count = 2
    queue = PriorityQueue()
    queue.put((s_state.f(), 1, s_state))
    frontier = set()
    close = set()
    frontier.add(s_state.state_str())
    while not queue.empty():
        cur_state = queue.get()[2]
        state_str = cur_state.state_str()
        frontier.remove(state_str)
        close.add(state_str)
        if cur_state.solved():
            return cur_state.total_state()
        children = cur_state.create_children()
        for next_state in children:
            state_str = next_state.state_str()
            if state_str not in frontier and state_str not in close:
                frontier.add(state_str)
                queue.put((next_state.f(), count, next_state))
                count = count + 1

    return -1


car = []
k, n, m = [int(i) for i in input().split()]
x, y, direction, length = [i for i in input().split()]
red_car = Car(int(x), m - int(y) - 1, int(length), 'h')

for i in range(k - 1):
    x, y, direction, length = [i for i in input().split()]
    change_y = m - int(y) - 1
    new_car = Car(int(x), change_y, int(length), direction)
    car.append(new_car)

start = State(red_car=red_car, cars=car, parent=None, row=m, column=n)

total_state = solve(start)

for i in total_state:
    print(i.board)
