import pygame
import random
import time

pygame.font.init()
pygame.mixer.init()

WIDTH = 600

WINDOW = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("SUDOKU")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (69, 69, 69)
LIGHT_GREY = (200, 200, 200)
RED = (255, 70, 70)
GREEN = (0, 255, 0)
TURQUOISE = (92, 200, 230)
LIGHT_BLUE = (137, 207, 240)
DARK_BLUE = (0, 37, 158)

FPS = 60
clock = pygame.time.Clock()

game_over = False
run = True
started = False
mode = -1

font = pygame.font.Font("C:\mmmahrous\Zeiad\Programming\Sudoku game and solver\Assets\COMIC.TTF", 35)

win_sound = pygame.mixer.Sound("C:\mmmahrous\Zeiad\Programming\Sudoku game and solver\Assets\win.wav")
theme = pygame.mixer.Sound("C:\mmmahrous\Zeiad\Programming\Sudoku game and solver\Assets/theme.mp3")


class Slot:
    def __init__(self, value, pos, given):
        self.row, self.col = pos
        self.value = value
        self.color = BLACK
        self.given = given
        self.tried = []
        self.bg_color = [None, None]
        self.dummy_value = 0

    def make_wrong(self):
        self.color = RED

    def make_correct(self):
        self.color = DARK_BLUE

    def make_selected(self, grid):
        for row in grid:
            for value in row:
                value.bg_color[0] = None

        for value in grid[self.row]:
            value.bg_color[0] = LIGHT_GREY

        for value in [row[self.col] for row in grid]:
            value.bg_color[0] = LIGHT_GREY

        for value in get_box_values(self, grid):
            value.bg_color[0] = LIGHT_GREY

        self.bg_color[0] = TURQUOISE

    def draw_node(self):
        global font

        if self.bg_color[1] is not None:
            pygame.draw.rect(WINDOW, self.bg_color[1], (self.row * (WIDTH / 9),
                                                 self.col * (WIDTH / 9), WIDTH // 9 + 1, WIDTH // 9 + 1))

        if self.bg_color[0] is not None:
            pygame.draw.rect(WINDOW, self.bg_color[0], (self.row * (WIDTH / 9),
                                                 self.col * (WIDTH / 9), WIDTH // 9 + 1, WIDTH // 9 + 1))

        if self.dummy_value != 0:
            WINDOW.blit(font.render(str(self.dummy_value), False, self.color),
                        ((WIDTH / 9) * self.row + 20, self.col * (WIDTH / 9) + 10))

        if self.given:
            WINDOW.blit(font.render(str(self.value), False, self.color),
                        ((WIDTH / 9) * self.row + 20, self.col * (WIDTH / 9) + 10))


def draw(grid):
    WINDOW.fill(WHITE)

    for row in grid:
        for value in row:
            value.draw_node()

    for i in range(1, 10):
        if i % 3 == 0:
            pygame.draw.line(WINDOW, BLACK, (i * (WIDTH / 9), 0), (i * (WIDTH / 9), WIDTH), 3)
            pygame.draw.line(WINDOW, BLACK, (0, i * (WIDTH / 9)), (WIDTH, i * (WIDTH / 9)), 3)
        else:
            pygame.draw.line(WINDOW, BLACK, (i * (WIDTH / 9), 0), (i * (WIDTH / 9), WIDTH))
            pygame.draw.line(WINDOW, BLACK, (0, i * (WIDTH / 9)), (WIDTH, i * (WIDTH / 9)))

    pygame.display.update()


def get_box_values(value, grid):
    box_col = value.col - (value.col % 3)
    box_row = value.row - (value.row % 3)

    box_values = []

    for row in grid:
        if grid.index(row) in range(box_row, box_row + 3):
            for num in row:
                if num.col in range(box_col, box_col + 3):
                    box_values.append(num)

    return box_values


def find_related(value, grid):
    related = set()
    for row in grid:
        related.add(row[value.col])

    for num in grid[value.row]:
        related.add(num)

    for num in get_box_values(value, grid):
        related.add(num)

    return related


def find_possible_values(value, grid):
    possible_values = [i for i in range(1, 10) if i not in value.tried]
    values_to_delete = set()

    for i in find_related(value, grid):
        values_to_delete.add(i.value)

    for num in values_to_delete:
        if num in possible_values:
            possible_values.remove(num)

    return possible_values


def go_forward(current_node_coords, grid):
    # print(current_node_coords)
    current_node_coords[1] += 1
    if current_node_coords[1] > 8:
        current_node_coords[1] = 0
        current_node_coords[0] += 1

    try:
        current_node = grid[current_node_coords[0]][current_node_coords[1]]
    except IndexError:
        current_node_coords = [9, 0]
        current_node = False

    return current_node_coords, current_node


def go_back(current_node_coords, grid):
    if current_node_coords[1] == 0:
        current_node_coords[0] -= 1
        current_node_coords[1] = 8
    else:
        current_node_coords[1] -= 1

    current_node = grid[current_node_coords[0]][current_node_coords[1]]

    return current_node_coords, current_node


def solve(grid):
    draw(grid)

    current_node_coords = [0, 0]
    current_node = grid[current_node_coords[0]][current_node_coords[1]]
    while True:
        while current_node.given:
            current_node_coords, current_node = go_forward(current_node_coords, grid)
            if current_node_coords == [9, 0]:
                return grid

        current_node = grid[current_node_coords[0]][current_node_coords[1]]
        possible_values = find_possible_values(current_node, grid)

        while len(possible_values) == 0:
            current_node.tried.clear()

            current_node_coords, current_node = go_back(current_node_coords, grid)

            while current_node.given:
                current_node_coords, current_node = go_back(current_node_coords, grid)

            if current_node.value not in current_node.tried and current_node.value != 0:
                current_node.tried.append(current_node.value)

            current_node.value = 0
            possible_values = find_possible_values(current_node, grid)

        rand_value = random.choice(possible_values)
        current_node.value = rand_value
        current_node.tried.append(current_node.value)

        current_node_coords, current_node = go_forward(current_node_coords, grid)
        if current_node_coords == [9, 0]:
            return grid


def make_grid():
    grid = [[Slot(0, (x, i), False) for i in range(9)] for x in range(9)]

    solve(grid)

    return grid


def get_clicked():
    x, y = pygame.mouse.get_pos()

    row = int(x // (WIDTH / 9))
    col = int(y // (WIDTH / 9))

    return row, col


def make_unsolved(grid, empty_no):
    for row in grid:
        for value in row:
            value.given = True
    row = -1
    col = -1
    tried_pos = []
    for _ in range(empty_no):
        while (row, col) in tried_pos:
            row = random.randint(0, 8)
            col = random.randint(0, 8)
        grid[row][col].dummy_value = 0
        grid[row][col].given = False
        tried_pos.append((row, col))
    return grid


def check_grid(grid):
    correct = True
    for row in grid:
        for value in row:
            if not (value.given or value.dummy_value == value.value):
                correct = False
    return correct


def end_game():
    global font, run, started

    theme.stop()

    font = pygame.font.Font("C:\mmmahrous\Zeiad\Programming\Sudoku game and solver\Assets\Sudoku.ttf", 150)
    txt = font.render("YOU WIN!", False, DARK_BLUE)
    WINDOW.blit(txt, (50, 200))
    # win_sound.play()
    pygame.draw.ellipse(WINDOW, LIGHT_BLUE, (240, 350, 130, 55))
    font = pygame.font.Font("C:\mmmahrous\Zeiad\Programming\Sudoku game and solver\Assets\Sudoku.ttf", 35)
    WINDOW.blit(font.render("RETRY", False, GREY), (265, 360))
    pygame.display.update()
    retry = False
    while not retry:
        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                retry = True

            if pygame.mouse.get_pressed(3)[0] and 239 < pos[0] < 371 and 351 < pos[1] < 406:
                retry = True
                font = font = pygame.font.Font("C:\mmmahrous\Zeiad\Programming\Sudoku game and solver\Assets\COMIC.TTF", 35)
                started = False
                main()


def menu():
    global font
    WINDOW.fill(WHITE)
    font = pygame.font.Font("C:\mmmahrous\Zeiad\Programming\Sudoku game and solver\Assets\Sudoku.ttf", 180)
    WINDOW.blit(font.render("SUDOKU", False, DARK_BLUE), (30, 30))

    font = pygame.font.Font("C:\mmmahrous\Zeiad\Programming\Sudoku game and solver\Assets\Sudoku.ttf", 35)
    pygame.draw.ellipse(WINDOW, LIGHT_BLUE, (230, 250, 150, 55))
    WINDOW.blit(font.render("EASY", False, GREY), (270, 260))

    pygame.draw.ellipse(WINDOW, LIGHT_BLUE, (230, 320, 150, 55))
    WINDOW.blit(font.render("HARD", False, GREY), (270, 330))

    pygame.display.update()


def highlight_correct_group(grid):
    for row in grid:
        correct = True
        for value in row:
            if value.value != value.dummy_value and not value.given:
                correct = False
        if correct:
            for value in row:
                value.bg_color[1] = GREEN
    
    for col in range(9):
        correct = True
        for row in grid:
            if row[col].value != row[col].dummy_value and not row[col].given:
                correct = False
        if correct:
            for row in grid:
                row[col].bg_color[1] = GREEN

    for i in [grid[1][1], grid[1][4], grid[1][7], grid[4][1], grid[4][4], grid[4][7], grid[7][1], grid[7][4], grid[7][7]]:
        correct = True
        for value in get_box_values(i, grid):
            if value.value != value.dummy_value and not value.given:
                correct = False
        if correct:
            for value in get_box_values(i, grid):
                value.bg_color[1] = GREEN



def main():
    global game_over, run, started, mode, font

    # theme.play(100)

    selected_node = None
    grid = make_grid()

    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if not started:
                if pygame.mouse.get_pressed(3)[0]:
                    pos = pygame.mouse.get_pos()
                    if 229 < pos[0] < 381:
                        if 249 < pos[1] < 306:
                            mode = 0  # 0 is easy 1 is hard
                            started = True
                            font = pygame.font.Font("C:\mmmahrous\Zeiad\Programming\Sudoku game and solver\Assets\COMIC.TTF", 35)
                            grid = make_unsolved(grid, 50)
                        elif 319 < pos[1] < 376:
                            mode = 1
                            started = True
                            font = pygame.font.Font("C:\mmmahrous\Zeiad\Programming\Sudoku game and solver\Assets\COMIC.TTF", 35)
                            grid = make_unsolved(grid, 50)

            else:
                row, col = get_clicked()
                if pygame.mouse.get_pressed(3)[0] and row < 9 and col < 9:
                    selected_node = grid[row][col]
                    selected_node.make_selected(grid)

                if event.type == pygame.KEYDOWN and selected_node is not None and not selected_node.given and selected_node.bg_color[1] != GREEN:
                    if event.key == pygame.K_0:
                        selected_node.dummy_value = 0

                    if event.key == pygame.K_1:
                        selected_node.dummy_value = 1

                    if event.key == pygame.K_2:
                        selected_node.dummy_value = 2

                    if event.key == pygame.K_3:
                        selected_node.dummy_value = 3

                    if event.key == pygame.K_4:
                        selected_node.dummy_value = 4

                    if event.key == pygame.K_5:
                        selected_node.dummy_value = 5

                    if event.key == pygame.K_6:
                        selected_node.dummy_value = 6

                    if event.key == pygame.K_7:
                        selected_node.dummy_value = 7

                    if event.key == pygame.K_8:
                        selected_node.dummy_value = 8

                    if event.key == pygame.K_9:
                        selected_node.dummy_value = 9

                    if mode == 0:
                        if selected_node.dummy_value == selected_node.value:
                            selected_node.make_correct()
                        else:
                            selected_node.make_wrong()
                    else:
                        selected_node.color = DARK_BLUE

                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    for row in grid:
                        for value in row:
                            value.dummy_value = value.value
                            value.color = BLACK
                    game_over = True
        if not started:
            menu()
        else:
            draw(grid)
            highlight_correct_group(grid)
            game_over = check_grid(grid)

            if game_over:
                end_game()

    pygame.quit()


main()
