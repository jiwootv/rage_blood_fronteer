# 불복종 지수에 대한 내용을 다루는 파일입니다.
# Last edit: 2025-01-11
# Maker: qwru0905, YJ
# 불복종만 넣기

import random


# 불복종 지수 설정
disobedience = 100
# 뭐가 일어날 확률 0~100(%)
"""
불복종에 의해서 발생할 수 있는 이벤트: 
작업 능력 감소 30% _ 6  : 1번
자원 소모 증가 25% _ 5
지휘 불능 20% _ 4
떠남 15% _ 3
쿠@데타 10% _ 2
합 100% _ 20

__ 블복종 확률 계산 식 __
𝑦 = 1.05^𝑥
"""


#number = random.randint()

def disobendience_percent_cal(dbd):
    return round(1.05**dbd, 2)

# for i in range(1, 101):
    # print("i: " + str(i))
    # print(disobendience_percent_cal(i))
    # print(disobendience_percent_cal(i)/2)
    # print()

dbd_act_amount = 5  # 가능한 불복종에 따른 행동의 갯수
dbd_act_percent = [6, 5, 4, 3, 2]
dbd_act_name = [None, "작업 능력 감소", "자원 소모 증가", "지휘 불능", "떠남", "쿠데타"]
dbdp = []

for i in range(5):
    for k in range(dbd_act_percent[i]):
        dbdp.append(range(1, dbd_act_amount+1)[i])
# print(dbdp)


def dbd_act(dbd):
    disobendience_percent_cal(dbd)
    if random.random() <= dbd/200:
        return random.choice(dbdp)
    else:
        return 0


print(dbd_act_name[dbd_act(disobedience)])


