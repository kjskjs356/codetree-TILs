# 2023 삼성 하반기 오후 1번 루돌프의 반란


# n: 맵크기, m: 게임 턴 수, p: 산타 인원수, c: 루돌프 힘, d: 산타 힘
n, m, p, c, d = map(int, input().split())
# 맵 생성
area = [[0] * n for _ in range(n)]

# 루돌프 위치
x, y = map(int, input().split())
x -= 1
y -= 1
dearLocation = [x, y]

area[dearLocation[0]][dearLocation[1]] = -1

# 산타 배열 설정
santa = []
for i in range(p):
    num, x, y = map(int, input().split())
    santa.append([num, x - 1, y - 1])
santa.sort()

# 산타 인원수에 따라 기절 턴수 관리하는 배열 생성 (0번째 인덱스는 제외)
sturn = [0] * (p + 1)

# 산타 배치
for i in range(p):
    num, x, y = santa[i]
    area[x][y] = num

# 각 산타가 얻음 점수 배열(0번째 인덱스는 제외)
score = [0] * (p + 1)

# 산타 생존 여부 배열
survival = [True] * (p + 1)
survival[0] = False

# 8방향 움직임(루돌프, 12시부터 시계)
dxd = [-1, -1, 0, 1, 1, 1, 0, -1]
dyd = [0, 1, 1, 1, 0, -1, -1 ,-1]

# 4방향 움직임(산타, 12시부터 시계)
dxs = [-1, 0, 1, 0]
dys = [0, 1, 0, -1]

# 충돌함수(매개변수값이 1이면 루돌프, 2면 산타)
def Crush(typeNum, direct, num):
    if typeNum == 1:
        # 충돌당한 산타의 점수 획득
        score[num] += c
        sturn[num] = 2
        flag = True
        first = True
        # 충돌당한 방향으로 밀려남, 해당장소에 산타가 있으면 연쇄적으로 밀려남, 더이상 밀려나지않거나 탈락하면 반본 종료
        while flag:
            x, y = santa[num - 1][1], santa[num - 1][2]
            # 최초 부딪힌 경우 c칸, 이후로는 1칸씩만 이동
            if first:
                nx = x + dxd[direct] * c
                ny = y + dyd[direct] * c
            else:
                nx = x + dxd[direct]
                ny = y + dyd[direct]
            first = False
            # 격자 벗어나면 산타 탈락하고 종료
            if not (0 <= nx < n and 0 <= ny < n):
                santa[num - 1][1], santa[num - 1][2] = -1, -1
                survival[num] = False
                flag = False
            # 해당 칸 다른 산타 존재
            elif area[nx][ny] > 0:
                nextNum = area[nx][ny]
                area[nx][ny] = num
                santa[num - 1][1], santa[num - 1][2] = nx,ny
                num = nextNum
            # 벗어나지 않고 빈칸이면 위치 갱신하고 충돌 종료
            else:
                area[nx][ny] = num
                santa[num - 1][1], santa[num - 1][2] = nx, ny
                flag = False
    elif typeNum == 2:
        # 충돌당한 산타의 점수 획득
        score[num] += d
        sturn[num] = 2
        flag = True
        first = True
        # 충돌당한 방향으로 밀려남, 해당장소에 산타가 있으면 연쇄적으로 밀려남, 더이상 밀려나지않거나 탈락하면 반본 종료
        while flag:
            x, y = santa[num - 1][1], santa[num - 1][2]
            # 최초 부딪힌 경우 c칸, 이후로는 1칸씩만 이동
            if first:
                nx = x + dxs[(direct + 2) % 4] * d
                ny = y + dys[(direct + 2) % 4] * d
            else:
                nx = x + dxs[(direct + 2) % 4]
                ny = y + dys[(direct + 2) % 4]
            first = False
            # 격자 벗어나면 산타 탈락하고 종료
            if not (0 <= nx < n and 0 <= ny < n):
                santa[num - 1][1], santa[num - 1][2] = -1, -1
                survival[num] = False
                flag = False
            # 해당 칸 다른 산타 존재
            elif area[nx][ny] > 0:
                nextNum = area[nx][ny]
                area[nx][ny] = num
                santa[num - 1][1], santa[num - 1][2] = nx, ny
                num = nextNum
            # 벗어나지 않고 빈칸이면 위치 갱신하고 충돌 종료
            else:
                area[nx][ny] = num
                santa[num - 1][1], santa[num - 1][2] = nx, ny
                flag = False


