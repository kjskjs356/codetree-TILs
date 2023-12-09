# 2023 삼성 하반기 오전 1번 왕실의 기사 대결
from collections import deque

L, N, Q = map(int, input().split())
area = []
for _ in range(L):
    temp = list(map(int, input().split()))
    area.append(temp)
knight = []
# 최초 기사들 체력
first = [0] * N
now = [0] * N
for i in range(N):
    r, c, h, w, k = map(int, input().split())
    knight.append([r - 1, c - 1, h, w, k])
    first[i] = k
ans = 0

# 위 오 왼 아
dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]

def SetKnight():
    for i in range(N):
        r, c, h, w, k = knight[i][0], knight[i][1], knight[i][2], knight[i][3], knight[i][4]
        # 이미 끝난 기사는 맵배치 X
        if k == 0: continue
        for x in range(r, r + h):
            for y in range(c, c + w):
                area2[x][y] = i + 1

def Move(idx, d):
    # 지목받은 병사의 좌측 상단 위치 확인
    isBlock = False
    target = [idx + 1]
    q = deque()
    q.append(idx)
    while q:
        if isBlock: break
        idx2 = q.popleft()
        # 위쪽 이동 체크
        if d == 0:
            x, y, h, w = knight[idx2][0], knight[idx2][1], knight[idx2][2], knight[idx2][3]
            for i in range(w):
                nx = x + dx[d]
                ny = y + i + dy[d]
                # 범위 벗어나거나 벽이면 이동 불가
                if not (0 <= nx < L and 0 <= ny < L) or area[nx][ny] == 2:
                    isBlock = True
                    break
                # 다른 기사 존재하면 해당 기사 target에 저장
                elif area2[nx][ny] > 0:
                    if area2[nx][ny] not in target:
                        target.append(area2[nx][ny])
                    q.append(area2[nx][ny] - 1)
        # 오른쪽 이동 체크
        if d == 1:
            x, y, h, w = knight[idx2][0], knight[idx2][1], knight[idx2][2], knight[idx2][3]
            for i in range(h):
                nx = x + i + dx[d]
                ny = y + w - 1 + dy[d]
                # 범위 벗어나거나 벽이면 이동 불가
                if not (0 <= nx < L and 0 <= ny < L) or area[nx][ny] == 2:
                    isBlock = True
                    break
                # 다른 기사 존재하면 해당 기사 target에 저장
                elif area2[nx][ny] > 0:
                    if area2[nx][ny] not in target:
                        target.append(area2[nx][ny])
                    q.append(area2[nx][ny] - 1)
        # 아래쪽 이동 체크
        if d == 2:
            x, y, h, w = knight[idx2][0], knight[idx2][1], knight[idx2][2], knight[idx2][3]
            for i in range(w):
                nx = x + h - 1 + dx[d]
                ny = y + i + dy[d]
                # 범위 벗어나거나 벽이면 이동 불가
                if not (0 <= nx < L and 0 <= ny < L) or area[nx][ny] == 2:
                    isBlock = True
                    break
                # 다른 기사 존재하면 해당 기사 target에 저장
                elif area2[nx][ny] > 0:
                    if area2[nx][ny] not in target:
                        target.append(area2[nx][ny])
                    q.append(area2[nx][ny] - 1)
        # 왼쪽 이동 체크
        if d == 3:
            x, y, h, w = knight[idx2][0], knight[idx2][1], knight[idx2][2], knight[idx2][3]
            for i in range(h):
                nx = x + i + dx[d]
                ny = y + + dy[d]
                # 범위 벗어나거나 벽이면 이동 불가
                if not (0 <= nx < L and 0 <= ny < L) or area[nx][ny] == 2:
                    isBlock = True
                    break
                # 다른 기사 존재하면 해당 기사 target에 저장
                elif area2[nx][ny] > 0:
                    if area2[nx][ny] not in target:
                        target.append(area2[nx][ny])
                    q.append(area2[nx][ny] - 1)
    if isBlock: return True, target
    # 이동가능한 상태면 target안에 들어있는 병사번호들 위치 갱신
    for num in target:
        x, y = knight[num - 1][0], knight[num - 1][1]
        nx = x + dx[d]
        ny = y + dy[d]
        knight[num - 1][0], knight[num - 1][1] = nx, ny
    return False, target

def CheckTrap(idx, target, area2):
    global ans
    for i in range(L):
        for j in range(L):
            # 해당 칸이 명령받은 기사면 패스
            if area2[i][j] - 1 == idx: continue
            # 해당칸에 함정이 있고 이동한 기사면 체력 1 깎음
            elif area[i][j] == 1 and area2[i][j] in target:
                if knight[area2[i][j] - 1][4] > 0:
                    knight[area2[i][j] - 1][4] -= 1

# 왕의 명령 수 만큼 진행
for _ in range(Q):
    idx, d = map(int, input().split())
    idx -= 1
    # 명령받은 기사 체력 없으면 패스
    if knight[idx][4] == 0: continue
    # 맵에 기사 세팅
    area2 = [[0] * L for _ in range(L)]
    SetKnight()
    # 기사 이동
    isBlock, target = Move(idx, d)
    # 움직일 수 없는 상태면 현재 명령 종료
    if isBlock: continue
    # 갱신된 위치를 기반으로 area2에 재배치 후 함정 확인
    area2 = [[0] * L for _ in range(L)]
    SetKnight()
    # 명령받은 기사를 제외한 나머지 움직인 기사들 함정여부 확인
    CheckTrap(idx, target, area2)
    # 현재 체력 갱신
    for i in range(N):
        now[i] = knight[i][4]

# 명령 종료 후 최초체력과 현재 체력 비교 후 답 도출
for i in range(N):
    if now[i] > 0:
        ans += first[i] - now[i]
print(ans)