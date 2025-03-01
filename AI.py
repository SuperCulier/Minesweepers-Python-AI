# Các ô được dự đoán có mìn (-1)
# các ô chưa mở 0 (có value là -1 nếu nó là mìn và -2 nếu không có mìn), khi mở ô này thì set lại status thành -1 hoặc -1
# các ô được dự đoán là an toàn (-2)
# các số nguyên > 0: số lượng mìn trong 8 ô xung quanh
# Input giải thuật: mảng chứa các ô, số hàng, số cột
import random

def get_neighbors(i, j, grid_size):
    """Lấy danh sách các ô lân cận của (i, j)."""
    neighbors = []
    for di in [-1, 0, 1]:
        for dj in [-1, 0, 1]:
            ni, nj = i + di, j + dj
            if 0 <= ni < grid_size and 0 <= nj < grid_size and (di != 0 or dj != 0):
                neighbors.append((ni, nj))
    return neighbors


def rollback(table, col, row):
    #Kiểm tra các ô xung quanh (col, row). Nếu có ô số nào bị quá giới hạn mìn, mở lại một số ô bất kỳ.
    grid_size = len(table)
    rollback_occurred = False  # Đánh dấu nếu có rollback
    
    # Duyệt tất cả các ô xung quanh (col, row)
    for ni, nj in get_neighbors(col, row, grid_size):
        if table[ni][nj][0] > 0:  # Nếu là ô số
            # Đếm số mìn thực tế xung quanh ô này
            mine_count = sum(1 for x, y in get_neighbors(ni, nj, grid_size) if table[x][y][0] == -1)
            unopen_count = sum(1 for x, y in get_neighbors(ni, nj, grid_size) if table[x][y][0] == 0)
            # Nếu số mìn thực tế lớn hơn số trên ô, rollback một số ô ngẫu nhiên
            if (mine_count > table[ni][nj][0]) or (mine_count + unopen_count < table[ni][nj][0]):
                sai_pham = abs(mine_count - table[ni][nj][0])
                print(f"LỖI: Ô ({ni}, {nj}) có số mìn xung quanh = {mine_count}, nhưng chỉ cho phép {table[ni][nj][0]}. Rollback {sai_pham} ô...")
                
                # Lấy danh sách các ô có mìn xung quanh ô (ni, nj)
                min_positions = [(x, y) for x, y in get_neighbors(ni, nj, grid_size) if table[x][y][0] in (-1, -2)]
                # Chọn ngẫu nhiên `sai_pham` ô để mở lại
                if len(min_positions) >= sai_pham:
                    to_reset = random.sample(min_positions, sai_pham)
                    for x, y in to_reset:
                        table[x][y][0] = 0  # Mở lại ô
                rollback_occurred = True
    
    return not rollback_occurred  # Trả về True nếu không rollback, False nếu đã rollback
"""

def rollback(table, col, row):
    #Kiểm tra các ô xung quanh (col, row). Nếu có ô số nào bị quá giới hạn mìn, chỉ rollback các ô xung quanh nó.
    grid_size = len(table)
    rollback_occurred = False  # Đánh dấu nếu có rollback
    
    # Duyệt tất cả các ô xung quanh (col, row)
    for ni, nj in get_neighbors(col, row, grid_size):
        if table[ni][nj][0] > 0:  # Nếu là ô số
            # Đếm số mìn thực tế xung quanh ô này
            mine_count = sum(1 for x, y in get_neighbors(ni, nj, grid_size) if table[x][y][0] == -1)
            unopen_count = sum(1 for x, y in get_neighbors(ni, nj, grid_size) if table[x][y][0] == 0)
            
            # Nếu số mìn thực tế lớn hơn số trên ô, rollback các ô xung quanh ô này
            if (mine_count > table[ni][nj][0]) or (mine_count + unopen_count < table[ni][nj][0]):
                #print(f"LỖI: Ô ({ni}, {nj}) có số mìn xung quanh = {mine_count}, nhưng chỉ cho phép {table[ni][nj][0]}. Rollback...")
                print("Phát hiện lỗ hỏng, Đang tiến hành roll back")
                for x, y in get_neighbors(ni, nj, grid_size):
                    if table[x][y][0] < 0:  # Reset chỉ các ô chưa mở xung quanh ô đang xét
                        table[x][y][0] = 0
                rollback_occurred = True
    return not rollback_occurred  # Trả về True nếu không rollback, False nếu đã rollback
"""

