
# Artificial Intelligence Assignment 1
# __author__ = "clucle"

import math

MAZE_FILE_PATH = ""
MAZE_INPUT_FILE_NAME = "_floor.txt"
MAZE_OUTPUT_FILE_NAME = "_floor_output.txt"
DEBUG = False


class Node:
    def __init__(self, here_y, here_x, step, dst_y, dst_x, parent_y, parent_x,
                 weight_step, weight_heuristic, heuristic_type):
        self.here_y = here_y
        self.here_x = here_x
        self.parent_y = parent_y
        self.parent_x = parent_x
        self.step = step
        # min heap
        self.priority = step * weight_step
        if heuristic_type == 1:
            self.priority += self.manhattan(here_y, here_x, dst_y, dst_x) * weight_heuristic
        elif heuristic_type == 2:
            self.priority += self.euclidean(here_y, here_x, dst_y, dst_x) * weight_heuristic
        elif heuristic_type == 3:
            self.priority += self.euclidean_cube(here_y, here_x, dst_y, dst_x) * weight_heuristic

    @staticmethod
    def manhattan(here_y, here_x, dst_y, dst_x):
        return abs(here_y - dst_y) + abs(here_x - dst_x)

    @staticmethod
    def euclidean(here_y, here_x, dst_y, dst_x):
        return math.sqrt((here_y - dst_y) * (here_y - dst_y) + (here_x - dst_x) * (here_x - dst_x))

    @staticmethod
    def euclidean_cube(here_y, here_x, dst_y, dst_x):
        return (here_y - dst_y) * (here_y - dst_y) + (here_x - dst_x) * (here_x - dst_x)


class PriorityQueue:
    def __init__(self):
        self.queue = list()

    def insert(self, node):
        if self.size() == 0:
            self.queue.append(node)
        else:
            for idx in range(0, self.size()):
                if node.priority > self.queue[idx].priority:
                    if idx == (self.size() - 1):
                        self.queue.insert(idx + 1, node)
                    else:
                        continue
                else:
                    self.queue.insert(idx, node)
                    return True

    def show(self):
        for idx in self.queue:
            print("pr {} y {} x {}".format(idx.priority, idx.here_y, idx.here_x))

    def delete(self):
        return self.queue.pop(0)

    def size(self):
        return len(self.queue)


