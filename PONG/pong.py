import time
import pygame
import random

pygame.init()

font = pygame.font.SysFont("yugothic", 20)

# theme = pygame.mixer.Sound("C:\mmmahrous\Zeiad\Programming\PONG/theme.mp3")
# win = pygame.mixer.Sound("C:\mmmahrous\Zeiad\Programming\PONG/win.mp3")

WIDTH, HEIGHT = 1000, 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PONG")


class Player:
    def __init__(self, num, bot):
        self.num = num

        if num == 1:
            self.racket = pygame.rect.Rect(20, HEIGHT / 2 - 30, 15, 85)
        else:
            self.racket = pygame.rect.Rect(WIDTH - 40, HEIGHT / 2 - 30, 15, 85)
        
        self.score = 0
        self.bot = bot
    
    def score_point(self):
        global ball, start, started

        self.score += 1
        ball.rec = pygame.rect.Rect(WIDTH / 2 - 10, HEIGHT / 2 - 10, 20, 20)
        started = False 
        start = False

        if self.score == 3:
            self.win()

    def reset(self):
        self.racket.top = HEIGHT / 2 - 30
    
    def win(self):
        global end, run
        # theme.stop()
        # win.play()
        end = True
        font = pygame.font.Font("C:\mmmahrous\Zeiad\Programming\PONG\ARCADECLASSIC.TTF", 100)
        WINDOW.blit(font.render("PLAYER " + str(self.num) + " WON", False, BLUE), (200, 250))
        pygame.display.update()
        time.sleep(8)
        run = False


class Ball:
    def __init__(self):
        self.m = 0
        self.direction = 0
        self.rec = pygame.rect.Rect(WIDTH / 2 - 10, HEIGHT / 2 - 10, 20, 20)
        self.speed = 4


player1 = Player(1, False)
player2 = Player(2, False)
racket_speed = 8

ball = Ball()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (128, 128, 128)
RED = (255, 0, 0)
BLUE = (0, 0, 255) 

FPS = 60
clock = pygame.time.Clock()
end = False   # Whether to end the game
run = True 
start = False   #  Whether the game has started
started = False   # Whether the ball has started moving between scores
chosen = False  # Whether the player has chosen to play against another player or a bot,   not chosen yet = 0, 1 player = 1, 2 players = 2

x_to_move = 0
y_to_move = 0
bounced = False
calculated1 = False
calculated2 = False
dest = 0

# Start buttons
button_1 = pygame.rect.Rect(WIDTH / 2 - 75, HEIGHT / 2.5, 150, 30)
button_2 = pygame.rect.Rect(WIDTH / 2 - 75, HEIGHT / 2.5 + 60, 150, 30)

def draw():


    WINDOW.fill(BLACK)
    pygame.draw.rect(WINDOW, WHITE, player1.racket)
    pygame.draw.rect(WINDOW, WHITE, player2.racket)

    pygame.draw.rect(WINDOW, WHITE, (WIDTH / 2 - 5, 0, 10, HEIGHT))

    pygame.draw.rect(WINDOW, GREY, ball.rec)

    WINDOW.blit(font.render("PLAYER 1: " + str(player1.score), False, BLUE), ((10, 0)))
    WINDOW.blit(font.render("PLAYER 2: " + str(player2.score), False, BLUE), ((870, 0)))
    
    pygame.display.update()


def player1_movement(keys):
    global start

    if keys[pygame.K_w] and player1.racket.top >= 0:
        player1.racket.top -= racket_speed
        start = True
    if keys[pygame.K_s] and player1.racket.top + player1.racket.height <= HEIGHT:
        player1.racket.top += racket_speed
        start = True
    

def update_data(ball_status, player_racket):
    c = ball_status[1] - ball_status[2] * ball_status[0]
    y = ball_status[2] * player_racket.left + c
    return y, c


def future_ball_pos(player_racket):
    ball_status = [ball.rec.right, HEIGHT - ball.rec.top, ball.m]
    y, c = update_data(ball_status, player_racket)

    while (y) > HEIGHT or (y) < 0:
        if y > HEIGHT:   # I'm taking HEIGHT - ball.rec.top instead of the top alone because the y in pygame is inverted
            ball_status = [(HEIGHT - c) / ball_status[2], HEIGHT, ball_status[2] * -1]
            y, c = update_data(ball_status, player_racket)

        elif y < 0:
            ball_status = [-c / ball_status[2], ball.rec.height, ball_status[2] * -1]
            y, c = update_data(ball_status, player_racket)

    return y


def player2_movement(keys):
    global start, started, dest, calculated1

    if not player2.bot:
        if keys[pygame.K_UP] and player2.racket.top >= 0:
            start = True
            player2.racket.top -= racket_speed
        if keys[pygame.K_DOWN] and player2.racket.top + player2.racket.height <= HEIGHT:
            player2.racket.top += racket_speed
            start = True
# Bot movement explanation:
# If the ball is moving away from it, it remains stationary
# Otherwise, the ball position when it reaches the bot's left border is calculated
# Then the bot moves to that position
    else:
        if started:
            if not calculated1:
                dest = HEIGHT - future_ball_pos(player2.racket)  # Have to subtract it from HEIGHT cus pygame coords r flipped
                calculated1 = True
            if dest != player2.racket.center[1]:
                if dest > player2.racket.center[1]:
                    if dest - player2.racket.center[1] > racket_speed:
                        player2.racket.top += racket_speed
                    else:
                        player2.racket.top = dest - player2.racket.height / 2
                else:
                    if player2.racket.center[1] - dest > racket_speed:
                        player2.racket.top -= racket_speed
                    else:
                        player2.racket.top = dest - player2.racket.height / 2


