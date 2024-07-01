import pygame
import time

pygame.init()

width, height = 1035, 600
button_width, button_height = 200, 60
button_x,  button_y = width - button_width - 20, 20

window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Space Invaders")

yellow_hit = pygame.USEREVENT + 1
red_hit = pygame.USEREVENT + 2

white = (255, 255, 255)
red_color = (255, 0, 0)
yellow_color = (255, 255, 0)
green = (0, 255, 0)

font = pygame.font.Font("C:\mmmahrous\Zeiad\Programming\Space Invaders\Assets\grinched.otf", 40)

FPS = 60
yellow_vel = 6
red_vel = 6
yellow_bullet_vel = 9
red_bullet_vel = 9
count = 0

left = 1

border = pygame.Rect(width/2 - 5, 0, 10, height)

red_bullets = []
yellow_bullets = []
powerups = []
yellow_bullet_count = 0
red_bullet_count = 0
red_health = 10
yellow_health = 10
red_max_bullets = 5
yellow_max_bullets = 6
start = time.time()
run = True

background = pygame.image.load("C:\mmmahrous\Zeiad\Programming\Space Invaders\Assets\Earth-from-space-1-64e9a7c.jpg")
game_over_bg = pygame.image.load("C:\mmmahrous\Zeiad\Programming\Space Invaders\Assets\Game Over.jpg")


silencer_gun = pygame.mixer.Sound("C:\mmmahrous\Zeiad\Programming\Space Invaders\Assets\Gun+Silencer.mp3")
grenade = pygame.mixer.Sound("C:\mmmahrous\Zeiad\Programming\Space Invaders\Assets\Grenade+1.mp3")
# theme = pygame.mixer.Sound("C:\mmmahrous\Zeiad\Programming\Space Invaders\Assets\Boss Theme.mp3")
win_song = pygame.mixer.Sound("C:\mmmahrous\Zeiad\Programming\Space Invaders\Assets\win.wav")

# Defining Spaceships
spaceship_width, spaceship_height = 65, 50

yellow_ship_img = pygame.image.load("C:\mmmahrous\Zeiad\Programming\Space Invaders\Assets\spaceship_yellow.png")
yellow_ship = pygame.transform.rotate(pygame.transform.scale(yellow_ship_img, (spaceship_width, spaceship_height)), 270)

red_ship_img = pygame.image.load("C:\mmmahrous\Zeiad\Programming\Space Invaders\Assets\spaceship_red.png")
red_ship = pygame.transform.rotate(pygame.transform.scale(red_ship_img, (spaceship_width, spaceship_height)), 90)

yellow = pygame.Rect((width/2 + width/4, height/2, spaceship_width, spaceship_height))
red = pygame.Rect((width/4, height/2, spaceship_width, spaceship_height))


def red_bullets_handling(red_bullets, yellow):
    global red_health

    for bullet in red_bullets:
        bullet.x += red_bullet_vel
        if yellow.colliderect(bullet):
            red_bullets.remove(bullet)
            red_health -= 1
        if bullet.x >= width:
            red_bullets.remove(bullet)

    return red_health


def yellow_bullets_handling(yellow_bullets, red):
    global yellow_health

    for bullet in yellow_bullets:
        bullet.x -= yellow_bullet_vel
        if red.colliderect(bullet):
            yellow_bullets.remove(bullet)
            yellow_health -= 1
        if bullet.x <= 0:
            yellow_bullets.remove(bullet)

    return yellow_health


def draw(yellow_player, red_player, red_bullets, yellow_bullets, red_health, yellow_health):

    window.blit(background, (0, 0))

    red_text = font.render(f"Health: {yellow_health}", False, red_color)
    yellow_text = font.render(f"Health: {red_health}", False, yellow_color)

    window.blit(red_text, (0, 0))
    window.blit(yellow_text, (width/2 + 5, 0))

    pygame.draw.rect(window, white, border)

    window.blit(red_ship, (red_player.x, red_player.y))
    window.blit(yellow_ship, (yellow_player.x, yellow_player.y))

    for bullet in yellow_bullets:
        pygame.draw.rect(window, yellow_color, bullet)
    for bullet in red_bullets:
        pygame.draw.rect(window, red_color, bullet)

    pygame.display.update()