class Maze:
    maze_names = None
    current_maze_idx = None
    current_row_size = None
    current_column_size = None
    current_maze = None
    current_maze_visit = None

    def init_maze(self):
        self.current_maze_idx = None
        self.current_row_size = None
        self.current_column_size = None
        self.current_maze = None
        self.current_maze_visit = None

    def set_maze(self, info):
        self.current_maze_idx = int(info[0])
        self.current_row_size = int(info[1])
        self.current_column_size = int(info[2])

    def print_maze(self):
        print("maze {}".format(self.current_maze_idx))
        for row in range(0, self.current_row_size + 2):
            print('[', end='')
            for col in range(0, self.current_column_size + 2):
                print(self.current_maze[row][col], end=',')
            print(']', end='')
            print(" ")

    def read_maze(self, path):
        with open(path, 'r') as f:
            lines = f.readlines()
            self.set_maze(info=lines[0].split())
            self.current_maze = [[0] * (self.current_column_size + 2) for _ in range(self.current_row_size + 2)]
            self.current_maze_visit = [[0] * (self.current_column_size + 2) for _ in range(self.current_row_size + 2)]
            for row in range(1, self.current_row_size + 1):
                arr = lines[row].split()
                arr.insert(0, '0')
                arr.append('0')
                self.current_maze[row] = list(map(int, arr))
        if DEBUG:
            self.print_maze()

    def write_maze(self, name, maze_len, maze_time):
        with open("./{}/{}{}".format(MAZE_FILE_PATH, name, MAZE_OUTPUT_FILE_NAME), 'w') as f:
            for row in range(1, self.current_row_size + 1):
                for col in range(1, self.current_column_size + 1):
                    f.write("{} ".format(self.current_maze[row][col]))
                f.write('\n')
            f.write("---\n")
            f.write("length={}\n".format(maze_len))
            f.write("time={}\n".format(maze_time))

    def get_start_position(self):
        for row in range(1, self.current_row_size + 1):
            for col in range(1, self.current_column_size + 1):
                if self.current_maze[row][col] == 3:
                    return row, col

    def get_key_position(self):
        for row in range(1, self.current_row_size + 1):
            for col in range(1, self.current_column_size + 1):
                if self.current_maze[row][col] == 6:
                    return row, col

    def get_destination_position(self):
        for row in range(1, self.current_row_size + 1):
            for col in range(1, self.current_column_size + 1):
                if self.current_maze[row][col] == 4:
                    return row, col

    def is_validate(self, valid_y, valid_x):
        if 0 < valid_y <= self.current_row_size and\
                0 < valid_x <= self.current_column_size:
            if self.current_maze[valid_y][valid_x] > 1:
                return True
        return False

    def find_path(self, here_y, here_x, dst_y, dst_x, weight_step, weight_heuristic, heuristic_type):
        q = PriorityQueue()
        q.insert(Node(here_y, here_x, 0, dst_y, dst_x, 0, 0, weight_step, weight_heuristic, heuristic_type))
        visit = [[0] * (self.current_column_size + 2) for _ in range(self.current_row_size + 2)]
        step = [[0] * (self.current_column_size + 2) for _ in range(self.current_row_size + 2)]
        time = 0
        while q.size() > 0:
            here = q.delete()
            hy = here.here_y
            hx = here.here_x
            if visit[hy][hx]:
                if step[hy][hx] <= here.step:
                    continue

            visit[hy][hx] = [here.parent_y, here.parent_x]
            time += 1
            step[hy][hx] = here.step
            
            if hy == dst_y and hx == dst_x:
                while visit[hy][hx] != [0, 0]:
                    if hy == here_y and hx == here_x:
                        break
                    if self.current_maze[hy][hx] != 3 and self.current_maze[hy][hx] != 4:
                        self.current_maze[hy][hx] = 5
                    tmp_hy = visit[hy][hx][0]
                    hx = visit[hy][hx][1]
                    hy = tmp_hy
                    
                return here.step, time

            if self.is_validate(hy + 1, hx):
                q.insert(Node(hy + 1, hx, here.step + 1, dst_y, dst_x, hy, hx,
                              weight_step, weight_heuristic, heuristic_type))
            if self.is_validate(hy, hx + 1):
                q.insert(Node(hy, hx + 1, here.step + 1, dst_y, dst_x, hy, hx,
                              weight_step, weight_heuristic, heuristic_type))
            if self.is_validate(hy - 1, hx):
                q.insert(Node(hy - 1, hx, here.step + 1, dst_y, dst_x, hy, hx,
                              weight_step, weight_heuristic, heuristic_type))
            if self.is_validate(hy, hx - 1):
                q.insert(Node(hy, hx - 1, here.step + 1, dst_y, dst_x, hy, hx,
                              weight_step, weight_heuristic, heuristic_type))
        return 0, time

    def first_floor(self, here_y, here_x, key_y, key_x, dst_y, dst_x):
        # greedy euclidean
        # 3850 / 5809
        key_len, key_time = self.find_path(here_y, here_x, key_y, key_x, 0, 1, 2)
        dst_len, dst_time = self.find_path(key_y, key_x, dst_y, dst_x, 0, 1, 2)
        return key_len + dst_len, key_time + dst_time

    def second_floor(self, here_y, here_x, key_y, key_x, dst_y, dst_x):
        # greedy manhattan
        # 758 / 1008
        key_len, key_time = self.find_path(here_y, here_x, key_y, key_x, 0, 1, 1)
        dst_len, dst_time = self.find_path(key_y, key_x, dst_y, dst_x, 0, 1, 1)
        return key_len + dst_len, key_time + dst_time

    def third_floor(self, here_y, here_x, key_y, key_x, dst_y, dst_x):
        # greedy euclidean
        # 554 / 649
        key_len, key_time = self.find_path(here_y, here_x, key_y, key_x, 0, 1, 2)
        dst_len, dst_time = self.find_path(key_y, key_x, dst_y, dst_x, 0, 1, 2)
        return key_len + dst_len, key_time + dst_time

    def fourth_floor(self, here_y, here_x, key_y, key_x, dst_y, dst_x):
        # a star euclidean_cube 1, 1, 3
        # 334 / 416
        key_len, key_time = self.find_path(here_y, here_x, key_y, key_x, 1, 1, 3)
        dst_len, dst_time = self.find_path(key_y, key_x, dst_y, dst_x, 1, 1, 3)
        return key_len + dst_len, key_time + dst_time

    def fifth_floor(self, here_y, here_x, key_y, key_x, dst_y, dst_x):
        # greedy euclidean
        # 106 / 120
        key_len, key_time = self.find_path(here_y, here_x, key_y, key_x, 0, 3, 2)
        dst_len, dst_time = self.find_path(key_y, key_x, dst_y, dst_x, 0, 3, 2)
        return key_len + dst_len, key_time + dst_time

    def sixth_floor(self, here_y, here_x, key_y, key_x, dst_y, dst_x):
        key_len, key_time = self.find_path(here_y, here_x, key_y, key_x, 2, 1, 1)
        dst_len, dst_time = self.find_path(key_y, key_x, dst_y, dst_x, 2, 1, 1)
        return key_len + dst_len, key_time + dst_time

    def explore(self, name):
        here_y, here_x = self.get_start_position()
        key_y, key_x = self.get_key_position()
        dst_y, dst_x = self.get_destination_position()
        maze_len, maze_time = getattr(self, "{}_floor".format(name))(here_y, here_x, key_y, key_x, dst_y, dst_x)
        self.write_maze(name, maze_len, maze_time)

    def run(self):
        for m in self.maze_names:
            self.init_maze()
            self.read_maze(path="./{}/{}{}".format(MAZE_FILE_PATH, m, MAZE_INPUT_FILE_NAME))
            self.explore(m)

    def __init__(self, maze_names):
        self.maze_names = maze_names


maze = Maze(maze_names=["first", "second", "third", "fourth", "fifth"])
maze.run()
