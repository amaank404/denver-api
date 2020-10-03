import pygame

pygame.init()

WIDTH = 720
HEIGHT = 576
FPS = 60
CELL_HEIGHT = 20
CELL_WIDTH = 12

# Colors  (R,  G,  B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

display = pygame.display.set_mode((WIDTH, HEIGHT))
grid_surface = pygame.Surface((720, 480))
clock = pygame.time.Clock()

grid_surface_rect: pygame.Rect = grid_surface.get_rect()
grid_surface_rect.bottom = HEIGHT


def draw_grid(surface: pygame.Surface):
    height = surface.get_height()
    width = surface.get_width()
    for x in range(0, height, CELL_HEIGHT):
        pygame.draw.line(surface, BLACK, (0, x), (width, x))  # Horizontal lines
    for x in range(0, width, CELL_WIDTH):
        pygame.draw.line(surface, BLACK, (x, 0), (x, height))


def main():
    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit(0)
        display.fill(WHITE)
        grid_surface.fill(WHITE)
        draw_grid(grid_surface)
        display.blit(grid_surface, grid_surface_rect)
        pygame.display.update()


if __name__ == '__main__':
    main()