# 루돌프 움직임 함수
def MoveDear(x1, y1):
    # 가장 가까운 산타 탐색
    minDist = 999999 # 최단거리 갱신용
    targetN, targetR, targetC = -1, 0, 0 # 차순위인 r값 c값 비교용
    for num, x2, y2 in santa:
        dist = (x1 - x2) ** 2 + (y1 - y2) ** 2
        # 최단거리인 경우 개신
        if dist < minDist:
            targetN, minDist, targetR, targetC = num, dist, x2, y2
        # 거리가 같은 경우 r, c 차례 비교
        elif dist == minDist:
            if x2 > targetR:
                targetN, targetR, targetC = num, x2, y2
            elif x2 == targetR:
                if y2 > targetC:
                    targetN, targetR, targetC = num, x2, y2
    # 가장 가까운 산타 쪽으로 1칸 이동
    # 이동하기위해선 8방향을 탐색하여 산타와 거리가 가장 가까워지는 방향을 정해서 이동해야한다
    minDirect = 0
    # 방향을 정하기 위해 최단거리 값 다시 갱신
    minDist = 999999
    for i in range(8):
        nx = x1 + dxd[i]
        ny = y1 + dyd[i]
        if 0 <= nx < n and 0 <= ny < n:
            nowDist = (nx - targetR) ** 2 + (ny - targetC) ** 2
            if nowDist < minDist:
                minDirect = i
                minDist = nowDist
    # 루돌프 해당방향으로 1칸이동, 산타가없으면 종료, 산타가 있으면충돌
    nx = x1 + dxd[minDirect]
    ny = y1 + dyd[minDirect]
    # 산타가 있을때에만 충돌하기
    if area[nx][ny] > 0:
        # 충돌방향과 충돌한 산타의 번호 매개변수 사용
        Crush(1, minDirect, targetN)
    area[nx][ny] = -1
    area[x1][y1] = 0
    dearLocation[0], dearLocation[1] = nx, ny


def MoveSanta(num):
    x1, y1 = dearLocation[0], dearLocation[1]
    x2, y2 = santa[num - 1][1], santa[num - 1][2]
    # 루돌프와의 최단거리 우선 계산 후, 이동했을때 가까워 질 경우에만 이동하기
    minDist = (x1 -x2) ** 2 + (y1 - y2) ** 2
    # 최단거리 방향
    minDirect = 0
    # 이동가능 여부
    isMove = False
    for i in range(4):
        # 가까워지는 방향이어도 해당 방향으로 이동못하거나 산타가 있으면 이동 불가
        nx = x2 + dxs[i]
        ny = y2 + dys[i]
        if 0 <= nx < n and 0 <= ny < n:
            if area[nx][ny] > 0: continue
            nowDist = (nx - x1) ** 2 + (ny - y1) ** 2
            if nowDist < minDist:
                minDist = nowDist
                minDirect = i
                isMove = True
    # 이동가능하면 산타 이동시키기
    if isMove:
        nx = x2 + dxs[minDirect]
        ny = y2 + dys[minDirect]
        area[x2][y2] = 0
        santa[num - 1][1], santa[num - 1][2] = nx, ny
        # 루돌프가 있으면 충돌
        if area[nx][ny] == -1:
            Crush(2, minDirect, num)
        else:
            area[nx][ny] = num


# m 만큼 게임 턴 실시
for i in range(m):
    # 루돌프 움직임
    MoveDear(dearLocation[0], dearLocation[1])
    # 산타 차례대로 행동, 단 기절 중이거나 탈락한 산타는 이동X
    for j in range(1, p + 1):
        if sturn[j] > 0 or not survival[j]: continue
        MoveSanta(j)
    # 산타 생존여부 확인, 모두 죽으면 바로 게임 끝
    if sum(survival) == 0:
        break
    # 살아있는 산타는 1점식 추가 획득
    for j in range(1, p + 1):
        if survival[j]:
            score[j] += 1
    # 턴 종료 시 기절 1회씩 감소
    for j in range(1, p + 1):
        if sturn[j] > 0: sturn[j] -= 1

print(' '.join(map(str, score[1:])))