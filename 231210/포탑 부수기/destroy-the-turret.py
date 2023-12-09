from collections import deque

# 2023 삼성 상반기 오전 1번 포탑부수기

N, M, K = map(int, input().split())
tower = []
for i in range(N):
    temp = list(map(int, input().split()))
    tower.append(temp)

# 우 하 좌 상
dx = [0, 1, 0, -1]
dy = [1, 0, -1, 0]

# 우 하 좌 상
dxx = [-1, 0, 1, 1, 1, 0, -1, -1]
dyy = [1, 1, 1, 0, -1, -1, -1, 0]

# 공격 기록 저장용 좌표
attaked = [[0] * M for _ in range(N)]

# 가장약한포탑 & 가장 강합 포탑 좌표
sx, sy, gx, gy = -1, -1, -1, -1

alive, ans = 0, 0

# 가장 약한 포탑 선정
def choiceMinTower(n):
    x, y = -1, -1
    attack = 10000
    for i in range(N):
        for j in range(M):
            if tower[i][j] == 0: continue
            # 공격력이 가장 낮은지 체크
            if tower[i][j] < attack:
                x, y = i, j
                attack = tower[i][j]
            # 공격력이 같으면 가장 최근에 공격했는지 체크
            elif tower[i][j] == attack:
                if attaked[i][j] > attaked[x][y]:
                    x, y = i, j
                    attack = tower[i][j]
                # 둘다 공격이력이 같은 경우 행 열 합 체크
                elif attaked[i][j] == attaked[x][y]:
                    if i + j > x + y:
                        x, y = i, j
                        attack = tower[i][j]
                    # 행열합 같으면 열 값이 가장 큰 포탑 선정
                    elif i + j == x + y:
                        if j > y:
                            x, y = i, j
                            attack = tower[i][j]
    # 최근 공격으로 갱신
    attaked[x][y] = n
    return x, y, attack + M + N

# 가장 강한 포탑 선정
def choiceMaxTower():
    x, y = -1, -1
    attack = 0
    for i in range(N):
        for j in range(M):
            if tower[i][j] == 0: continue
            # 공격력이 가장 높은지 체크
            if tower[i][j] > attack:
                x, y = i, j
                attack = tower[i][j]
            # 공격력이 같으면 가장 오래전에 공격했는지 체크
            elif tower[i][j] == attack:
                if attaked[i][j] < attaked[x][y]:
                    x, y = i, j
                    attack = tower[i][j]
                # 둘다 공격이력이 같은 경우 행 열 합 체크
                elif attaked[i][j] == attaked[x][y]:
                    if i + j < x + y:
                        x, y = i, j
                        attack = tower[i][j]
                    # 행열합 같으면 열 값이 가장 작은 포탑 선정
                    elif i + j == x + y:
                        if j < y:
                            x, y = i, j
                            attack = tower[i][j]
    return x, y


# 격자마다 최단거리 설정
def bfs(a, b):
    q = deque()
    q.append((a, b, 0))
    while q:
        x, y, cnt = q.popleft()
        distance[x][y] = cnt
        for i in range(4):
            nx = (x + dx[i])
            ny = (y + dy[i])
            # 격자 벗어나면 반대편으로 이동
            if nx < 0: nx = N - 1
            elif nx > N - 1: nx = 0
            if ny < 0: ny = M - 1
            elif ny > M - 1: ny = 0

            if tower[nx][ny] != 0 and distance[nx][ny] == 10000:
                distance[nx][ny] = cnt + 1
                q.append((nx, ny, cnt + 1))


# 최단거리 레이저 공격
def laserAttack(x, y, gx, gy, atk):
    # 목표지점 도착할때까지 레이저 공격
    damaged[gx][gy] = True
    minDist = 10000
    while True:
        tx, ty = -1, -1
        for i in range(4):
            nx = x + dx[i]
            ny = y + dy[i]
            # 격자 벗어나면 반대편으로 이동
            if nx < 0:
                nx = N - 1
            elif nx > N - 1:
                nx = 0
            if ny < 0:
                ny = M - 1
            elif ny > M - 1:
                ny = 0
            if tower[nx][ny] != 0:
                if minDist > distance[nx][ny]:
                    minDist = distance[nx][ny]
                    tx, ty = nx, ny
        if tx == gx and ty == gy:
            tower[gx][gy] -= atk
            if tower[gx][gy] < 0:
                tower[gx][gy] = 0
            return
        tower[tx][ty] -= atk // 2
        if tower[tx][ty] < 0: tower[tx][ty] = 0
        damaged[tx][ty] = True
        x, y = tx, ty

# 포탑 공격
def cannonAttack(x, y, gx, gy, atk):
    damaged[gx][gy] = True
    for i in range(8):
        nx = gx + dxx[i]
        ny = gy + dyy[i]
        # 격자 벗어나면 반대편으로 이동
        if nx < 0:
            nx = N - 1
        elif nx > N - 1:
            nx = 0
        if ny < 0:
            ny = M - 1
        elif ny > M - 1:
            ny = 0
        if x == nx and y == ny: continue
        if tower[nx][ny] != 0:
            tower[nx][ny] -= atk // 2
            if tower[nx][ny] < 0: tower[nx][ny] = 0
            damaged[nx][ny] = True
    tower[gx][gy] -= atk
    if tower[gx][gy] < 0: tower[gx][gy] = 0


# 남아있는 포탑 개수 확인
def checkTower():
    alive, attack = 0, 0
    for i in range(N):
        for j in range(M):
            if tower[i][j] != 0:
                alive += 1
                if tower[i][j] > attack:
                    attack = tower[i][j]
    return alive, attack

# 포탑 정비
def refairTower():
    for i in range(N):
        for j in range(M):
            if not damaged[i][j] and tower[i][j] != 0:
                if i == sx and j == sy: continue
                if i == gx and j == gy: continue
                tower[i][j] += 1


# K턴 or 남아있는 포탑개수 1개인 경우 종료
for i in range(1, K + 1):
    # 최단거리 계산용 좌표
    distance = [[10000] * M for _ in range(N)]
    damaged = [[False] * M for _ in range(N)]

    # 공격자 및 공격 대상자 선정
    sx, sy, attack = choiceMinTower(i)
    gx, gy = choiceMaxTower()
    tower[sx][sy] += (M + N)

    # 최단거리설정
    bfs(gx, gy)

    # 레이저 공격 가능여부 체크
    if(distance[sx][sy] != 10000):
        laserAttack(sx, sy, gx, gy, attack)
    else:
        cannonAttack(sx, sy, gx, gy, attack)

    refairTower()
    # 포탑 개수 체크
    alive, ans = checkTower()
    if alive == 1:
        print(ans)
        break

if alive > 1: print(ans)