def yellow_movement(yellow_pos, keys):
    if keys[pygame.K_LEFT] and yellow_pos.x - yellow_vel >= border.x + border.width:  # left
        yellow_pos.x -= yellow_vel
    if keys[pygame.K_RIGHT] and yellow_pos.x + yellow_vel + 40 < width:  # right P.S. the added part is to adjust
        yellow_pos.x += yellow_vel
    if keys[pygame.K_UP] and yellow_pos.y - yellow_vel > 0:  # up
        yellow_pos.y -= yellow_vel
    if keys[pygame.K_DOWN] and yellow.y + yellow_vel + 60 < height:  # down P.S. the added part is to adjust
        yellow_pos.y += yellow_vel


def red_movement(red_pos, keys):
    if keys[pygame.K_a] and red_pos.x + red_vel > 0:  # left
        red_pos.x -= red_vel
    if keys[pygame.K_d] and red_pos.x + red_pos.width + red_vel - 20 < border.x:  # right  P.S. the subtracted part is to adjust
        red_pos.x += red_vel
    if keys[pygame.K_w] and red_pos.y > 0:  # up
        red_pos.y -= red_vel
    if keys[pygame.K_s] and red_pos.y + red_pos.height + red_vel + 10 < height:  # down P.S. the added part is to adjust
        red_pos.y += red_vel


def game_over():
    global run

    window.blit(game_over_bg, (0, 0))

    restart_button = pygame.Rect(button_x, button_y, button_width, button_height)
    pygame.draw.rect(window, green, restart_button)

    font = pygame.font.Font("C:\mmmahrous\Zeiad\Programming\Space Invaders\Assets\grinched.otf", 30)
    button_txt = font.render("Restart?", False, white)
    window.blit(button_txt, (button_x + 40, 0 + 30))

    font = pygame.font.Font("C:\mmmahrous\Zeiad\Programming\Space Invaders\Assets\grinched.otf", 100)
    winner_txt = font.render(f"{winner} WINS", False, white)
    window.blit(winner_txt, (width / 2 - 210, height / 2 - 200))

    pygame.display.update()

    restart = False
    while not restart:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                restart = True
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                if pos[0] in range(button_x, button_x + button_width) and pos[1] in range(button_y,
                                                                                          button_y + button_height):
                    red_bullets.clear()
                    yellow_bullets.clear()

                    yellow.x, yellow.y = width / 2 + width / 4, height / 2
                    red.x, red.y = width / 4, height / 2

                    # theme.play()

                    restart = True


def declare_winner(winner):
    global yellow_health
    global red_health

    font = pygame.font.Font("C:\mmmahrous\Zeiad\Programming\Space Invaders\Assets\grinched.otf", 80)
    winner_txt = font.render(f"{winner} WINS", False, (0, 255, 0))
    window.blit(winner_txt, (width/2 - 210, height/2 - 80))

    # theme.stop()
    win_song.play()

    pygame.display.update()

    time.sleep(3)

    win_song.stop()
    yellow_health = 10
    red_health = 10


def main():
    global winner
    global run

    # theme.play()

    fps_adjuster = pygame.time.Clock()

    while run:
        fps_adjuster.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e and len(red_bullets) < red_max_bullets:
                    pygame.mixer.Sound.play(silencer_gun)
                    red_bullets.append(
                        pygame.Rect((float(red.x + red.width), red.y + red.height / 2, 35, 7)))

                if event.key == pygame.K_RCTRL and len(yellow_bullets) < yellow_max_bullets:
                    pygame.mixer.Sound.play(grenade)
                    yellow_bullets.append(
                        pygame.Rect((float(yellow.x - yellow.width), yellow.y + yellow.height / 2, 35, 7)))

        keys = pygame.key.get_pressed()

        yellow_health = yellow_bullets_handling(yellow_bullets, red)
        red_health = red_bullets_handling(red_bullets, yellow)

        draw(yellow, red, red_bullets, yellow_bullets, red_health, yellow_health)

        red_movement(red, keys)

        yellow_movement(yellow, keys)

        if red_health == 0 or yellow_health == 0:
            if red_health == 0:
                winner = "Red"
                declare_winner(winner)

            if yellow_health == 0:
                winner = "Yellow"
                declare_winner(winner)

            game_over()

    pygame.quit()


if __name__ == "__main__":
    main()
