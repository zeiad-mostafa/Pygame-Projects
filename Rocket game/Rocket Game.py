import pygame
import time
import random

count = 0

pygame.init()
width, height = 900, 650
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Rocket Game")

# setting some variables
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
yellow = (255, 255, 0)
green = (0, 255, 0)

clock = pygame.time.Clock()

background_vel = 6
run = True
click = False
start = time.time()
score = 0
bullets_fired = 0
bullet_vel = 15
bullets = []
bullet_capacity = 5
bullet_wid = 10
bullet_height = 30
multiples = [num * 15 for num in range(1, 100)]
upgrades = []

font = pygame.font.SysFont("C:\mmmahrous\Zeiad\Programming\Rocket game\Assets/ARCADECLASSIC.TTF", 40)
txt = font.render("CLICK TO START", False, black)
txt_rect = pygame.rect.Rect(width/3.5 + 75, 100, 60, 30)

# Defining Sounds
# theme = pygame.mixer.Sound("C:\mmmahrous\Zeiad\Programming\Rocket game\Assets/theme.mp3")
explosion_sound = pygame.mixer.Sound("C:\mmmahrous\Zeiad\Programming\Rocket game\Assets/explosion.wav")
laser = pygame.mixer.Sound("C:\mmmahrous\Zeiad\Programming\Rocket game\Assets/laser.mp3")
break_sound = pygame.mixer.Sound("C:\mmmahrous\Zeiad\Programming\Rocket game\Assets/rock.mp3")
upgrade_sound = pygame.mixer.Sound("C:\mmmahrous\Zeiad\Programming\Rocket game\Assets/powerup get.mp3")

# Defining Upgrades
arrow = pygame.transform.scale(pygame.image.load("C:\mmmahrous\Zeiad\Programming\Rocket game\Assets/arrow.png"), (60, 60))

bullet_img = pygame.transform.scale(pygame.image.load("C:\mmmahrous\Zeiad\Programming\Rocket game\Assets/bullet.png"), (60, 60))

upgrade_dict = {1: arrow,
                2: bullet_img}

# Defining Pictures
game_over_bg = pygame.image.load("C:\mmmahrous\Zeiad\Programming\Rocket game\Assets/gameover.jpg")
game_over_bg = pygame.transform.scale(game_over_bg, (width, height))

explosion = pygame.image.load("C:\mmmahrous\Zeiad\Programming\Rocket game\Assets/explosion.jpg")
explosion = pygame.transform.scale(explosion, (150, 150))

ground = pygame.image.load("C:\mmmahrous\Zeiad\Programming\Rocket game\Assets/ground.png")
ground = pygame.transform.scale(ground, (width, 160))
ground_rect = pygame.rect.Rect(0, height - 100, width, height - height/5)

sky = pygame.image.load("C:\mmmahrous\Zeiad\Programming\Rocket game\Assets/sky.jpg")
sky = pygame.transform.scale(sky, (width, height))
sky_rect = pygame.rect.Rect(0, ground_rect.y - height, width, height)
sky_rect_two = pygame.rect.Rect(0, sky_rect.y - height, width, height)

space = pygame.image.load("C:\mmmahrous\Zeiad\Programming\Rocket game\Assets/space.png")
space = pygame.transform.scale(space, (width, height))
space_backgrounds = [pygame.rect.Rect(0, sky_rect_two.y - height, width, height)]

# Defining Rocket and meteors
rocket_width, rocket_height = 50, 150

grounded_rocket = pygame.image.load("C:\mmmahrous\Zeiad\Programming\Rocket game\Assets/Rocket 2.png")
grounded_rocket = pygame.transform.scale(grounded_rocket, (rocket_width - 10, rocket_height - 60))
grounded_rocket_rect = pygame.rect.Rect(width/2 - 25, height/2 + 140, rocket_width, rocket_height)

flying_rocket = pygame.image.load("C:\mmmahrous\Zeiad\Programming\Rocket game\Assets/Rocket.png")
flying_rocket = pygame.transform.scale(flying_rocket, (rocket_width - 10, rocket_height))
flying_rocket_rect = pygame.rect.Rect(
    grounded_rocket_rect.x, grounded_rocket_rect.y - 15, rocket_width - 17, rocket_height - 60)

meteor_pic = pygame.image.load("C:\mmmahrous\Zeiad\Programming\Rocket game\Assets/meteor.png")
meteor_pic = pygame.transform.scale(meteor_pic, (75, 75))
meteor_lst = []


