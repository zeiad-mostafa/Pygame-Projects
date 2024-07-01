# بسم الله الرحمن الرحيم

import pygame
import operator
from math import sqrt

HEIGHT, WIDTH = 640, 640
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()

WHITE = (255, 229, 204)
BLACK = (135, 62, 35)
GREY = (208, 197, 194)

PIECES = {(0, 1): pygame.transform.scale(pygame.image.load("C:\mmmahrous\Zeiad\Programming\Chess\Assets\Black Pawn.png"),   (50, 62)),
          (0, 2): pygame.transform.scale(pygame.image.load("C:\mmmahrous\Zeiad\Programming\Chess\Assets\Black Knight.png"), (62, 62)),
          (0, 3): pygame.transform.scale(pygame.image.load("C:\mmmahrous\Zeiad\Programming\Chess\Assets\Black Bishop.png"), (57, 62)),
          (0, 4): pygame.transform.scale(pygame.image.load("C:\mmmahrous\Zeiad\Programming\Chess\Assets\Black Rook.png"),   (57, 62)),
          (0, 5): pygame.transform.scale(pygame.image.load("C:\mmmahrous\Zeiad\Programming\Chess\Assets\Black Queen.png"),  (65, 62)),
          (0, 6): pygame.transform.scale(pygame.image.load("C:\mmmahrous\Zeiad\Programming\Chess\Assets\Black King.png"),   (64, 65)),
          (1, 1): pygame.transform.scale(pygame.image.load("C:\mmmahrous\Zeiad\Programming\Chess\Assets\White Pawn.png"),   (50, 62)),
          (1, 2): pygame.transform.scale(pygame.image.load("C:\mmmahrous\Zeiad\Programming\Chess\Assets\White Knight.png"), (62, 62)),
          (1, 3): pygame.transform.scale(pygame.image.load("C:\mmmahrous\Zeiad\Programming\Chess\Assets\White Bishop.png"), (57, 62)),
          (1, 4): pygame.transform.scale(pygame.image.load("C:\mmmahrous\Zeiad\Programming\Chess\Assets\White Rook.png"),   (57, 62)),
          (1, 5): pygame.transform.scale(pygame.image.load("C:\mmmahrous\Zeiad\Programming\Chess\Assets\White Queen.png"),  (65, 62)),
          (1, 6): pygame.transform.scale(pygame.image.load("C:\mmmahrous\Zeiad\Programming\Chess\Assets\White King.png"),   (64, 65)),
}
w_castle_qs = False
w_castle_ks = False
b_castle_qs = False
b_castle_ks = False

w_moved = False
b_moved = False

w_check = False
b_check = False

turn = 1

