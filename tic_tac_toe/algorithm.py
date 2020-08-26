def update_state(curr, r, c, v):
    curr[r * 3 + c] = get_symbol(v)
    return not v


def get_symbol(v):
    return 'X' if v else 'O'


def gen_moves(curr, v):
    s = get_symbol(v)
    poss_moves = []
    for i, x in enumerate(curr):
        if x == -1:
            poss_moves.append(curr[:])
            poss_moves[-1][i] = s
    return poss_moves


def is_won(curr: list):
    for i in range(3):
        if curr[3 * i + 0] == curr[3 * i + 1] == curr[3 * i + 2] != -1: return True
        if curr[0 + i] == curr[3 + i] == curr[6 + i] != -1: return True
    return curr[0] == curr[4] == curr[8] != -1 or curr[2] == curr[4] == curr[6] != -1


def is_draw(curr: list):
    return -1 not in curr


def final_score(curr):
    res = 0
    for x in curr:
        if x == -1: res += 1
    return res


def find_best_move(curr, is_ai, v):
    if is_won(curr): return curr, final_score(curr) if is_ai else -final_score(curr)
    if is_draw(curr): return curr, 0
    poss_moves = gen_moves(curr, v)
    b = -10 if is_ai else 10
    next_move = None
    for move in poss_moves:
        _, score = find_best_move(move, not is_ai, v)
        if score > b and is_ai:
            next_move, b = move, score
        elif score < b and not is_ai:
            next_move, b = move, score
    return next_move, b


def display(curr):
    for i in range(9):
        if i % 3 == 0: print()
        if curr[i] == -1:
            print("_", end="\t")
        else:
            print(curr[i], end="\t")
    print(end="\n")


def take_user_input(b):
    r = int(input("Enter row number : "))
    c = int((input("Enter column number : ")))
    while not (0 <= r <= 2 and 0 <= c <= 2) or b[3 * r + c] != -1:
        print(" Invalid input ")
        r = int(input("Enter row number : "))
        c = int((input("Enter column number : ")))
    return r, c


def play():
    b, v = [-1] * 9, True
    print(" Welcome to Tic tac Toe Game :  (numbers are 0 indexed)")
    display(b)
    s = input("Do you want to play first True/False : ")
    x = True if s == "True" else False
    while True:
        if x:
            r, c = take_user_input(b)
            v = update_state(b, r, c, v)
            display(b)
        else:
            b, s = find_best_move(b, True, v)
            v = not v
            print("score : ", s)
            display(b)
        if is_won(b):
            print("{} has own !".format("Computer" if not x else "Player"))
            return
        if is_draw(b):
            print("Match is drawn")
            return
        x = not x


play()
