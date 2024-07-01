# بسم الله الرحمن الرحيم

import random
import pygame

pygame.font.init()

Height, Width = 600, 350
WIN = pygame.display.set_mode((Width, Height))
pygame.display.set_caption("Platformer")

clock = pygame.time.Clock()

WHITE = (255, 255, 255)
GREY = (79, 79, 79)

Character_dimensions = (33, 27)
Platform_dimensions = (32, 18)

CharacterRightImg = pygame.transform.scale(pygame.image.load("Platformer game\Assets\Char right.jpg"), (33, 27))
CharacterLeftImg = pygame.transform.scale(pygame.image.load("Platformer game\Assets\Char left.jpg"), (33, 27))
JmpCharacterImg = pygame.transform.scale(pygame.image.load("Platformer game\Assets\Jumping Char.jpg"), (33, 27))
PlatformImg = pygame.transform.scale(pygame.image.load("Platformer game\Assets\\Normal Platform.png"), Platform_dimensions)
MovingPlatformImg = pygame.transform.scale(pygame.image.load("Platformer game\Assets\Moving platform.png"), (35, 18))
SpikeImg = pygame.transform.scale(pygame.image.load("Platformer game\Assets\Spikes.jpg"), Platform_dimensions)
CloudImg = pygame.transform.scale(pygame.image.load("Platformer game\Assets\Cloud.jpg"), (32, 14))
WeakPlatformImg = pygame.transform.scale(pygame.image.load("Platformer game\Assets\Weak platform.png"), Platform_dimensions)
TrampolineImg = pygame.transform.scale(pygame.image.load("Platformer game\Assets\Trampoline.png"), (32, 22))
PropellerImg = pygame.image.load("Platformer game\Assets\Propeller.jpg")

Platforms = pygame.sprite.Group()

txt_font = pygame.font.SysFont("Platformer game\Assets\ARCADECLASSIC.TTF", 20)
Jmpvel = -13
next_platform = 550   # The y coordinate of the next platform to be spawned
last_spawned = -1   # Stores the last platform spwaned to ensure that the game is not impossible :)


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = PlatformImg
        self.rect = self.image.get_rect(center=(x, y))
        Platforms.add(self)
        self.vely = 0

    def collide(self, Character):
        Character.vel = Jmpvel
        
    def update(self):
        if self.rect.center[1] >= 600:
            Platforms.remove(self)
            spawn_platform()
            
        self.rect = self.rect.move(0, self.vely)

class MovingPlatform(Platform):
    def __init__(self, x, y,):
        Platform.__init__(self, x, y)
        self.image = MovingPlatformImg
        self.velx = random.choice((-2, -1, 1, 2))
    
    def update(self):
        self.rect = self.rect.move(self.velx, 0)
        if self.rect.right >= 300 or self.rect.left < 0:
            self.velx = -self.velx

        if self.rect.center[1] >= 600:
            Platforms.remove(self)
            spawn_platform()
                    
        self.rect = self.rect.move(0, self.vely)

class Cloud(Platform):
    def __init__(self, x, y):
            Platform.__init__(self, x, y)
            self.image = CloudImg
    def collide(self, Character):
        pass

class Spike(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image = SpikeImg
    def collide(self, character):
        character.alive = False

class WeakPlatform(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image = WeakPlatformImg
    
    def collide(self, Character):
        Character.vel = Jmpvel
        Platforms.remove(self)

class Trampoline(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image = TrampolineImg
    
    def collide(self, Character):
        Character.vel = Jmpvel * 1.5


class Character:
    def __init__(self):
        self.image = CharacterLeftImg
        self.vel = 0
        self.rect = self.image.get_rect(center=(175, 300))
        self.alive = True
        self.stagnant = False    # WHEN THIS IS TRUE, THE CAMERA IS GOING UP OR DOWN, SO THE CHAR MUST REMAIN IN ITS SAME POSITION ON THE SCREEN
        
    def update(self):
        # MOVEMENT
        self.vel += 0.25
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect = self.rect.move(-5, 0)
            self.image = CharacterLeftImg
            
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect = self.rect.move(5, 0)
            self.image = CharacterRightImg
        
        if self.rect.left > 350:
            self.rect.left = 0
        elif self.rect.right < 0:
            self.rect.right = 350
        
        # CHECKING COLLISION
        Platform_lst = Platforms.sprites()
        Index = self.rect.collidelist(Platform_lst)
        if Index != -1 and self.vel >= 0:
           Platform_lst[Index].collide(self)
        
    
    def draw(self):
        WIN.blit(self.image, self.rect)


def draw():
    WIN.fill(WHITE)
    
    Player.draw()
    Platforms.draw(WIN)
    
    pygame.display.update()
    

def spawn_platform():
    global next_platform, last_spawned
    
    next_spawn = last_spawned
    while abs(next_spawn - last_spawned) <= 1:
        next_spawn = random.randint(1, 11)
    
    last_spawned = next_spawn
    
    if 1 <= next_spawn <= 3 or next_platform > 100:
        Platforms.add(Platform(random.randint(30, 320), next_platform))
    elif next_spawn == 4 or next_spawn == 5: 
        Platforms.add(WeakPlatform(random.randint(30, 320), next_platform))
    elif next_spawn == 6 or next_spawn == 7:
        Platforms.add(Cloud(random.randint(30, 320), next_platform))
    elif next_spawn == 8 or next_spawn == 9:
        Platforms.add(MovingPlatform(random.randint(30, 320), next_platform))
    elif next_spawn == 10:
        Platforms.add(Spike(random.randint(30, 320), next_platform))
    elif next_spawn == 11:
        Platforms.add(Trampoline(random.randint(30, 320), next_platform))
    

    next_platform -= random.randint(70, 90)


def main():
    global Player

    run = True
    started = False
    Player = Character()
    start_txt = pygame.font.Font.render(txt_font, "PRESS ANY BUTTON TO START", False, GREY)
    for _ in range(50):
        spawn_platform()

    while run:
        clock.tick(60)
        
        draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                started = True

        if not started:
            WIN.blit(start_txt, (start_txt.get_rect(center=(175, 50))))
            pygame.display.update()
            continue
        
        for plat in Platforms:
            plat.vely = -Player.vel
            if -Player.rect.top + plat.rect.top > 1000:
                run = False
        
        if not Player.alive:
            run = False
        
        Platforms.update()
        Player.update()
        

main()        