class Piece:
    def __init__(self, id, square):
        self.id = id
        self.possible_squares = []
        self.square = square

    def check_possible_squares(self):
        self.possible_squares = []
        if self.id[0] == 0 and self.id[1] == 1:            # BLACK PAWN  
            self.check_pawn_move(operator.sub, 6)

        elif self.id[0] == 1 and self.id[1] == 1:          # WHITE PAWN  
            self.check_pawn_move(operator.add, 1)
        
        elif self.id[1] == 2:                              # HORSE       
            self.check_T(operator.add, 1)
            self.check_T(operator.add, 2)
            self.check_T(operator.sub, 1)
            self.check_T(operator.sub, 2)

        elif self.id[1] == 3:                              # BISHOP      
            self.check_diagonal(operator.add, operator.add)
            self.check_diagonal(operator.add, operator.sub)
            self.check_diagonal(operator.sub, operator.add)
            self.check_diagonal(operator.sub, operator.sub)

        elif self.id[1] == 4:                              # ROOK        
            self.check_straight(operator.add, True)
            self.check_straight(operator.sub, True)
            self.check_straight(operator.add, False)
            self.check_straight(operator.sub, False)

        elif self.id[1] == 5:                              # QUEEN       
            self.check_straight(operator.add, True)
            self.check_straight(operator.sub, True)
            self.check_straight(operator.add, False)
            self.check_straight(operator.sub, False)

            # *********PART2*********
            self.check_diagonal(operator.add, operator.add)
            self.check_diagonal(operator.add, operator.sub)
            self.check_diagonal(operator.sub, operator.add)
            self.check_diagonal(operator.sub, operator.sub)

        elif self.id[1] == 6:                              # KING        
            if self.id[0] == 0:
                for i in (-1, 1):
                    pos = (self.square.row, self.square.column + i)
                    if -1 < pos[0] < 8 and -1 < pos[1] < 8:
                        if squares[pos[0]][pos[1]].piece.id[1] == 0 or squares[pos[0]][pos[1]].piece.id[0] == 1:
                            self.possible_squares.append((self.square.row, self.square.column + i))

                    pos = (self.square.row + i, self.square.column)
                    if -1 < pos[0] < 8 and -1 < pos[1] < 8:
                        if squares[pos[0]][pos[1]].piece.id[1] == 0 or squares[pos[0]][pos[1]].piece.id[0] == 1:
                            self.possible_squares.append((self.square.row + i, self.square.column))

                    pos = (self.square.row + i, self.square.column + i)
                    if -1 < pos[0] < 8 and -1 < pos[1] < 8:
                        if squares[pos[0]][pos[1]].piece.id[1] == 0 or squares[pos[0]][pos[1]].piece.id[0] == 1:
                            self.possible_squares.append((self.square.row + i, self.square.column + i))

                    pos = (self.square.row - i, self.square.column + i)
                    if -1 < pos[0] < 8 and -1 < pos[1] < 8:
                        if squares[pos[0]][pos[1]].piece.id[1] == 0 or squares[pos[0]][pos[1]].piece.id[0] == 1:
                            self.possible_squares.append((self.square.row - i, self.square.column + i))
            else:
                for i in (-1, 1):
                    pos = (self.square.row, self.square.column + i)
                    if -1 < pos[0] < 8 and -1 < pos[1] < 8:
                        if squares[pos[0]][pos[1]].piece.id[0] == 0:
                            self.possible_squares.append((self.square.row, self.square.column + i))

                    pos = (self.square.row + i, self.square.column)
                    if -1 < pos[0] < 8 and -1 < pos[1] < 8:
                        if squares[pos[0]][pos[1]].piece.id[0] == 0:
                            self.possible_squares.append((self.square.row + i, self.square.column))

                    pos = (self.square.row + i, self.square.column + i)
                    if -1 < pos[0] < 8 and -1 < pos[1] < 8:
                        if squares[pos[0]][pos[1]].piece.id[0] == 0:
                            self.possible_squares.append((self.square.row + i, self.square.column + i))

                    pos = (self.square.row - i, self.square.column + i)
                    if -1 < pos[0] < 8 and -1 < pos[1] < 8:
                        if squares[pos[0]][pos[1]].piece.id[0] == 0:
                            self.possible_squares.append((self.square.row - i, self.square.column + i))
            
            # CASTLING
            if self.id[0] == 1 and not w_moved and not w_check:
                if w_castle_ks:
                    self.possible_squares.append((0, 6))
                if w_castle_qs:
                    self.possible_squares.append((0, 2))

            elif not b_moved and not b_check:
                if b_castle_ks:
                    self.possible_squares.append((7, 6))
                if b_castle_qs:
                    self.possible_squares.append((7, 2))
        
        try:
            self.possible_squares.remove((self.square.row, self.square.column))
        except ValueError:
            pass

    
    def check_straight(self, op, horizontal):
        counter = 1
        try:
            if horizontal:
                while squares[self.square.row][op(self.square.column, counter)].piece.id[1] == 0:
                    self.possible_squares.append((self.square.row, op(self.square.column, counter)))
                    counter += 1
                    if op(self.square.column, counter) < 0 or op(self.square.column, counter) > 7:
                        break
                else:
                    if squares[self.square.row][op(self.square.column, counter)].piece.id[0] != self.id[0]:
                        self.possible_squares.append((self.square.row, op(self.square.column, counter)))


            else:
                while squares[op(self.square.row, counter)][self.square.column].piece.id[1] == 0:
                    self.possible_squares.append((op(self.square.row, counter), self.square.column))
                    counter += 1
                    if op(self.square.row, counter) < 0 or op(self.square.row, counter) > 7:
                        break
                    
                else:
                    if squares[op(self.square.row, counter)][self.square.column].piece.id[0] != self.id[0]:
                        self.possible_squares.append((op(self.square.row, counter), self.square.column))
        except IndexError:
            pass  
    
    def check_T(self, op, mode):
        for i in range(1, 4, 2):
                if mode == 1:
                    target_row = op(self.square.row, 2)
                    target_column = self.square.column + i - 2
                else:
                    target_row = self.square.row + i - 2
                    target_column = op(self.square.column, 2)

                if 8 > target_row > -1 and 8 > target_column > -1:
                    if (squares[target_row][target_column].piece.id[1] == 0) or (squares[target_row][target_column].piece.id[0] != self.id[0]):
                        self.possible_squares.append((target_row, target_column))

    def check_diagonal(self, op1, op2):
        counter = 1

        if -1 < op1(self.square.row, counter) < 8 and -1 < op2(self.square.column, counter) < 8:
                while squares[op1(self.square.row, counter)][op2(self.square.column, counter)].piece.id[1] == 0:
                    self.possible_squares.append((op1(self.square.row, counter), op2(self.square.column, counter)))
                    counter += 1

                    if not ( -1 < op1(self.square.row, counter) < 8 and -1 < op2(self.square.column, counter) < 8):
                        break

                else:
                    if squares[op1(self.square.row, counter)][op2(self.square.column, counter)].piece.id[0] != self.id[0]:
                        self.possible_squares.append((op1(self.square.row, counter), op2(self.square.column, counter)))
        
    def check_pawn_move(self, op, start_row):
        if squares[op(self.square.row, 1)][self.square.column].piece.id[1] == 0:
                self.possible_squares.append((op(self.square.row, 1), self.square.column))

                if op(self.square.row, 2) != 8 and op(self.square.row, 2) != -1:    
                    if squares[op(self.square.row, 2)][self.square.column].piece.id[1] == 0 and self.square.row == start_row:
                        self.possible_squares.append((op(self.square.row, 2), self.square.column))
            
        if self.square.column != 7:
            if squares[op(self.square.row, 1)][self.square.column + 1].piece.id[1] != 0 and squares[op(self.square.row, 1)][self.square.column + 1].piece.id[0] != self.id[0]:
                self.possible_squares.append((op(self.square.row, 1), self.square.column + 1))
            
        if self.square.column != 0:
            if squares[op(self.square.row, 1)][self.square.column - 1].piece.id[1] != 0 and squares[op(self.square.row, 1)][self.square.column - 1].piece.id[0] != self.id[0]:
                self.possible_squares.append((op(self.square.row, 1), self.square.column - 1))

    def promote(self):
        self.id = ( self.id[1], int(input("2 : Knight\n3 : Bishop\n4 : Rook\n5 : Queen\n: ")))

    def castle(self, mode):
        # mode = 1: king side,     mode = 2: queen side
        if mode == 6:
            key_squares = (mode, 5, 7)
        else:
            key_squares = (mode, 3, 0)

        squares[self.square.row][key_squares[0]].piece = Piece(self.id, squares[self.square.row][key_squares[0]])
        squares[self.square.row][self.square.column].piece = Piece((0, 0), squares[self.square.row][self.square.column])
        squares[self.square.row][key_squares[1]].piece = Piece((self.id[0], 4), squares[self.square.row][key_squares[1]])
        squares[self.square.row][key_squares[2]].piece = Piece((0, 0), squares[self.square.row][key_squares[2]])


    
