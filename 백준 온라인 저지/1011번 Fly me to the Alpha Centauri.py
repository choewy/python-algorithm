def value() -> int:
    x, y = map(int, input().split())
    return y - x


for _ in range(int(input())):
    distance = value()          # 총 이동 거리
    maximum = 0                 # 작동 횟수 별 총 이동 거리의 최대값
    increase = 1                # 증가분
    add = False                 # 증가 여부
    count = 1                   # 작동 횟수

    while True:
        maximum += increase     # 최대값을 증가분만큼 증가

        if add:
            increase += 1       # 증가분 1 증가 ex) [1, 2, 2, 3, 3...]

        add = not add           # 증가 여부 역전화

        if distance <= maximum:
            break               # 총 이동 거리가 작동 횟수 별 최대값에 포함되는 경우

        count += 1              # 작동 횟수 1 증가

    print(count)

