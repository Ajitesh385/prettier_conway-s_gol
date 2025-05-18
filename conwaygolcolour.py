import pygame
import numpy as np
import time
import random

# Define vibrant colors
color_bg = (30, 30, 60)
color_grid = (50, 50, 90)
color_die_next = (255, 100, 100)  # light red
alive_colors = [(255, 255, 255), (255, 200, 0), (0, 255, 180), (100, 255, 100), (200, 0, 255)]

def update(screen, cells, size, with_progress=False):
    updated_cells = np.zeros((cells.shape[0], cells.shape[1]))
    
    for row, col in np.ndindex(cells.shape):
        alive = np.sum(cells[max(0, row - 1):row + 2, max(0, col - 1):col + 2]) - cells[row, col]

        if cells[row, col] == 1:
            if alive < 2 or alive > 3:
                color = color_die_next if with_progress else color_bg
            else:
                updated_cells[row, col] = 1
                color = random.choice(alive_colors) if with_progress else alive_colors[0]
        else:
            if alive == 3:
                updated_cells[row, col] = 1
                color = random.choice(alive_colors) if with_progress else alive_colors[0]
            else:
                color = color_bg

        pygame.draw.rect(screen, color, (col * size, row * size, size - 1, size - 1))

    return updated_cells

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("🌈 Conway's Game of Life - Color Edition")

    cell_size = 10
    cells = np.zeros((screen.get_height() // cell_size, screen.get_width() // cell_size))
    screen.fill(color_grid)
    update(screen, cells, cell_size)
    pygame.display.flip()

    running = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = not running
                    update(screen, cells, cell_size)
                    pygame.display.update()
                elif event.key == pygame.K_c:
                    cells = np.zeros_like(cells)  # Clear grid

        if pygame.mouse.get_pressed()[0]:  # Left click to draw
            pos = pygame.mouse.get_pos()
            cells[pos[1] // cell_size, pos[0] // cell_size] = 1
            update(screen, cells, cell_size)
            pygame.display.update()

        screen.fill(color_grid)

        if running:
            cells = update(screen, cells, cell_size, with_progress=True)
            pygame.display.update()

        time.sleep(0.05)

if __name__ == '__main__':
    main()
