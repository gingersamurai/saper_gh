import random

save_cnt = 0
row_cnt = int()
str_cnt = int()
bomb_cnt = int()
bombs = []
field_user_see = [] 
# 0 close 1 flag 2 used
field_bomb_near = []
field_used = []


def gen(user_row_cnt, user_str_cnt, user_bomb_cnt):
    global row_cnt
    global str_cnt
    global bomb_cnt
    global field_bomb_near
    global field_user_see
    global field_used
    global bombs
    row_cnt = user_row_cnt
    str_cnt = user_str_cnt
    bomb_cnt = user_bomb_cnt
    bombs = gen_bombs()
    field_user_see = [[0 for i in range(row_cnt)] for j in range(str_cnt)]
    field_bomb_near = [[0 for i in range(row_cnt)] for j in range(str_cnt)]
    field_used = [[0 for i in range(row_cnt)] for j in range(str_cnt)]
    gen_bomb_near()

def gen_bombs():
    pret = []
    res = []
    for y in range(str_cnt):
        for x in range(row_cnt):
            pret.append([y, x])
    for _ in range(bomb_cnt):
        res_now = random.choice(pret)
        res.append(res_now)
        pret.pop(pret.index(res_now))
    return res

def gen_bomb_near():
    global field_bomb_near
    for y in range(str_cnt):
        for x in range(row_cnt):
            if [y, x] in bombs:
                field_bomb_near[y][x] = -1
                continue
            cnt = 0
            for yp in range(y-1, y+2):
                for xp in range(x-1, x+2, 1):
                    if min(xp, yp) < 0 or xp >= row_cnt or yp >= str_cnt:
                        continue
                    cnt += [yp, xp] in bombs
            field_bomb_near[y][x] = cnt
    

def dbg_print():
    print(bombs)
    print("user_see")
    for i in field_user_see:
        print(i)
    print("bombs_near")
    for i in field_bomb_near:
        print(i)
    print()

def print_field():
    for y in range(str_cnt):
        for x in range(row_cnt):
            if field_user_see[y][x] == 0:
                print('*', end=" ")
            elif field_user_see[y][x] == 1:
                print('F', end=" ")
            else:
                print(field_bomb_near[y][x], end=" ")
        print()
    print()

def make_act(x, y, act):
    if act == 1:
        if field_user_see[y][x] == 0:
            field_user_see[y][x] = 1
        elif field_user_see[y][x] == 1:
            field_user_see[y][x] = 0
        return True
    elif act == 2:
        if [y, x] in bombs:
            print('проигрыш')
            for y in range(str_cnt):
                for x in range(row_cnt):
                    if field_bomb_near[y][x] == -1:
                        print('B', end=" ")
                    else: 
                        print(field_bomb_near[y][x], end=" ")
                print()
            return False
        else:
            field_user_see[y][x] = 2
            if field_bomb_near[y][x] == 0:
                dfs(y, x)
            return True

def dfs(y, x):
    field_used[y][x] = 1
    if field_bomb_near[y][x] > 0:
        return
    field_user_see[y][x] = 2
    if y > 0 and not field_used[y-1][x]:
        dfs(y-1, x)
    if x > 0 and not field_used[y][x-1]:
        dfs(y, x-1)
    if y+1 < str_cnt and not field_used[y+1][x]:
        dfs(y+1, x)
    if x+1 < row_cnt and not field_used[y][x+1]:
        dfs(y, x+1)

def save(save_num):
    global save_cnt
    global row_cnt
    global str_cnt
    global bomb_cnt
    global field_bomb_near
    global field_user_see
    global field_used
    global bombs
    save_cnt += 1
    save_file = open(f's{save_num}.txt', 'x')
    save_file.write(f'{row_cnt}\n')
    save_file.write(f'{str_cnt}\n')
    save_file.write(f'{bomb_cnt}\n')
    for i in field_bomb_near:
        for j in i:
            save_file.write(f'{j} ')
        save_file.write('\n')
    save_file.write('\n')
    for i in field_user_see:
        for j in i:
            save_file.write(f'{j} ')
        save_file.write('\n')
    save_file.write('\n')
    for i in field_used:
        for j in i:
            save_file.write(f'{j} ')
        save_file.write('\n')
    save_file.write('\n')
    for i in bombs:
        for j in i:
            save_file.write(f'{j} ')
        save_file.write('\n')
    save_file.write('\n')

def load(save_num):
    global save_cnt
    global row_cnt
    global str_cnt
    global bomb_cnt
    global field_bomb_near
    global field_user_see
    global field_used
    global bombs
    save_file = open(f's{save_num}.txt')
    row_cnt = int(save_file.readline())
    str_cnt = int(save_file.readline())
    bomb_cnt = int(save_file.readline())
    print(row_cnt, str_cnt, bomb_cnt)
    field_bomb_near.clear()
    for i in range(str_cnt):
        field_bomb_near.append(list(map(int, save_file.readline().split())))
    print(field_bomb_near)
    field_user_see.clear()
    save_file.readline()
    for i in range(str_cnt):
        field_user_see.append(list(map(int, save_file.readline().split())))
    print(field_user_see)
    field_used.clear()
    save_file.readline()
    for i in range(str_cnt):
        field_used.append(list(map(int, save_file.readline().split())))
    print(field_used)
    bombs.clear()
    save_file.readline()
    for i in range(bomb_cnt):
        y, x = map(int, save_file.readline().split())
        bombs.append([y, x])
    print(bombs)
    