def takeoff():
    for background in space_backgrounds:
        window.blit(space, (background.x, background.y))

    window.blit(sky, (sky_rect_two.x, sky_rect_two.y))
    window.blit(sky, (sky_rect.x, sky_rect.y))
    window.blit(ground, (ground_rect.x, ground_rect.y))
    window.blit(txt, (txt_rect.x, txt_rect.y))

    window.blit(flying_rocket, (flying_rocket_rect.x, flying_rocket_rect.y))

    pygame.display.update()


def start_screen():
    window.blit(sky, (sky_rect.x, sky_rect.y))
    window.blit(ground, (ground_rect.x, ground_rect.y))
    window.blit(txt, (txt_rect.x, txt_rect.y))

    if sky_rect.y > -1:
        window.blit(sky, (sky_rect_two.y, sky_rect_two.x))

    window.blit(grounded_rocket, (grounded_rocket_rect.x, grounded_rocket_rect.y))

    pygame.display.update()
    
    
def meteor_handling():
    global run, health

    for meteor in meteor_lst:
        meteor[0].y += background_vel
        if meteor[0].colliderect(flying_rocket_rect):
            meteor_lst.remove(meteor)
            break_sound.play()
            game_over()

        if meteor[0].y > height:
            meteor_lst.remove(meteor)


def handle_upgrades():
    global score, bullets_fired, health

    for upgrade in upgrades:
        if upgrade[0].colliderect(flying_rocket_rect):
            upgrades.remove(upgrade)
            upgrade_sound.play()

            if upgrade[1] == 1:
                score += 2000

            else:
                bullets_fired = 0


def draw(bullets_remaining):
    window.blit(sky, (sky_rect_two.x, sky_rect_two.y))

    for background in space_backgrounds:
        window.blit(space, (background.x, background.y))

    flying_rocket_rect.x = pygame.mouse.get_pos()[0] - 15
    flying_rocket_rect.y = pygame.mouse.get_pos()[1] - 30

    window.blit(flying_rocket, (flying_rocket_rect.x - 3, flying_rocket_rect.y - 7))
    # pygame.draw.rect(window, (255, 0, 0), flying_rocket_rect)

    for meteor in meteor_lst:
        window.blit(pygame.transform.scale(meteor_pic, (meteor[1], meteor[2])), (meteor[0].x, meteor[0].y))
        # pygame.draw.rect(window, red, meteor[0])

    for upgrade in upgrades:
        window.blit(upgrade_dict[upgrade[1]], (upgrade[0].x, upgrade[0].y))

    for bullet in bullets:
        pygame.draw.rect(window, (255, 0, 0), bullet)

    txt_font = pygame.font.Font("C:\mmmahrous\Zeiad\Programming\Rocket game\Assets/ARCADECLASSIC.TTF", 30)
    score_txt = txt_font.render(f"SCORE  {score}", False, yellow)
    window.blit(score_txt, (10, 10))

    score_txt = txt_font.render(f"BULLETS  LEFT  {30 - bullets_remaining}", False, yellow)
    window.blit(score_txt, (width - 250, 10))


