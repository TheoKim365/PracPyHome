import itertools
import pandas as pd
import xlwings as xw
from pathlib import Path
import random
import sys


LOTTO_NUMS_FILE = "Lotto645_won_994.xlsx"
GAMES = 20


## <2> indexing each lotton645 number
this_dir = Path(__file__).resolve().parent
wb = xw.Book(f"{this_dir}\{LOTTO_NUMS_FILE}")
ws = wb.sheets[0]
df = ws["a1"].expand().options(pd.DataFrame).value
df.index = df.index.astype(int)
wb.app.quit()

# df5 = df.reset_index()
# print(df5)
# sys.exit()

# <3> case_combi가 -1인 Data가 있으면 실행을 중지하고 회차를 알려 줌
df1 = df.loc[df["case_combi"] == -1, :]
non_index = len(df1)   # "case_combi"가 -1인 data_list만 선별하여 data 개수 count 
if non_index > 0:
    print("** Indexing 되지 않은 Data 행은:")
    print(df1)
    sys.exit("=> Data indexing is required")


## <4> Lotto file의 Data를 filtering 함
df2 = df.iloc[:,1:9]  # Lotto file에서 case_combi를 포함한 dataframe을 만듦
df2 = df2.reset_index()
df2 = df2.astype(dtype=int)


## <5> 당첨번호에 해당되는 dictionary data를 만든다 
rows = len(df2)
lotto_dict = {}

# print(df2)
# print(df2.iloc[0, 8])
# sys.exit()


n = 0
while n < rows:
    lotto_dict[df2.iloc[n, 8]] = list(df2.iloc[n, 1:7]) # make the dictionary datatype 
    n += 1

# print(lotto_dict)
# sys.exit()


## <1> Make the combination list  for 6/45 and convert to dictionary datatype
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
nonsel_list = list(nonsel_set)
print(len(combi_set) - len(nonsel_set))  # 이미 선정된 Lotto 번호 경우의 수를 확인

## <7> subset을 이용하여 조합을 만듦
random.shuffle(nonsel_list)
combisub_list = random.choices(nonsel_list, k=GAMES)  # GAMES : 뽑고자 하는 게임 수
# combisub_list.sort()


## <8> case_combi에 해당되는 조합의 List (원하는 게임 수)를 출력
for i, case_num in enumerate(combisub_list):
    if (i % 5) == 0:
        print('------------------------------------')
    print(f"{case_num} : {combi_dict[case_num]}")

sys.exit("Lucky numbers have been generated !!!")