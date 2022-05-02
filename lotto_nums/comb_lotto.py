import itertools
import pandas as pd
import numpy as np
import xlwings as xw
import random
from pathlib import Path
import sys


# a = list(range(1,46))
# a = range(1,46)
# b = [4,5,6]
# c = list(set(a) - set(b))
# print(c)
# sys.exit('일시정지')


## <1> find Last order of Lotto645 
LOTTO_NUMS_FILE = "Lotto645_won_1012.xlsx"
latest = 5  # 최근 * 당첨번호만 수집 
GAMES = 20  # 게임 수

# 최종 회차의 숫자부 알아내기 
fn_f = "Lotto645_won_"
fn_tmp = LOTTO_NUMS_FILE[-len(LOTTO_NUMS_FILE) : -5]   # 파일이름에서 .xlsx 제거하기 
end_order = int(fn_tmp[len(fn_f) : len(fn_tmp)])       # Lotto645 최신 회차 
start_order = end_order - latest + 1 


## <2> indexing each lotton645 number
this_dir = Path(__file__).resolve().parent
wb = xw.Book(f"{this_dir}\{LOTTO_NUMS_FILE}")
ws = wb.sheets[0]
df = ws["a1"].expand().options(pd.DataFrame).value
wb.app.quit()


## <3> case_combi가 -1인 Data만 선별하여 별도의 DataFrame을 생성 
df1 = df.loc[df["case_combi"] == -1, :]
n = len(df1)
combi_list = []
if n != 0:
    print("Doing indexing of Lotto645 numbers")
    
    ## <4> Make the combination list  for 6/45 and convert to dictionary datatype
    combi_list = list(itertools.combinations(range(1,46),6))

    combi_dict = {}
    for i, nums in enumerate(combi_list):
        combi_dict[i] = nums    # make the dictionary datatype
        i += 1    

    ## <5> Processing
    df2 = df1.iloc[:,1:7]
    df2 = df2.astype(dtype=int)  # data를 정수화
    df2 = df2.reset_index()      # index를 data에 포함시킴

    lotto_dict = {}
    while n >= 1:    # make the dictionary datatype
        lotto_dict[df2.iloc[n-1, 0]] = list(df2.iloc[n-1, 1:7])
        n -= 1

    lotto_sum = {}
    for idx, lotto_nums in lotto_dict.items():
        lotto_nos = list(lotto_nums)

        for key, values in combi_dict.items():
            if list(values) == lotto_nos:
                df.loc[idx, "case_combi"] = key
    # print(df)

    df.to_excel(f"{this_dir}\{LOTTO_NUMS_FILE}")

# ================로또번호가 이전에 중복되었는지 여부를 판별하기 위해 전체 회차 수를 출력 ===========
## <4> Lotto file의 Data를 filtering 함
df2 = df.iloc[:,1:9]  # Lotto file에서 case_combi를 포함한 dataframe을 만듦
df2 = df2.reset_index()
df2 = df2.astype(dtype=int)


## <5> 당첨번호에 해당되는 dictionary data를 만든다 
rows = len(df2)
lotto_dict = {}

n = 0
while n < rows:
    lotto_dict[df2.iloc[n, 8]] = list(df2.iloc[n, 1:7]) # make the dictionary datatype 
    n += 1


## <1> 위에서 Combination (6/45)를 만들었는지 확인하여 만들지 않았으면 
## Make the combination list  for 6/45 and convert to dictionary datatype
if len(combi_list) == 0:
    combi_list = list(itertools.combinations(range(1,46),6))
    combi_dict = {}
    for i, nums in enumerate(combi_list):
        combi_dict[i] = nums    # make the dictionary datatype
        i += 1    


## <6> # 이미 선정된 Lotto 번호 경우의 수를 확인 
print(len(set(combi_dict.keys()) - (set(combi_dict.keys()) - set(lotto_dict.keys()) )))
# =====================================================================================


## <a1> Start process for Lucky number picking 
wb = xw.Book(f"{this_dir}\{LOTTO_NUMS_FILE}")
ws = wb.sheets[0]
df = ws["a1"].expand().options(pd.DataFrame).value
# df.index = df.index.astype(int)
df = df.sort_index()
wb.app.quit()

df1 = df.loc[:, "n1":"case_combi"]
df1 = df1.astype(int)

df2 = df1.loc[start_order : end_order + 1, :]
df2 = df2.astype(int)


## <2> 불러온 dataframe의 숫자 전체를 1차원 list data로 변환
num45s_list = []
n = start_order
while n <= end_order:
    num45s_list.append(list(df1.loc[n, "n1":"nbo"]))
    n += 1

sel_num45s = []
for row in num45s_list:
    for element in row:
        sel_num45s.append(element)

sel_num45s = list(set(sel_num45s))
non_sel_num45s = list(set(range(1,46)) - set(sel_num45s))


print('selected numbers :' + str(sel_num45s))
print('non selected numbers :' + str(non_sel_num45s))
# sys.exit('일시정지')

i = 0
games_list =[]
while i < GAMES: 
    a_game = random.sample(sel_num45s, 3) + random.sample(non_sel_num45s,3)
    a_game.sort()
    games_list.append(a_game)
    i += 1

games_list.sort()

games_df = pd.DataFrame( games_list)
next_order = end_order + 1
games_df.to_excel((f"{this_dir}\For_Lotto645_{next_order}.xlsx"))

sys.exit("Completed")