class Square:
    def __init__(self, row, column):
        self.row = row
        self.column = column
        if column % 2 == 0:
            if row % 2 == 0:
                self.color = BLACK
            else:
                self.color = WHITE
        else:
            if row % 2 == 0:
                self.color = WHITE
            else:
                self.color = BLACK

# FIRST ELEMENT  0: Black           1: White
# SECOND ELEMENT 0: empty          1: Pawn          2: Knight         3: Bishop           4: Rook          5: Queen         6: King
        if row == 1:
            self.piece = Piece((1, 1), self)
        elif row == 6:
            self.piece = Piece((0, 1), self)

        elif row == 0 or row == 7:
            if row == 0:
                color = 1
            else:
                color = 0

            if column == 0 or column == 7:
                self.piece = Piece((color, 4), self)

            elif column == 1 or column == 6:
                self.piece = Piece((color, 2), self)

            elif column == 2 or column == 5:
                self.piece = Piece((color, 3), self)

            elif column == 3:
                self.piece = Piece((color, 5), self)

            elif column == 4:
                self.piece = Piece((color, 6), self)
        else:
            self.piece = Piece((0, 0), self)

        self.pos = (column * 80, (7 - row) * 80)

        self.selected = False

    def draw_piece(self):
        if self.piece.id[1] != 0:
            if not self.selected:
                WIN.blit(PIECES[self.piece.id], (self.pos[0] + 10, self.pos[1] + 10))
            else:
                WIN.blit(PIECES[self.piece.id], (pygame.mouse.get_pos()[0] - 20, pygame.mouse.get_pos()[1] - 24))

    def draw_square(self):
        pygame.draw.rect(WIN, self.color, (self.pos[0], self.pos[1], 80, 80))
    
    def draw_selection(self):
        for square in self.piece.possible_squares:
            pygame.draw.circle(WIN, GREY, (squares[square[0]][square[1]].column * 80 + 40, (7 - squares[square[0]][square[1]].row) * 80 + 40), 15)


