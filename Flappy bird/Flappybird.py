import pygame
import random

WIN_WIDTH = 600
WIN_HEIGHT = 630

WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

clock = pygame.time.Clock()

BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load("C:\mmmahrous\Zeiad\Programming\Flappy bird\Assets/bird1.png")), pygame.transform.scale2x(pygame.image.load("C:\mmmahrous\Zeiad\Programming\Flappy bird\Assets/bird2.png")), pygame.transform.scale2x(pygame.image.load("C:\mmmahrous\Zeiad\Programming\Flappy bird\Assets/bird3.png"))]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load("C:\mmmahrous\Zeiad\Programming\Flappy bird\Assets\pipe.png"))
BASE_IMG = pygame.transform.scale2x(pygame.image.load("C:\mmmahrous\Zeiad\Programming\Flappy bird\Assets/base.png"))
BG_IMG = pygame.transform.scale(pygame.image.load("C:\mmmahrous\Zeiad\Programming\Flappy bird\Assets/bg.png"), (WIN_WIDTH, WIN_HEIGHT))

class Bird:
    IMGS = BIRD_IMGS
    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 2

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0   # The tilt of the bird
        self.tick_count = 0   # Number of frames that have passed since last jump
        self.vel = 0   # Current velocity
        self.height = self.y   # The pos that I last jumped at
        self.img_count = 0  
        self.img = self.IMGS[0]   # The state of the bird (Wing up, wing down or wing straight)
    
    def jump(self):

        self.vel = -10
        self.tick_count = 0
        self.height = self.y
    
    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.jump()

        self.tick_count += 1

        d = self.vel * self.tick_count + 1.5 * self.tick_count ** 2

        if d >= 16:
            d = 16
        elif d < 0:
            d -= 2

        self.y = self.y + d

        if d < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL

    def draw(self, win):
        self.img_count += 1
        if self.img_count < self.ANIMATION_TIME:  # Animating the bird flaps
            self.img = self.IMGS[0]
        
        elif self.img_count < self.ANIMATION_TIME * 2:
            self.img = self.IMGS[1]

        elif self.img_count < self.ANIMATION_TIME * 3:
            self.img = self.IMGS[2]
        
        elif self.img_count < self.ANIMATION_TIME * 4:
            self.img = self.IMGS[1]
        
        elif self.img_count < self.ANIMATION_TIME * 4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0

        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME * 2

        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center)   # Rotating an img around its center
        win.blit(rotated_image, new_rect.topleft)
    
    def get_mask(self):
        return pygame.mask.from_surface(self.img)


class Pipe:
    GAP = 200
    VEL = 5

    def __init__(self, x):
        self.x = x
        self.height = 0
        self.gap = 100

        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True)
        self.PIPE_BOTTOM = PIPE_IMG

        self.passed = False

        self.set_height()
    
    def set_height(self):
        self.height = random.randrange(50, 350)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        self.x -= self.VEL

    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)

        if t_point or b_point:
            return True
        
        return False


class Base:
    VEL = 5
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH
    
    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH
        
        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH
    
    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y))

        win.blit(self.IMG, (self.x2, self.y))


def draw_window(win, bird, pipes, base):
    win.blit(BG_IMG, (0, 0))
    
    for pipe in pipes:
        pipe.draw(win)
    base.draw(win)

    bird.draw(win)

    pygame.display.update()


def main():
    bird = Bird(100, 300)
    base = Base(550)
    pipes = [Pipe(600)]

    score = 0

    run = True
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        bird.move()
        base.move()

        rem = []
        add_pipe = False
        for pipe in pipes:
            if pipe.collide(bird):
                pass

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)
            
            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True
    
            pipe.move()

        for r in rem:
            pipes.remove(r)

        if add_pipe:
            score += 1
            pipes.append(Pipe(600))

        for pipe in pipes:
            if pipe.collide(bird):
                run = False
        
        if bird.y + 50 >= 550:
            run = False

        draw_window(WIN, bird, pipes, base)


main()
pygame.quit()