import pygame
import sys
from ultils import load_matrix_from_file, create_table, draw_grid, handle_keypress,handle_keyCheck
#from AI import openSafe, Heuristic, selectCell

# Hàm chính
def main():
    pygame.init()
    
    filename = input("Nhập tên file TXT: ")
    matrix = load_matrix_from_file(filename)
    
    size = len(matrix)
    cell_size = 40
    padding = cell_size  # Lề để vẽ số hàng & cột
    screen_size = size * cell_size + padding
    screen = pygame.display.set_mode((screen_size, screen_size))
    pygame.display.set_caption("Minesweeper Grid")
    
    table = create_table(matrix)
    clock = pygame.time.Clock()
    
    running = True
    while running:
        screen.fill((255, 255, 255))
        draw_grid(screen, table, size, cell_size)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    handle_keypress(table, size, event.key)  # Xử lý khi nhấn phím
                elif event.key == pygame.K_s:
                    handle_keyCheck(table, size, event.key)
        
        pygame.display.flip()
        clock.tick(30)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

