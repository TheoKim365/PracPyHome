import itertools
import pandas as pd
import numpy as np
import xlwings as xw
import random
from pathlib import Path
import sys


## <1> find Last order of Lotto645 
LOTTO_NUMS_FILE = "Lotto645_won_996.xlsx"
GAMES = 200
end_order = int(LOTTO_NUMS_FILE[13:16])  # Lotto645 최근 회차
start_order = 836  # 2018.12.08 ~ (나눔로또 => 동행복권)


## <2> indexing each lotton645 number
this_dir = Path(__file__).resolve().parent
wb = xw.Book(f"{this_dir}\{LOTTO_NUMS_FILE}")
ws = wb.sheets[0]
df = ws["a1"].expand().options(pd.DataFrame).value
wb.app.quit()


# <3> case_combi가 -1인 Data만 선별하여 별도의 DataFrame을 생성 
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

# print(lotto_dict)
# sys.exit()


## <1> 위에서 Combination (6/45)를 만들었는지 확인하여 만들지 않았으면 
## Make the combination list  for 6/45 and convert to dictionary datatype
if len(combi_list) == 0:
    combi_list = list(itertools.combinations(range(1,46),6))
    combi_dict = {}
    for i, nums in enumerate(combi_list):
        combi_dict[i] = nums    # make the dictionary datatype
        i += 1    


## <6> combi_dict의 key로 이루어진 combi_set을 만들고 
#      lotto_dict의 key로 만들어진 lotto_set와 차를 구한다 
combi_set = set(combi_dict.keys())
lotto_set = set(lotto_dict.keys())

nonsel_set = combi_set.difference(lotto_set)
# nonsel_list = list(nonsel_set)
print(len(combi_set) - len(nonsel_set))  # 이미 선정된 Lotto 번호 경우의 수를 확인 
# sys.exit("임시 종료")
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

df2 = df1.loc[start_order : end_order, :]
df2 = df2.astype(int)

# print(df)
# print(df1)
# print(df2)
# sys.exit("임시 종료2")

## <2> 불러온 dataframe의 숫자 전체를 1차원 list data로 변환
num45s_list = [ ]
n = start_order
while n <= end_order:
    num45s_list.append(list(df1.loc[n, "n1":"n6"]))
    n += 1


## <3> for 문을 활용하여 모수 중에서
# dictionary data의 key 값에 해당하는 data 수(n) 를 확인하고
# key 값에 해당하는 data (n)에 +을 한다 
num45s_dict = {}
for k in range(1,46):       # 1~45번호에 대한 count를 초기화 
    num45s_dict[k] = 0   

for row in num45s_list:     # 1~45공이 나온 회수를 count
    for element in row:
        counter = num45s_dict[element]
        num45s_dict[element] = counter + 1
print(num45s_dict)

## <5> dictionary data를 작성한 후 weight factor를 고려한 list data 만들기 
num45wgt_list = [ ]
for num, picks_count in num45s_dict.items():
    k = 0
    m = (picks_count / 10) ** 5 + 1   # m = np.int32(picks_count ** 5 / 100000) + 1

    while k < m:
        num45wgt_list.append(num)
        k += 1
# random.shuffle(num45wgt_list)
# print(num45wgt_list)
# sys.exit("임시 종료")


## <6> list data에서 6개를 뽑고, 이미 뽑은 수와 중복되면 버리고 다시 뽑음 
# set data와 difference method 적용 
# set를 count하여 6개의 각기 다른 수가 될 때까지 sampling 함

i = 0
games_list = []
while i < GAMES:
    ballbox_list = num45wgt_list  # 원본은 유지하고 사본 list를 만듦. 
    agame_list = []
    while True:
        random.shuffle(ballbox_list)  # 미리 한번 섞어주고, choices에서 다시 섞어줌
        tmp_list = random.choices(ballbox_list, k=1)  # list의 다수의 요소를 가져옴, 원본 변경
        agame_list = agame_list + tmp_list
        agame_set = set(agame_list)
      
        if len(agame_set) == 6:
            agame_list = list(agame_set)
            agame_list.sort()
            break
   
    games_list.append(agame_list)
    i += 1

# games_list.sort()
games_df = pd.DataFrame(games_list)
next_order = end_order + 1
games_df.to_excel((f"{this_dir}\For_Lotto645_{next_order}.xlsx"))

sys.exit("Completed")

# ## <8> game_list를 excel file로 출력
# games_list


## <7> pick_list 전체를 sorting해서 출력하는 방법 강구 
for i, a_list in enumerate(games_list):
    if (i % 5) == 0:
        print('---------------------------')
    print(f"{i} : {a_list}")
    i += 1


## <9> 기존의 lotto645 선정과 값과 비교하여 동일한 경우(개수)는 새로 뽑기 
# 일부 다시 뽑기 위해 <6>프로시져를 이용하는 "함수"를 사용할 필요성 있음 
# for i, a_list in enumerate(games_list):
#    # 이전 프로시져 재활용 ... 
#    # dataframe을 dictionary datatype으로 저장하여 games_list와 비교 
#    i += 1

sys.exit("Completed")