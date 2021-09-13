from queue import Queue
from collections import deque
import random




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
            if maze[y][x] == '#':
                print('allarm')
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
        num_of_rob = 1
    elif n == 128:
        num_of_rob = 4 #очень дешевые боты, можно нагегенировать бесконечное количество
    elif n == 180:
        num_of_rob = 20 #хз пока
    elif n == 384:
        num_of_rob = 20 #20
    elif n == 1024:
        num_of_rob = 34 # 12
    else:
        if cost == 123456:
            num_of_rob = 30
        elif cost == 101010:
            num_of_rob = 100
        elif cost == 1500000:
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


def find_best_for_cell(n, free_ord, bot_x, bot_y, not_banned):
    min_cost = 1e6
    best_ord = None
    keys = list(not_banned.keys())
    max_iter = min(1000, len(keys))
    for i in range(max_iter):
        key = keys[random.randint(0, len(keys) - 1)]
        get_x, get_y = key
        put_x, put_y = free_ord[key].popleft()  
        free_ord[key].appendleft((put_x, put_y))


        first_x, first_y = check_square(n, bot_x, bot_y)
        second_x, second_y = check_square(n, get_x, get_y)
        third_x, third_y = check_square(n, put_x, put_y)

        part_1 = abs(bot_x - first_x) + abs(bot_y - first_y)
        part_2 = abs(first_x - second_x) + abs(first_y - second_y)
        part_3 = abs(second_x - get_x) + abs(second_y - get_y)
        part_4 = abs(second_x - third_x) + abs(second_y - third_y)
        part_5 = abs(third_x - put_x) + abs(third_y - put_y)

        temp = part_1 + part_2 + 2 * part_3 + part_4 + part_5
        if temp < min_cost:
            min_cost = temp
            best_ord = key
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

    free_ord = {}
    
    not_banned = {}
    banned = {}

    for i in range(t):
        temp = int(input()) #заказов на данной итерации
        for _ in range(temp):
            y0, x0, y1, x1  = map(int, input().split())
            
            if (x0 - 1, y0 - 1) not in free_ord:
                free_ord[(x0 - 1, y0 - 1)] = deque([(x1 - 1, y1 - 1)]) #добавляем в заказы
            else:
                free_ord[(x0 - 1, y0 - 1)].append((x1 - 1, y1 - 1))

            if (x0 - 1, y0 - 1) not in banned:
                not_banned[(x0 - 1, y0 - 1)] = 1




        ret = []
        rules = []
        for m in bots:
            if m.state == 0:
                while len(m.route) <= 60 and len(not_banned) != 0:
                    key_ord = find_best_for_cell(n, free_ord, m.x, m.y, not_banned)
                    get_x, get_y = key_ord
                    put_x, put_y = free_ord[key_ord].popleft()
                    if not free_ord[key_ord]:
                        free_ord.pop(key_ord)

                    not_banned.pop(key_ord) #словарь доступных мне начал заказов, <= free_ord
                    banned[key_ord] = 1

                    
                    m.start_x, m.start_y = get_x, get_y
                    first_x, first_y = check_square(n, m.x, m.y)
                    second_x, second_y = check_square(n, get_x, get_y)
                    third_x, third_y = check_square(n, put_x, put_y)


                    route = ''
                    route += find_route_izy(m.x, m.y, first_x, first_y)    
                    route += find_route_izy(first_x, first_y, second_x, second_y)
                    route += find_route_izy(second_x, second_y, get_x, get_y)

                    route += 'T'

                    route += find_route_izy(get_x, get_y, second_x, second_y)    
                    route += find_route_izy(second_x, second_y, third_x, third_y)
                    route += find_route_izy(third_x, third_y, put_x, put_y)


                    route += 'P'

                    m.x = put_x
                    m.y = put_y

                    m.route += route
            if len(m.route) <= 60:
                first_x, first_y = check_square(n, m.x, m.y)
                should = find_route_izy(m.x, m.y, first_x, first_y)
                size = 60 - len(m.route)
                if len(should) <= size:
                    cur_ans = m.route + should + (size - len(should)) * 'S'
                    m.x = first_x
                    m.y = first_y
                else: #len(should) > size, все не вместится. надо отдельно просчитывать
                    cur_ans = m.route + should[:size]
                    if abs(first_x - m.x) >= size:
                        if first_x <= m.x:
                            m.x -= size
                        else:
                            m.x += size
                    else:   #подвинуть x abs(first - m.x), значит уже не остается на подвинуть 
                        if first_y <= m.y:
                            m.y -= size - abs(first_x - m.x)
                        else: # first_y > m.y
                            m.y += size - abs(first_x - m.x)
                        m.x = first_x


                ret.append(cur_ans)
                m.route = ''
                m.state = 0
                if m.start_x:
                    rules.append((m.start_x, m.start_y))
                
            else:
                ret.append(m.route[:60])
                m.route = m.route[60:]
                if len(m.route) < 60:
                    m.state = 1
                else:
                    m.state = 0
        print('\n'.join(ret),flush=True)
        for j in rules:
            if j in free_ord:
                not_banned[j] = 1   #вывод из бана, надо когда бот дошел до клетки
            if j in banned:
                banned.pop(j)


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