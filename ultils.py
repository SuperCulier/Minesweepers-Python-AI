import pygame
import sys
import AI
import os

def load_matrix_from_file(filename, folder_path="testcase"):
    file_path = os.path.join(folder_path, filename)
    with open(file_path, "r") as f:
        matrix = [[int(num) for num in line.split()] for line in f]
    return matrix

def create_table(matrix):
    size = len(matrix)
    table = []
    for i in range(size):
        row = []
        for j in range(size):
            if matrix[i][j] > 0:
                row.append([matrix[i][j], 0])  # Ô đã mở 
            elif matrix[i][j] == 0:
                row.append([0, 0])  # Ô chưa mở
        table.append(row)
    return table


def draw_grid(screen, table, size, cell_size):
    font = pygame.font.Font(None, 30)  # Font cho chỉ số hàng & cột
    padding = cell_size  # Lề để chứa số hàng & cột

    for i in range(size):
        for j in range(size):
            x, y = j * cell_size + padding, i * cell_size + padding
            value, _ = table[i][j]

            # Mặc định tô màu trắng cho ô chưa mở
            color = (255, 255, 255)

            # Vẽ ô lưới
            pygame.draw.rect(screen, color, (x, y, cell_size, cell_size))

            # Nếu là ô đã mở và an toàn (-2) => Vẽ vòng tròn xanh
            if value == -2:
                pygame.draw.circle(screen, (0, 255, 0), (x + cell_size // 2, y + cell_size // 2), cell_size // 3)

            # Nếu là ô mìn đã được đánh dấu (-1) => Vẽ vòng tròn đỏ
            elif value == -1:
                pygame.draw.circle(screen, (255, 0, 0), (x + cell_size // 2, y + cell_size // 2), cell_size // 3)

            # Nếu ô có số (> 0) => Hiển thị số
            elif value > 0:
                text = font.render(str(value), True, (0, 0, 0))
                screen.blit(text, (x + cell_size // 3, y + cell_size // 4))

            # Viền ô
            pygame.draw.rect(screen, (0, 0, 0), (x, y, cell_size, cell_size), 1)

    # Vẽ chỉ số hàng (bên trái) và chỉ số cột (trên cùng)
    for i in range(size):
        # Chỉ số hàng (bên trái)
        row_label = font.render(str(i), True, (0, 0, 0))
        screen.blit(row_label, (padding // 3, i * cell_size + padding + cell_size // 3))

        # Chỉ số cột (trên cùng)
        col_label = font.render(str(i), True, (0, 0, 0))
        screen.blit(col_label, (i * cell_size + padding + cell_size // 3, padding // 3))


# Xử lý sự kiện chuột
"""def handle_click(table, pos, button, size, cell_size, padding):
    # Trừ đi padding để tính đúng vị trí ô
    x, y = pos[0] - padding, pos[1] - padding  

    # Nếu click vào phần chỉ số hàng/cột thì bỏ qua
    if x < 0 or y < 0:
        return  

    j, i = x // cell_size, y // cell_size  # Xác định tọa độ (i, j)

    # Kiểm tra xem có nằm trong bảng không
    if 0 <= i < size and 0 <= j < size:
        value, _, real_value = table[i][j]

        if button == 1:  # Chuột trái (mở ô)
            if real_value == -3:  # Nếu là mìn → Game over
                print("💥 Game Over! Bạn đã mở phải mìn.")
                pygame.quit()
                sys.exit()
            elif real_value == -4:  # Nếu là ô an toàn → Đánh dấu đã mở
                table[i][j][0] = -2

        elif button == 3:  # Chuột phải (đánh dấu mìn)
            if value == 0:  # Nếu chưa mở → Đánh dấu
                table[i][j][0] = -1
            elif value == -1:  # Nếu đã đánh dấu → Bỏ dấu
                table[i][j][0] = 0 
"""


# Gọi AI bằng phím A
def handle_keypress(table, size, key):
    if key == pygame.K_a:  # Nếu nhấn phím 'A'

        # Đặt lại xác suất của tất cả các ô chưa mở
        for i in range(size):
            for j in range(size):
                if table[i][j][0] == 0:  # Nếu ô chưa mở
                    table[i][j][1] = 0   # Reset xác suất về 0

        print("📌 AI đang xử lý...")
        AI.openSafe(table, size, size)
            #print("AI đã mở tất cả ô an toàn")
        #else: print("💥 Game Over! Bạn đã mở phải mìn.") # Mở các ô an toàn
        AI.Heuristic(table, size, size)  # Chạy thuật toán Heuristic
        AI.selectMine(table, size, size)
        AI.selectCell(table, size, size)
        #AI.selectBestCell(table, size, size)
        #AI.selectCell(table, size, size)  # Chọn ô an toàn

running = False  # Biến điều khiển trạng thái chạy của AI

def handle_keyAuto(table, size, key):
    global running  # Sử dụng biến toàn cục để kiểm soát trạng thái

    if key == pygame.K_d:  # Khi nhấn 'D', bắt đầu chạy AI
        running = True
        while running:
            # Đặt lại xác suất của tất cả các ô chưa mở
            for i in range(size):
                for j in range(size):
                    if table[i][j][0] == 0:  # Nếu ô chưa mở
                        table[i][j][1] = 0   # Reset xác suất về 0

            print("📌 AI đang xử lý...")
            AI.openSafe(table, size, size)
            AI.Heuristic(table, size, size)
            AI.selectMine(table, size, size)
            AI.selectCell(table, size, size)

            # Thêm điều kiện dừng nếu nhận phím 'P'
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                    running = False
                    print("🛑 AI đã dừng.")


def handle_keyCheck(table, size, key):
    if key == pygame.K_s:  # Nếu nhấn phím 'S'
        print("📌 AI đang xử lý...")
        AI.checkSolution(table, size)