def change_direction(ball, bounce_surface): # if bounce_surface = 1, the ball bounced off of player1, if bounce_surface = 2 the ball bounced off of player 2 otherwise it bounced off the edge of the screen
    global x_to_move, y_to_move, bounced, calculated1

    keys = pygame.key.get_pressed()
    # If the ball hits the player and he is moving in the same direction as the ball, its gradient gets steeper, otherwise it levels out a bit
        # If the ball hits either edge of the player, it moves sharply down or up
    if bounce_surface == 1:
        calculated1 = False
        if not bounced:
            ball.direction *= -1
            bounced = True

        if ball.m > 0 and keys[pygame.K_w] or ball.m < 0 and keys[pygame.K_s]:
            ball.m *= random.uniform(1, 1.7)
        elif ball.m > 0 and keys[pygame.K_s] or ball.m < 0 and keys[pygame.K_w]:
            ball.m /= random.uniform(1, 1.7)
            
        if ball.rec.center[1] > player1.racket.top:
            ball.m = random.uniform(1, 2)
        elif ball.rec.center[1] < player1.racket.bottom:
            ball.m = random.uniform(-1, -2)
    
    if bounce_surface == 2:
        if not bounced:
            ball.direction *= -1
            bounced = True

        if ball.m > 0 and keys[pygame.K_UP] or ball.m < 0 and keys[pygame.K_DOWN]:
            ball.m *= random.uniform(1, 1.7)
        elif ball.m > 0 and keys[pygame.K_DOWN] or ball.m < 0 and keys[pygame.K_UP]:
            ball.m /= random.uniform(1, 1.7)
            
        if ball.rec.center[1] > player2.racket.top:
            ball.m = random.uniform(1, 2)
        elif ball.rec.center[1] < player2.racket.bottom:
            ball.m = random.uniform(-1, -2)

    elif bounce_surface == 3:
        ball.m *= -1
    
    x_to_move = ball.speed * ball.direction
    y_to_move = ((ball.rec.left + x_to_move) * ball.m) - (ball.rec.left * ball.m )

def ball_movement():
    global x_to_move, y_to_move, started, bounced
    # This module uses the pythagrean theorem
    # Basically, x is the distance moved right/left and y is the distance moved up/down
    # x and y are two sides of a right triangle and the hypotenuse is the ball_speed
    # y = the gradient(m) * x   (y=mx + c)
    # So (ball_speed)^2 = x^2 + (mx)^2
    # Solve for x
    # Get y by y = mx
    # The y-intercept can be ignored because we it only affects the position of the line, which doesn't matter

    if not started:
        started = True
        ball.m = 0
        ball.speed = 5
        ball.direction = random.choice((1, -1))
        x_to_move = ball.speed * ball.direction
        y_to_move = 0

    if  WIDTH / 2 - 10 < ball.rec.left < WIDTH / 2 + 10:
        bounced = False

    if ball.rec.colliderect(player1.racket) or ball.rec.colliderect(player2.racket) or ball.rec.top < 0 or ball.rec.bottom > HEIGHT:
        ball.speed = 6

        if ball.rec.colliderect(player1.racket):
            change_direction(ball, 1)

        elif ball.rec.colliderect(player2.racket):
            change_direction(ball, 2)

        if ball.rec.top < 0 or ball.rec.bottom > HEIGHT:
            change_direction(ball, 3)

    ball.rec.left += x_to_move
    ball.rec.top -= y_to_move

def check_scored(): # Checks if a player scored a point
    global calculated1

    score = False
    if ball.rec.right <= 0:
        player2.score_point()
        player2.reset()
        player1.reset()
        score = True

    elif ball.rec.left >= WIDTH:
        player1.score_point()
        player2.reset()
        player1.reset()
        score = True

    if score:
        calculated1 = False
        draw()


def start_screen():
    global font, chosen

    WINDOW.fill(BLACK)
    pygame.draw.rect(WINDOW, BLUE, button_1)
    pygame.draw.rect(WINDOW, BLUE, button_2)
    WINDOW.blit(font.render("2 PLAYERS", False, BLACK), (button_1.left + 15, button_1.top + 5))
    WINDOW.blit(font.render("1 PLAYER", False, BLACK), (button_2.left + 20, button_2.top + 5))

    pygame.display.update()

    pos = pygame.mouse.get_pos()
    if ((button_1.left < pos[0] < button_1.right) and (button_1.top < pos[1] < button_1.bottom)) and pygame.mouse.get_pressed()[0]:
        # theme.play(10)
        chosen = True
    
    elif ((button_2.left < pos[0] < button_2.right) and (button_2.top < pos[1] < button_2.bottom)) and pygame.mouse.get_pressed()[0]:
        # theme.play(10)
        chosen = True
        player2.bot = True


def main():
    global run, start, started, chosen

    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        if not end:
            if not chosen:
                start_screen()
            else:
                keys = pygame.key.get_pressed()
                if start:
                    ball_movement()
                player1_movement(keys)
                player2_movement(keys)
                
                draw()
                check_scored()
        
main()