def game_over():
    global score, run

    def retry():
        global run, bullets_fired, score, click, space_backgrounds

        button_x, button_y, button_width, button_height = round(width/2 - 100), round(height/2 + 100), 200, 50
        button = pygame.rect.Rect(button_x, button_y, button_width, button_height)
        restart_font = pygame.font.Font("C:\mmmahrous\Zeiad\Programming\Rocket game\Assets/ARCADECLASSIC.TTF", 50)
        restart_txt = restart_font.render("RETRY", False, white)
        score_font = pygame.font.Font("C:\mmmahrous\Zeiad\Programming\Rocket game\Assets/ARCADECLASSIC.TTF", 80)
        score_text = score_font.render(f"SCORE  {score}", False, red)
        
        try_again = False
        while not try_again:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    try_again = True
                    run = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pos()[0] in range(button_x, button_x + button_width) and \
                            pygame.mouse.get_pos()[1] in range(button_y, button_y + button_height):
                        try_again = True
                        space_backgrounds.clear()
                        meteor_lst.clear()
                        bullets.clear()

                        ground_rect.x, ground_rect.y = 0, height - 100
                        sky_rect.x, sky_rect.x = 0, ground_rect.y - height
                        sky_rect_two.x, sky_rect_two.y = 0, sky_rect.y - height

                        bullets_fired = 0
                        score = 0
                        click = False
                        space_backgrounds = [pygame.rect.Rect(0, sky_rect_two.y - height, width, height)]

            window.blit(game_over_bg, (0, 0))
            window.blit(score_text, (width/3, height/5))
            pygame.draw.rect(window, green, button)
            window.blit(restart_txt, (button.x + 30, button.y))

            pygame.display.update()
                    
    txt_font = pygame.font.Font("C:\mmmahrous\Zeiad\Programming\Rocket game\Assets/ARCADECLASSIC.TTF", 100)
    go_txt = txt_font.render("GAME OVER", False, (255, 0, 0))

    txt_font = pygame.font.Font("C:\mmmahrous\Zeiad\Programming\Rocket game\Assets/ARCADECLASSIC.TTF", 60)
    score_txt = txt_font.render(f"SCORE  {score}", False, (255, 0, 0))

    window.blit(space, (0, 0))
    window.blit(explosion, (flying_rocket_rect.x, flying_rocket_rect.y))
    for meteor in meteor_lst:
        window.blit(pygame.transform.scale(meteor_pic, (meteor[1], meteor[2])), (meteor[0].x, meteor[0].y))

    window.blit(go_txt, (width/3 - 100, height/3))
    window.blit(score_txt, (width/3 - 50, height/2))

    pygame.display.update()

    # theme.stop()

    explosion_sound.play()

    time.sleep(4)

    retry()
    

def handle_bullets():
    global score

    for bullet in bullets:
        bullet.y -= bullet_vel
        for meteor in meteor_lst:
            if bullet.colliderect(meteor[0]):
                break_sound.play()
                try:
                    bullets.remove(bullet)
                    meteor_lst.remove(meteor)
                except ValueError:
                    pass
                score += 100

        if bullet.y <= 0:
            try:
                bullets.remove(bullet)
            except ValueError:
                continue


def main():
    global txt_rect, font, run, score, bullets_fired, background_vel, click

    while run:
        clock.tick(60)
        viable_x_coordinates = [i for i in range(5, width + 20)]
        for meteor in meteor_lst:
            for i in range(meteor[0].x - 40, meteor[0].x + 40):
                try:
                    viable_x_coordinates.remove(i)
                except ValueError:
                    continue
        if len(meteor_lst) < 11:
            size = random.choice(range(50, 100))
            meteor_lst.append((pygame.rect.Rect(
                random.choice(viable_x_coordinates), random.randint(flying_rocket_rect.y - width - 100, 10), size, size)
                    , size, size))

        end = time.time()
        if round(end - start) in multiples:
            multiples.remove(round(end-start))
            upgrades.append((pygame.rect.Rect(random.randint(30, width - 100),
                                              flying_rocket_rect.y - height * 2, 75, 75), random.randint(1, 2)))

        space_backgrounds.append(pygame.rect.Rect(0, space_backgrounds[-1].y - height, width, height))

        while not click:
            start_screen()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    click = True

                if event.type == pygame.MOUSEBUTTONUP:
                    click = True
                    # theme.play(10)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if len(bullets) < bullet_capacity and bullets_fired < 30:
                    if sky_rect_two.y >= 0:
                        laser.play()

                        bullets.append(pygame.rect.Rect(
                            flying_rocket_rect.x + flying_rocket_rect.width / 2, flying_rocket_rect.y - bullet_height,
                            bullet_wid, bullet_height))
                        bullets_fired += 1

        for background in space_backgrounds:
            background.y += background_vel

        for upgrade in upgrades:
            upgrade[0].y += background_vel

        if (sky_rect.y < 0 or sky_rect.y > -1) and sky_rect_two.y < -1:
            sky_rect_two.y += background_vel
            sky_rect.y += background_vel
            ground_rect.y += background_vel
            txt_rect.y += background_vel

            takeoff()
            continue

        if sky_rect_two.y < height:
            sky_rect_two.y += background_vel

        handle_upgrades()

        handle_bullets()

        draw(bullets_fired)

        mouse_on_screen = True

        while mouse_on_screen:
            if pygame.mouse.get_focused() == 0:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                        break

                font = pygame.font.Font("C:\mmmahrous\Zeiad\Programming\Rocket game\Assets/ARCADECLASSIC.TTF", 100)
                pause = font.render("PAUSED", False, red)
                window.blit(pause, (width/2 - 150, height/2 - 130))
                pygame.display.update()

            else:
                mouse_on_screen = False
        score += 1

        meteor_handling()

        pygame.display.update()

main()
