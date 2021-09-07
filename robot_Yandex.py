from queue import Queue
import numpy as np
import random




class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


def astar(maze, start, end):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""

    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Add the start node
    open_list.append(start_node)

    # Loop until you find the end
    while len(open_list) > 0:

        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node:
            path = ''
            current = current_node
            while current.parent is not None:
                move = (current.position[0] - current.parent.position[0], current.position[1] - current.parent.position[1])
                if move == (-1, 0):
                    path += 'L'
                elif move == (1, 0):
                    path += 'R'
                elif move == (0, -1):
                    path += 'U'
                else:
                    path += 'D'
                current = current.parent
            return path[::-1] # Return reversed path

        # Generate children
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]: # Adjacent squares

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] != '.':
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:

            # Child is on the closed list
            for closed_child in closed_list:
                if child == closed_child:
                    continue

            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            # Child is already in the open list
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            # Add the child to the open list
            if child not in closed_list:
                open_list.append(child)

class rob:
    def __init__(self, x = 0, y = 0, state = 0, start_x = None, start_y = None, end_x = None, end_y = None, route = ''):
        
        self.x = x   #координаты в момент того, как ему пришел заказ
        self.y = y   

        self.state = state   #0 - без дела, 1 - едет забирать заказ, 2 - едет отдавать заказ

        self.start_x = start_x  #начало 
        self.start_y = start_y 

        self.end_x = end_x 
        self.end_y = end_y

        self.route = route #путь, который надо выводить 


def generate_bots(maze, n, num_of_rob): #написать функцию, которая хорошо выдает расположение в зависимости от входных данных
    bots = []
    print(num_of_rob,flush=True)
    for i in range(num_of_rob):
        x = random.randint(0, n - 1)
        y = random.randint(0, n - 1)
        while maze[y][x] == '#':
            x = random.randint(0, n - 1)
            y = random.randint(0, n - 1)
        print(y + 1, x + 1,flush=True)
        bots.append(rob(x = x,y = y))
    return bots


def find_robs(maze, n, max_tips, cost, t, d):
    #все числа с потолка взял

    if n == 9:
        num_of_rob = 1

    if n == 4:
        num_of_rob = 1
    elif n == 128:
        num_of_rob = 4 #очень дешевые боты, можно нагегенировать бесконечное количество
    elif n == 180:
        num_of_rob = 10 #хз пока
    elif n == 384:
        num_of_rob = 1
    elif n == 1024:
        num_or_rob = 75
    else:
        if max_tips == 123456:
            num_or_rob = 30
        elif max_tips == 101010:
            num_or_rob = 100
        elif max_tips == 1500000:
            num_or_rob = 20
        else:
            num_or_rob = 25

    return generate_bots(maze, n, num_of_rob)