def main():
    global squares, w_castle_ks, w_castle_qs, b_castle_ks, b_castle_qs, w_moved, b_moved, turn, w_check, b_check

    origin_square = None

    run = True
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                origin_square = squares[7 - (pos[1] // 80)][pos[0] // 80]
                if origin_square.piece.id[0] == turn:
                    origin_square.selected = True
                    origin_square.piece.check_possible_squares()
                else:
                    origin_square = None

            if event.type == pygame.MOUSEBUTTONUP and origin_square is not None:
                pos = list(pygame.mouse.get_pos())
                if pos[0] < 0:
                    pos[0] = 0
                elif pos[0] > 640:
                    pos[0] = 640
                
                if pos[1] < 0:
                    pos[1] = 0
                elif pos[1] > 640:
                    pos[1] = 640

                destination_square = squares[7 - (pos[1] // 80)][pos[0] // 80]

                origin_square.piece.check_possible_squares()
                if (destination_square.row, destination_square.column) in origin_square.piece.possible_squares:
                    if origin_square.piece.id[1] == 6:
                        d = sqrt((origin_square.row - destination_square.row)**2 + (origin_square.column - destination_square.column)**2)
                        if d < 2:
                            if origin_square.piece.id[0] == 1:
                                w_moved = True
                            else:
                                b_moved = True
                            destination_square.piece = Piece(origin_square.piece.id, destination_square)
                            origin_square.piece = Piece((0, 0), origin_square)

                        else:
                            origin_square.piece.castle(destination_square.column)
                            w_moved, b_moved = True, True
                    else:
                        destination_square.piece = Piece(origin_square.piece.id, destination_square)
                        origin_square.piece = Piece((0, 0), origin_square)

                        if (destination_square.row == 0 or destination_square.row == 7) and destination_square.piece.id[1] == 1:
                            destination_square.piece.promote()
                    turn = int(not turn)

                origin_square.selected = False
                origin_square = None

                w_check, b_check = False, False
                for row in squares:
                    for square in row:
                        if square.piece.id[0] != turn:
                            square.piece.check_possible_squares()
                            for square in square.piece.possible_squares:
                                if squares[square[0]][square[1]].piece.id[1] == 6:
                                    if squares[square[0]][square[1]].piece.id[0] == 0:
                                        b_check = True
                                    else:
                                        w_check = True

        #   ***************************CASTLING CHECK***************************
        if squares[0][5].piece.id[1] == 0 and squares[0][6].piece.id[1] == 0:
            w_castle_ks = True
        else:
            w_castle_ks = False
        
        if squares[0][1].piece.id[1] == 0 and squares[0][2].piece.id[1] == 0 and squares[0][3].piece.id[1] == 0:
            w_castle_qs = True
        else:
            w_castle_qs = False
        
        if squares[7][5].piece.id[1] == 0 and squares[7][6].piece.id[1] == 0:
            b_castle_ks = True
        else:
            b_castle_ks = False
        
        if squares[7][1].piece.id[1] == 0 and squares[7][2].piece.id[1] == 0 and squares[7][3].piece.id[1] == 0:
            b_castle_qs = True
        else:
            b_castle_qs = False
        #   \***************************CASTLING CHECK***************************
        
        for row in squares:
            for square in row:
                square.draw_square()

        for row in squares:
            for square in row:
                square.draw_piece()
        
        if origin_square is not None:
            origin_square.draw_selection()
        pygame.display.update()


squares = [[] for _ in range(8)]

for i in range(8):
    for j in range(8):
        squares[i].append(Square(i, j))

main()
pygame.quit()