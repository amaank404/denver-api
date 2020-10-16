import pygame
import argparse
import denver

pygame.init()

WIDTH = 720
HEIGHT = 580
FPS = 60
CELL_HEIGHT = 20
CELL_WIDTH = 12

# Colors  (R,  G,  B)
GRAY = (250, 250, 250)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
WHITE = (255, 255, 255)
LIGHT_BLACK = (169, 169, 169)
LIGHT_RED = (255, 204, 203)
LIGHT_GREEN = (144, 238, 144)
LIGHT_YELLOW = (255, 237, 131)
LIGHT_BLUE = (47, 141, 255)
LIGHT_MAGENTA = (255, 128, 255)
LIGHT_CYAN = (224, 255, 255)
LIGHT_WHITE = (248, 248, 255)

# Style Escape Sequence
BRIGHT = (250, 250, 250)
NORMAL = (240, 240, 240)
DIM = (230, 230, 230,)

COLORS = denver.ctext.ColoredText.cloredTextEscapeSequenceFore
COLORS_PYGAME_LIST = [BLACK, BLUE, RED, GREEN, YELLOW, MAGENTA, CYAN, WHITE,
                      LIGHT_BLACK, LIGHT_RED, LIGHT_GREEN, LIGHT_YELLOW, LIGHT_BLUE,
                      LIGHT_MAGENTA, LIGHT_CYAN, LIGHT_WHITE]
STYLE_PYGAME_LIST = [DIM, NORMAL, BRIGHT]
color_select_fore = 0
color_select_back = 0
style_select = 1


def generate_color_pallet(colors: list, selected: int):
    surface = pygame.Surface((len(colors)*CELL_WIDTH, CELL_HEIGHT))
    for position, index in zip(range(0, len(colors)*CELL_WIDTH, CELL_WIDTH), range(len(colors))):
        pygame.draw.rect(surface, colors[index], pygame.Rect((position, 0), (CELL_WIDTH, CELL_HEIGHT)))
    pygame.draw.rect(surface, BLACK, pygame.Rect(selected*CELL_WIDTH, 0, CELL_WIDTH, CELL_HEIGHT), 2)
    return surface


def draw_grid(surface: pygame.Surface):
    height = surface.get_height()
    width = surface.get_width()
    for x in range(0, height, CELL_HEIGHT):
        pygame.draw.line(surface, BLACK, (0, x), (width, x))  # Horizontal lines
    for x in range(0, width, CELL_WIDTH):
        pygame.draw.line(surface, BLACK, (x, 0), (x, height))


def transform_surface_coordinates_to_grid_coordinates(surface_coordinates):
    return surface_coordinates[0] // CELL_WIDTH, surface_coordinates[1] // CELL_HEIGHT


def grid_to_surface_coordinates(grid_coordinates):
    return grid_coordinates[0] * CELL_WIDTH, grid_coordinates[1] * CELL_HEIGHT


def main(args):
    global color_select_fore
    global color_select_back
    global style_select
    file_name = args.store
    if file_name is None:
        file_name = args.file
    if file_name is None:
        raise ValueError("Please specify either one of the options")
    font = pygame.font.Font("freesansbold.ttf", 10)
    fore_color_label = font.render("Fore Color", True, BLACK)
    fore_color_label_rect: pygame.Rect = fore_color_label.get_rect()
    fore_color_label_rect.midtop = (600, 2)

    back_color_label = font.render("Back Color", True, BLACK)
    back_color_label_rect: pygame.Rect = back_color_label.get_rect()
    back_color_label_rect.midtop = (600, 38)

    display = pygame.display.set_mode((WIDTH, HEIGHT))
    grid_surface = pygame.Surface((720, 480))
    clock = pygame.time.Clock()

    grid_surface_rect: pygame.Rect = grid_surface.get_rect()
    grid_surface_rect.bottom = HEIGHT

    last_selected = "fore"
    while True:
        clock.tick(FPS)
        display.fill(WHITE)
        grid_surface.fill(GRAY)
        draw_grid(grid_surface)

        color_pallet_fore = generate_color_pallet(COLORS_PYGAME_LIST, color_select_fore)
        color_pallet_fore_rect: pygame.Rect = color_pallet_fore.get_rect()
        color_pallet_fore_rect.midtop = (600, 14)

        color_pallet_back = generate_color_pallet(COLORS_PYGAME_LIST, color_select_back)
        color_pallet_back_rect: pygame.Rect = color_pallet_back.get_rect()
        color_pallet_back_rect.midtop = (600, 50)

        display.blit(grid_surface, grid_surface_rect)
        display.blit(color_pallet_fore, color_pallet_fore_rect)
        display.blit(color_pallet_back, color_pallet_back_rect)
        display.blit(fore_color_label, fore_color_label_rect)
        display.blit(back_color_label, back_color_label_rect)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit(0)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    if last_selected == "fore":
                        color_select_fore -= 1
                    elif last_selected == "back":
                        color_select_back -= 1
                    elif last_selected == "style":
                        style_select -= 1
                if event.key == pygame.K_RIGHT:
                    if last_selected == "fore":
                        color_select_fore += 1
                    elif last_selected == "back":
                        color_select_back += 1
                    elif last_selected == "style":
                        style_select += 1
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_position = event.pos
                if color_pallet_fore_rect.collidepoint(*mouse_position):
                    last_selected = "fore"
                    mouse_x_no_offset = mouse_position[0]-color_pallet_fore_rect.left
                    color_select_fore = transform_surface_coordinates_to_grid_coordinates((mouse_x_no_offset, 1))[0]
                elif color_pallet_back_rect.collidepoint(*mouse_position):
                    last_selected = "back"
                    mouse_x_no_offset = mouse_position[0]-color_pallet_back_rect.left
                    color_select_back = transform_surface_coordinates_to_grid_coordinates((mouse_x_no_offset, 1))[0]

        if color_select_back >= len(COLORS_PYGAME_LIST):
            color_select_back -= len(COLORS_PYGAME_LIST)
        if color_select_fore >= len(COLORS_PYGAME_LIST):
            color_select_fore -= len(COLORS_PYGAME_LIST)
        if color_select_fore < 0:
            color_select_fore += len(COLORS_PYGAME_LIST)
        if color_select_back < 0:
            color_select_back += len(COLORS_PYGAME_LIST)

        if style_select >= len(STYLE_PYGAME_LIST):
            style_select -= len(STYLE_PYGAME_LIST)
        if style_select < 0:
            style_select += len(STYLE_PYGAME_LIST)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="File Name to open", nargs="?", default=None)
    parser.add_argument("-s", "--store", help="Place to save the edited file", required=False, default=None)
    arguments = parser.parse_args()

    main(arguments)