def openSafe(table, col, row):
    for i in range(row):
        for j in range(col):
            if table[i][j][0] > 0:  # Kiểm tra ô có số lớn hơn 0
                count_mines = 0
                neighbors = []
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if dx == 0 and dy == 0:
                            continue
                        ni, nj = i + dx, j + dy
                        if 0 <= ni < row and 0 <= nj < col:
                            if table[ni][nj][0] == -1:  # Kiểm tra ô có mìn
                                count_mines += 1
                            elif table[ni][nj][0] == 0:
                                neighbors.append((ni, nj))
                if count_mines == table[i][j][0]:  # Nếu số ô có mìn bằng với số trên ô đang kiểm tra
                    for ni, nj in neighbors:
                        table[ni][nj][0] = -2  # Đánh dấu ô là an toàn
                        rollback(table, ni, nj)
                        print(f"AI mở ô an toàn: ({ni}, {nj})")
                        #if table[ni][nj][2] == -3:
                        #    return False
    #return True

def Heuristic(table, col, row): 
    # Thực hiện một số thao tác với các tham số đầu vào
    # duyệt qua tất cả các ô có số > 0, Nếu một ô có số và số ô chưa mở xung quanh đúng bằng số đó, tất cả những ô đó là mìn

    for i in range(row):
        for j in range(col):
            if table[i][j][0] > 0:  # Sử dụng table[i][j][0] để lấy giá trị của ô
                count_unopened = 0
                count_mine = 0
                neighbors = []
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if dx == 0 and dy == 0:
                            continue
                        ni, nj = i + dx, j + dy
                        if 0 <= ni < row and 0 <= nj < col and table[ni][nj][0] == 0:  # Sử dụng table[ni][nj][0] để kiểm tra giá trị của ô
                            count_unopened += 1
                            neighbors.append((ni, nj))
                        elif 0 <= ni < row and 0 <= nj < col and table[ni][nj][0] == -1:
                            count_mine += 1
                if count_unopened == table[i][j][0] - count_mine:  # Sử dụng table[i][j][0] để so sánh
                    for ni, nj in neighbors:
                        table[ni][nj][0] = -1  # Đánh dấu ô là mìn
                        rollback(table, ni, nj)
                elif (table[i][j][0] - count_mine) > 0 and count_unopened != 0:
                    for ni, nj in neighbors:
                        table[ni][nj][1] += (table[i][j][0] - count_mine) / count_unopened  # Cập nhật xác suất vào table[ni][nj][1]

def selectCell(table, col, row):
    minProb = 10000
    safePosition = (-1, -1)
    
    for i in range(row):
        for j in range(col):
            if table[i][j][0] == 0:  # Kiểm tra ô chưa mở
                if table[i][j][1] < minProb:  # Kiểm tra giá trị xác suất
                    minProb = table[i][j][1]
                    safePosition = (i, j)
    
    if safePosition != (-1, -1):
        table[safePosition[0]][safePosition[1]][0] = -2  # Đánh dấu ô an toàn
        print(f"AI mở ô được dự đoán là an toàn nhất: {safePosition}")
        rollback(table, safePosition[0], safePosition[1])

def selectMine(table, col, row):
    maxProb = 0
    minePosition = (-1, -1)
    
    for i in range(row):
        for j in range(col):
            if table[i][j][0] == 0:  # Kiểm tra ô chưa mở
                if table[i][j][1] > maxProb:  # Kiểm tra giá trị xác suất
                    maxProb = table[i][j][1]
                    minePosition = (i, j)
    
    if minePosition != (-1, -1):
        table[minePosition[0]][minePosition[1]][0] = -1  # Đánh dấu ô là mìn
        print(f"AI đánh dấu ô này có mìn: {minePosition}")
        rollback(table, minePosition[0], minePosition[1])

def checkSolution(table, grid_size):
    not_satisfied_cells = []

    for i in range(grid_size):
        for j in range(grid_size):
            if table[i][j][0] > 0:  # Chỉ kiểm tra các ô có giá trị > 0
                # Đếm số ô có mìn (-3) xung quanh
                mine_count = sum(1 for x, y in get_neighbors(i, j, grid_size) if table[x][y][0] == -1)
                
                # Nếu số mìn xung quanh không khớp với giá trị của ô, lưu lại ô đó
                if mine_count != table[i][j][0]:
                    not_satisfied_cells.append((i, j))

    if not not_satisfied_cells:
        print("Đã giải chính xác!")
    else:
        print("Các ô không thỏa mãn:", not_satisfied_cells)