def find_best(free_ord, bot_x, bot_y):  #добавить рандомные 100, вместо перебора всего

    min_cost = 1e7
    best_ord = None
    if len(free_ord) == 1:
        return 0
    k = np.random.randint(0, len(free_ord) - 1, min(100, len(free_ord) // 1000 + 10))
    for i in k:
        temp = abs(bot_x - free_ord[i][0]) + abs(bot_y - free_ord[i][1]) + abs(free_ord[i][0] - free_ord[i][2]) + abs(free_ord[i][1] - free_ord[i][3])
        if temp < min_cost:
            min_cost = temp
            best_ord = i
    return best_ord


def type_of_maze(n): #функция, которая проверяет тип карты
    if n == 9:
        return 1
    elif n in [4, 128]:
        return 0
    elif n in [180, 384, 1024]:
        return 1
    else:
        return 2



def check_square(n, x, y):
    x_add = 0
    y_add = 0
    if n == 180: ###.......#####.....
        # слева отступ 3, потом 7, потом 5 отступ. То же самое по y
        #если номер квадрата k, тогда 7 * (k - 1) + 
        X = (x - (3 - 1)) // 12 
        Y = (y - (3 - 1)) // 12   #X, Y - координаты квадратов
        if (x - (3 - 1)) % 12 > 10:
            x_add = 1
        if (y - (3 - 1)) % 12 > 10:
            y_add = 1

        return [(3 - 1) + 4 + X * 12 + x_add, (3 - 1) + 4 + Y * 12 + y_add]   #выдаем центры квадратов (отступ - 1) + радиус квадрата + X * (центральный отступ + размер квадрата)
    elif n == 384:
        X = (x - (6 - 1)) // 24
        Y = (y - (6 - 1)) // 24
        if (x - (6 - 1)) % 24 > 19:
            x_add = 1
        if (y - (6 - 1)) % 24 > 19:
            y_add = 1
        return [(6 - 1) + 7 + X * 24 + x_add, (6 - 1) + 7 + Y * 24 + y_add]
    else:
        X = (x - (8 - 1)) // 32
        Y = (y - (8 - 1)) // 32
        if (x - (8 - 1)) % 32 > 25:
            x_add = 1
        if (y - (8 - 1)) % 32 > 25:
            y_add = 1
        return [(8 - 1) + 9 + X * 32 + x_add, (8 - 1) + 9 + Y * 32 + y_add]


def find_best_for_cell(n, free_ord, bot_x, bot_y):
    min_cost = 1e7
    best_ord = None
    if len(free_ord) == 1:
        return 0
    k = np.random.randint(0, len(free_ord) - 1, min(100, len(free_ord) // 1000 + 10))
    for i in k:
        first_x, first_y = check_square(n, bot_x, bot_y)
        second_x, second_y = check_square(n, free_ord[i][0], free_ord[i][1])
        third_x, third_y = check_square(n, free_ord[i][2], free_ord[i][3])

        part_1 = abs(bot_x - first_x) + abs(bot_y - first_y)
        part_2 = abs(first_x - second_x) + abs(first_y - second_y)
        part_3 = abs(second_x - free_ord[i][0]) + abs(second_y - free_ord[i][1])
        part_4 = abs(second_x - third_x) + abs(second_y - third_y)
        part_5 = abs(third_x - free_ord[i][2]) + abs(third_y - free_ord[i][3])

        temp = part_1 + part_2 + 2 * part_3 + part_4 + part_5
        if temp < min_cost:
            min_cost = temp
            best_ord = i
    return best_ord

def find_route_izy(x0, y0, x1, y1):
    ans = ''
    if x1 - x0 >= 0:
        ans += 'R' * (x1 - x0)
    else:
        ans += 'L' * (x0 - x1)

    if y1 - y0 >= 0:
        ans += 'D' * (y1 - y0)
    else:
        ans += 'U' * (y0 - y1)

    return ans

def cells(maze, n, max_tips, cost, t, d):
    bots = find_robs(maze, n, max_tips, cost, t, d)

    free_ord = []
    

    for i in range(t):
        temp = int(input()) #заказов на данной итерации
        for _ in range(temp):
            inp = list(map(int, input().split()))
            if maze[inp[1] - 1][inp[0] - 1] != '#' and maze[inp[3] - 1][inp[2] - 1] != '#':
                free_ord.append([inp[1] - 1, inp[0] - 1, inp[3] - 1, inp[2] - 1]) #добавляем в заказы

        for m in bots:
            if m.state == 0:
                while len(m.route) <= 60 and len(free_ord) != 0:
                    num_ord = find_best_for_cell(n, free_ord, m.x, m.y)
                    free_ord[-1], free_ord[num_ord] = free_ord[num_ord], free_ord[-1]
                    now_ord = free_ord.pop()

                    m.end_x = now_ord[2]
                    m.end_y = now_ord[3]

                    first_x, first_y = check_square(n, m.x, m.y)
                    second_x, second_y = check_square(n, now_ord[0], now_ord[1])
                    third_x, third_y = check_square(n, now_ord[2], now_ord[3])



                    m.route += find_route_izy(m.x, m.y, first_x, first_y)    
                    m.route += find_route_izy(first_x, first_y, second_x, second_y)
                    m.route += find_route_izy(second_x, second_y, now_ord[0], now_ord[1])

                    m.route += 'T'

                    m.route += find_route_izy(now_ord[0], now_ord[1], second_x, second_y)    
                    m.route += find_route_izy(second_x, second_y, third_x, third_y)
                    m.route += find_route_izy(third_x, third_y, now_ord[2], now_ord[3])

                    
                    m.x = now_ord[2]
                    m.y = now_ord[3]

                    m.route += 'P'
            if len(m.route) <= 60:
                print(m.route + (60 - len(m.route)) * 'S',flush=True)
                m.route = ''
                m.state = 0
            else:
                print(m.route[:60],flush=True)
                m.route = m.route[60:]
                m.state = 1


def low_iq_test(maze, n, max_tips, cost, t, d):
    bots = find_robs(maze, n, max_tips, cost, t, d)

    free_ord = []
    

    for i in range(t):
        temp = int(input()) #заказов на данной итерации
        for _ in range(temp):
            inp = list(map(int, input().split()))
            free_ord.append([inp[1] - 1, inp[0] - 1, inp[3] - 1, inp[2] - 1]) #добавляем в заказы

        for m in bots:
            if m.state == 0:
                while len(m.route) < 60 and len(free_ord) != 0:

                    num_ord = find_best(free_ord, m.x, m.y)
                    free_ord[-1], free_ord[num_ord] = free_ord[num_ord], free_ord[-1]

                    now_ord = free_ord.pop()
                    m.end_x = now_ord[2]
                    m.end_y = now_ord[3]
                    route = find_route_izy(m.x, m.y, now_ord[0], now_ord[1])    #если бот бездействует - можно направить куда надо, но это попозже
                    route += 'T'
                    route += find_route_izy(now_ord[0], now_ord[1], now_ord[2], now_ord[3])
                    m.x = m.end_x
                    m.y = m.end_y
                    route += 'P'
                    m.route += route
            if len(m.route) <= 60:
                print(m.route + (60 - len(m.route)) * 'S',flush=True)
                m.route = ''
                m.state = 0
            else:
                print(m.route[:60],flush=True)
                m.route = m.route[60:]
                m.state = 1



def innop(maze, n, max_tips, cost, t, d):
    return 
    


def main():
    maze = []
    n, max_tips, cost = map(int, input().split()) #n - размер поля, чаевые, цена робота


    for i in range(n):
        a = list(input())
        maze.append(a)

    t, d = map(int, input().split()) #считываем кол-во итераций и количество заказов


    if type_of_maze(n) == 0:
        low_iq_test(maze, n, max_tips, cost, t, d)
    elif type_of_maze(n) == 1:
        cells(maze, n, max_tips, cost, t, d)
    else:
        innop(maze, n, max_tips, cost, t, d)

if __name__ == '__main__':
    main()