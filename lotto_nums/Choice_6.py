import random
from math import perm, comb
import sys

balls_list = [4, 11, 14, 16, 18, 22, 27, 28, 30, 34, 36, 37, 39, 42, 43, 44]
GAMES = 20

if GAMES > comb(len(balls_list), 6): 
    sys.exit("원하는 게임수가 선택 가능한 경우의 수보다 큽니다.")
    
i = 0
games_list = []
while i < GAMES:
    random.shuffle(balls_list)                      # 미리 한번 섞어주고, 선택에서 다시 섞어줌
    agame_list = random.sample(balls_list, k=6)     # 6개의 볼을 선택함 
    agame_list.sort()
    games_list.append(agame_list)
    i += 1

# games_list.sort()

for i, a_list in enumerate(games_list):
    if (i % 5) == 0:
        print('---------------------------')
    print(f"{i} : {a_list}")
    i += 1