import itertools
import pandas as pd
import xlwings as xw
import random
from pathlib import Path
import sys


## <1> find Last order of Lotto645 
LOTTO_NUMS_FILE = "Lotto645_won_1015.xlsx"
Latest = 5  # 최근 * 당첨번호만 수집 
GAMES = 40000  # 게임 수

# 최종 회차의 숫자부 알아내기 
fn_f = "Lotto645_won_"
fn_tmp = LOTTO_NUMS_FILE[-len(LOTTO_NUMS_FILE) : -5]   # 파일이름에서 .xlsx 제거하기 
End_order = int(fn_tmp[len(fn_f) : len(fn_tmp)])       # Lotto645 최신 회차 
Start_order = End_order - Latest + 1 


## <2> indexing each lotton645 number
this_dir = Path(__file__).resolve().parent
wb = xw.Book(f"{this_dir}\{LOTTO_NUMS_FILE}")
ws = wb.sheets[0]
df = ws["a1"].expand().options(pd.DataFrame).value
wb.app.quit()


## <3> case_combi가 -1인 Data만 선별하여 별도의 DataFrame을 생성 
df1 = df.loc[df["case_combi"] == -1, :]    # 회차는 index column이 됨
n = len(df1)

combi_list = []
if n != 0:
    print("Indexing Lotto645 numbers")
    
    ## <4> Processing
    df2 = df1.iloc[:,1:7]        
    df2 = df2.astype(dtype=int)  # data를 정수화
    df2 = df2.reset_index()      # index를 data에 포함시킴

    lotto_dict = {}
    while n >= 1:    # make the dictionary datatype
        lotto_dict[df2.iloc[n-1, 0]] = list(df2.iloc[n-1, 1:7])
        n -= 1

    ## <5> Make the combination list  for 6/45 and convert to dictionary datatype
    combi_list = list(itertools.combinations(range(1,46),6))
    combi_dict = {}
    for i, nums in enumerate(combi_list):
        combi_dict[i] = nums                # make the dictionary datatype
        i += 1 

    for idx, lotto_nums in lotto_dict.items():
        for key, values in combi_dict.items():
            if list(values) == list(lotto_nums): # lotto_nos:
                df.loc[idx, "case_combi"] = key

    df.to_excel(f"{this_dir}\{LOTTO_NUMS_FILE}")


## <6> Lotto file의 Data를 filtering 함
df2 = df.iloc[:,1:9]  # Lotto file에서 case_combi를 포함한 dataframe을 만듦
df2 = df2.reset_index()
df2 = df2.astype(dtype=int)


## <7> 당첨번호에 해당되는 dictionary data를 만든다 
rows = len(df2)
lotto_dict = {}
n = 0
while n < rows:
    lotto_dict[df2.iloc[n, 8]] = list(df2.iloc[n, 1:7]) # make the dictionary datatype 
    n += 1


## <9> 이전 회수까지 중복된 set가 있었는지 확인 
print('동일하지 않은 당첨번호가 나온 횟수: ', len(set(lotto_dict.keys() )))


## <10> Start process for Lucky number picking 
wb = xw.Book(f"{this_dir}\{LOTTO_NUMS_FILE}")
ws = wb.sheets[0]
df = ws["a1"].expand().options(pd.DataFrame).value
df = df.sort_index()
wb.app.quit()

df1 = df.loc[:, "n1":"case_combi"]
df2 = df1.loc[Start_order : End_order + 1, :]
df2 = df2.astype(dtype=int)


## <11> 불러온 dataframe의 숫자 전체를 1차원 list data로 변환
num45s_list = [ ]
n = Start_order

while n <= End_order:
    num45s_list.append(list(df2.loc[n, "n1":"nbo"]))
    n += 1


## <12> 이전 회수에서 뽑힌 숫자들과 그렇지 않을 숫자를 구분해 줌 
nums_sel = []
for row in num45s_list:    
    for element in row:
        nums_sel.append(element)

nums_sel = set(nums_sel)
nums_non_sel = set(range(1,46)) - set(nums_sel)
        
print('선택된 번호:', nums_sel)
print('선택되지 않은 번호:', nums_non_sel)

## <13> 이전 회수에서 선택된 번호와 뽑히지 않은 번호를 조합하여 1set를 만듦 
i = 0
n = random.choice(range(2,5))      # 전회에서 뽑힌 번호 중 몇개를 섞을 것인지 random (2,3,4)으로 결정 
print('전회 번호와 중북번호 사용 수:', n)
games_list = []

while i < GAMES:
    a_game = random.sample(list(nums_sel), n) + random.sample(list(nums_non_sel), 6 - n)
    a_game.sort()
    games_list.append(a_game)
    i += 1

## <14> Excel 파일로 출력 
games_df = pd.DataFrame(games_list)
next_order = End_order + 1
games_df.to_excel((f"{this_dir}\For_Lotto645_{next_order}.xlsx"))

sys.exit("Completed")