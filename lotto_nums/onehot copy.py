import numpy as np

# # 당첨번호를 원핫인코딩(ohbin)로 변환
# def numbers2ohbin(numbers):
#     # ohbin = np.zeros(45, np.int32) # 45개의 빈칸을 만듦
#     ohbin = '000000000000000000000000000000000000000000000'
    

#     for i in range(6):  # 6개의 당첨번호에 대해서 반복함
#         # ohbin[int(numbers[i] - 1)] = 1
#         # # 로또번호는 1부터 시작하지만 벡터의 인덱스 시작은 0부터 시작하므로 1을 뺌
#         ohbin. [i:i+1] = 1
#         print(ohbin)

#     return ohbin

# # 원핫인코딩(ohbin)을 번호로 변환 
# def ohbin2numbers(ohbin):
#     numbers = []

#     for i in range(len(ohbin)):
#         if ohbin[i] == 1:
#             numbers.append(i + 1)
    
#     return numbers


a_dict ={}
x = [10, 23, 29, 33, 37, 40]
a = str(x)
print(a)
a_dict[a] = 3
print(a_dict.items())

# x_oh = numbers2ohbin(x)
# print("x_oh : " + str(x_oh))
# print(str(x_oh))

# x = ohbin2numbers(x_oh)
# print("x : " + str(x))
