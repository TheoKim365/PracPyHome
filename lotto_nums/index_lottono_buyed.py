import itertools
import pandas as pd
import xlwings as xw
from pathlib import Path
import sys


LOTTO_NUMS_FILE = "Lotto645_buyed_980" # excel file name without extention


## <2> indexing each lotton645 number
this_dir = Path(__file__).resolve().parent
wb = xw.Book(f"{this_dir}\{LOTTO_NUMS_FILE}.xlsx")
ws = wb.sheets[0]
df = ws["a1"].expand().options(pd.DataFrame).value
# df.index = df.index.astype(int)  # index를 정수화하는 process를 버림 
wb.app.quit()


# <3> case_combi가 -1인 Data만 선별하여 별도의 DataFrame을 생성 
df1 = df.loc[df["case_combi"] == -1, :]
n = len(df1)
if n == 0:
    sys.exit("No need indexing for Lotto645 excel file")


## <1> Make the combination list  for 6/45 and convert to dictionary datatype
combi_list = list(itertools.combinations(range(1,46),6))

combi_dict = {}
for i, nums in enumerate(combi_list):
    combi_dict[i] = nums    # make the dictionary datatype
    i += 1    

## <4> Processing
df2 = df1.iloc[:,1:7]
df2 = df2.astype(dtype=int)   # data를 정수화
df2 = df2.reset_index()       # index를 data에 포함시킴

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

df.to_excel(f"{this_dir}\{LOTTO_NUMS_FILE}_idx.xlsx")
sys.exit("Completed without Error")
# # the end