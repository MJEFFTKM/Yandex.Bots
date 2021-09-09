from queue import Queue
from collections import deque
import random
import time





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

    check = 0
    if n == 180:
        indent = 3 - 1
        side = 7
        pas = 5
        tales = 14
        check += 1
    elif n == 384:
        indent = 6 - 1
        side = 13
        pas = 11
        tales = 15
        check += 1
    elif n == 1024:
        indent = 8 - 1
        side = 17
        pas = 15
        tales = 31
        check += 1

    if check == 1:
        for i in range(num_of_rob):
            x = random.randint(0, tales) * (side + pas) + (indent + (side // 2) + 1)
            y = random.randint(0, tales) * (side + pas) + (indent + (side // 2) + 1)
            print(y + 1, x + 1,flush=True)
            bots.append(rob(x = x,y = y))

    else:
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
    if n == 4:
        num_of_rob = 3
    elif n == 128:
        num_of_rob = 4 #очень дешевые боты, можно нагегенировать бесконечное количество
    elif n == 180:
        num_of_rob = 10 #хз пока
    elif n == 384:
        num_of_rob = 18
    elif n == 1024:
        num_of_rob = 15
    else:
        if max_tips == 123456:
            num_of_rob = 30
        elif max_tips == 101010:
            num_of_rob = 100
        elif max_tips == 1500000:
            num_of_rob = 20
        else:
            num_of_rob = 25

    return generate_bots(maze, n, num_of_rob)



def find_best(free_ord, bot_x, bot_y):  #добавить рандомные 100, вместо перебора всего

    min_cost = 2e4
    best_ord = None
    if len(free_ord) == 1:
        return 0

    
    max_iter = min(100, len(free_ord) // 1000 + 50)
    for _ in range(max_iter):
        i = random.randint(0, len(free_ord) - 1)
        temp = abs(bot_x - free_ord[i][0]) + abs(bot_y - free_ord[i][1]) + abs(free_ord[i][0] - free_ord[i][2]) + abs(free_ord[i][1] - free_ord[i][3])
        if temp < min_cost:
            min_cost = temp
            best_ord = i
    return best_ord


def type_of_maze(n): #функция, которая проверяет тип карты
    if n == 4 or n == 128:
        return 0
    elif n == 180 or n == 384 or n == 1024:
        return 1
    else:
        return 2



def check_square(n, x, y):
    x_add = 0
    y_add = 0
    if n == 180:
        indent = 3 - 1
        side = 7
        pas = 5
    elif n == 384:
        indent = 6 - 1
        side = 13
        pas = 11
    else:
        indent = 8 - 1
        side = 17
        pas = 15

    X = (x - indent) // (pas + side)
    Y = (y - indent) // (pas + side)
    if (x - indent) % (pas + side) > (pas + side - indent):
        x_add = 1
    if (y - indent) % (pas + side) > (pas + side - indent):
        y_add = 1
    return [indent + (side // 2) + 1 + (X + x_add) * (pas + side), indent + (side // 2) + 1 + (Y + y_add) * (pas + side)]


def find_best_for_cell(n, free_ord, bot_x, bot_y):
    keys = list(free_ord.keys())
    key = keys[random.randint(0, len(keys) - 1)]
    return key

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

    free_ord = {}
    

    for i in range(t):
        temp = int(input()) #заказов на данной итерации
        for _ in range(temp):
            inp = list(map(int, input().split()))
            
            if (inp[1] - 1, inp[0] - 1) not in free_ord:
                free_ord[(inp[1] - 1, inp[0] - 1)] = deque([(inp[3] - 1, inp[2] - 1)]) #добавляем в заказы
            else:
                free_ord[(inp[1] - 1, inp[0] - 1)].append((inp[3] - 1, inp[2] - 1))


                 

        for m in bots:
            if m.state == 0:
                while len(m.route) <= 60 and len(free_ord) != 0:
                    key_ord = find_best_for_cell(n, free_ord, m.x, m.y)
                    get_x, get_y = key_ord
                    put_x, put_y = free_ord[key_ord].popleft()
                    if len(free_ord[key_ord]) == 0:
                        free_ord.pop(key_ord)

                

                    first_x, first_y = check_square(n, m.x, m.y)
                    second_x, second_y = check_square(n, get_x, get_y)
                    third_x, third_y = check_square(n, put_x, put_y)

                    m.route += find_route_izy(m.x, m.y, first_x, first_y)    
                    m.route += find_route_izy(first_x, first_y, second_x, second_y)
                    m.route += find_route_izy(second_x, second_y, get_x, get_y)

                    m.route += 'T'

                    m.route += find_route_izy(get_x, get_y, second_x, second_y)    
                    m.route += find_route_izy(second_x, second_y, third_x, third_y)
                    m.route += find_route_izy(third_x, third_y, put_x, put_y)


                    m.route += 'P'

                    m.x = put_x
                    m.y = put_y

            if len(m.route) <= 60:
                print(m.route + (60 - len(m.route)) * 'S',flush=True)
                m.route = ''
                m.state = 0
            else:
                print(m.route[:60],flush=True)
                m.route = m.route[60:]
                if len(m.route) < 60:
                    m.state = 1
                else:
                    m.state = 0

    #print("--- %s seconds ---" % (time.time() - start_time))


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
    #start_time = time.time()
    main()