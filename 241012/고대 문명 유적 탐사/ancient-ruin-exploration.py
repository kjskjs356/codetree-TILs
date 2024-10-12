# 2024 삼성 하반기 오전 1번 고대문명유적탐사

from collections import deque

# k:  반복 횟수, m: 유물 족가의 개수
k, m = map(int, input().split())
area = [list(map(int, input().split())) for _ in  range(5)]

# 벽면의 유물 저장 배열
wallArr = list(map(int, input().split()))
wall = deque()
for i in range(len(wallArr)):
    wall.append(wallArr[i])

# 4방향 탐색
dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]

# 턴마다 점수 저장용 배열
ans = []

# 회전 중심 좌표
cx = [1, 1, 1, 2, 2, 2, 3, 3, 3]
cy = [1, 2, 3, 1, 2, 3, 1, 2, 3]


def Bfs(a, b, num, v):
    q= deque()
    q.append((a, b))
    cnt = 1
    while q:
        x, y = q.pop()
        v[x][y] = True
        for i in range(4):
            nx = x + dx[i]
            ny = y + dy[i]
            if 0 <= nx < 5 and 0 <= ny < 5 and not v[nx][ny] and area[nx][ny] == num:
                v[nx][ny] = True
                cnt += 1
                q.append((nx, ny))
    return cnt


def RotateArea(x, y):
    f1, f2, f3 = area[x - 1][y - 1], area[x - 1][y], area[x - 1][y + 1]
    area[x - 1][y - 1], area[x - 1][y], area[x - 1][y + 1] \
        = area[x + 1][y - 1], area[x][y - 1], area[x - 1][y - 1]
    area[x + 1][y - 1], area[x][y - 1], area[x - 1][y - 1] \
        = area[x + 1][y + 1], area[x + 1][y], area[x + 1][y - 1]
    area[x + 1][y + 1], area[x + 1][y], area[x + 1][y - 1] \
        = area[x - 1][y + 1], area[x][y + 1], area[x + 1][y + 1]
    area[x - 1][y + 1], area[x][y + 1], area[x + 1][y + 1] = f1, f2, f3


def EraseBfs(a, b, num):
    q = deque()
    q.append((a, b))
    area[a][b] = 0
    while q:
        x, y = q.pop()
        for i in range(4):
            nx = x + dx[i]
            ny = y + dy[i]
            if 0 <= nx < 5 and 0 <= ny < 5 and area[nx][ny] == num:
                area[nx][ny] = 0
                q.append((nx, ny))

# 유물 탐색 함수
def Search():
    maxCnt = 0
    minRotate = 999999
    tx, ty = 99, 99
    score = 0
    eraseList = []
    isSuccess = False
    # 각 중심점 돌면서 체크
    for x, y in zip(cx, cy):
        for r in range(4):
            # 90도씩 돌면서 탐색(함수 호출 1번당 90도 회전)
            RotateArea(x, y)
            tempList = []
            # 3번 돌때까지만(270) bfs 탐색
            if r < 3:
                nowCnt = 0
                visited = [[False for _ in range(5)] for _ in range(5)]
                for i in range(5):
                    for j in range(5):
                        if not visited[i][j]:
                            tempCnt = Bfs(i, j, area[i][j], visited)
                            # tempCnt가 3이상일때만 3획득
                            if tempCnt >= 3:
                                nowCnt += tempCnt
                                tempList.append((i, j))
                                isSuccess = True
                # 1. 최대값 비교, 2. 회전각도 비교, 3. 가장 작은 열 비교, 4. 가장 작은 행 비교
                if nowCnt > maxCnt:
                    maxCnt = nowCnt
                    tx, ty = x, y
                    minRotate = r
                    eraseList = tempList
                elif nowCnt == maxCnt:
                    if r < minRotate:
                        minRotate = r
                        tx, ty = x, y
                        eraseList = tempList
                    elif r == minRotate:
                        if x < tx:
                            tx, ty = x, y
                            eraseList = tempList
                        elif x == tx:
                            if y < ty:
                                ty = y
                                eraseList = tempList
    if not isSuccess: return
    # 최종 갱신된 값을 기준으로 점수 획득 후 회전 & 제거 작업
    score += maxCnt
    for i in range(minRotate + 1):
        RotateArea(tx, ty)
    # 회전된 상태에서 연결된 유물 조각 제거(eraseList 이용해서 특정 좌표만 활용)
    for i ,j in eraseList:
        EraseBfs(i, j, area[i][j])

    # 빈 칸에 유적에 있는 번호 차례대로 넣고 유물 연쇄획득 반복, 더이상 안되면 멈춤
    flag = True
    while flag:
        eraseList = []
        visited = [[False for _ in range(5)] for _ in range(5)]
        for j in range(5):
            for i in range(4, -1 ,-1):
                if area[i][j] == 0:
                    area[i][j] = wall.popleft()
        # 유물 연쇄획득, 더이상 획득 못하면 종료
        for i in range(5):
            for j in range(5):
                if not visited[i][j]:
                    tempCnt = Bfs(i, j, area[i][j], visited)
                    # tempCnt가 3이상일때만 3획득
                    if tempCnt >= 3:
                        eraseList.append((i, j))
                        score += tempCnt
        if len(eraseList) > 0:
            for i, j in eraseList:
                EraseBfs(i, j, area[i][j])
        else:
            flag = False
    if score > 0:
        ans.append(score)
    else:
        return


# 턴 만큼 탐사 진행
for i in range(k):
    # 가장 점수를 높게 받는 회전 중심 및 유물 개수 찾기
    Search()

print(' '.join(map(str, ans)))