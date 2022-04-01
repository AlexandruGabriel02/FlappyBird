import pygame
import sys
import random

pygame.init()

WIDTH = 288
HEIGHT = 512
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

clock = pygame.time.Clock()

bg = pygame.image.load("sprites/background-day.png")
base = pygame.image.load("sprites/base.png")

class Player():
    def __init__(self, posX, posY, width, height, velocity):
        self.posX = posX
        self.posY = posY
        self.width = width
        self.height = height
        self.jump_vel = velocity
        self.curr_vel = 0
        self.g = 1
        self.started = False
        self.textures = [pygame.image.load("sprites/yellowbird-midflap.png"),
                         pygame.image.load("sprites/yellowbird-upflap.png"),
                         pygame.image.load("sprites/yellowbird-downflap.png")]
        self.index = 0
        self.score = 0
        self.highscore = 0

    def draw(self):
        texture = self.textures[self.index // 3]
        if self.curr_vel >= 0:
            texture = pygame.transform.rotate(texture, 15)
        else:
            texture = pygame.transform.rotate(texture, -15)
        window.blit(texture, (self.posX - self.width // 2, self.posY - self.height // 2))

    def jump(self):
        self.started = True
        self.curr_vel = self.jump_vel

    def update(self, pipes):
        global g
        self.posY += (-1 * self.curr_vel)

        if self.curr_vel <= -self.jump_vel:
            self.curr_vel = -self.jump_vel
        else:
            self.curr_vel = self.curr_vel - self.g

        for pipe in pipes:
            if bird.posX > pipe.posX and pipe.can_score:
                self.score += 1
                pipe.can_score = False
                score_sound = pygame.mixer.Sound("audio/point.wav")
                pygame.mixer.Sound.play(score_sound)

        self.index = (self.index + 1) % 9

class Pipe():
    def __init__(self, posX, posY, gap):
        self.posX = posX
        self.posY = posY
        self.gap = gap
        self.vel = 2
        self.texture = pygame.image.load("sprites/pipe-green.png")
        self.width = self.texture.get_width()
        self.can_score = True
    def draw(self):
        reversedText = pygame.transform.rotate(self.texture, 180)
        window.blit(reversedText, (self.posX, self.posY - reversedText.get_height()))
        window.blit(self.texture, (self.posX, self.posY + self.gap))

    def update(self):
        self.posX -= self.vel
        if self.posX + self.texture.get_width() <= 0:
            self.posX += 600
            self.can_score = True
            self.posY = random.randint(50, HEIGHT - 130 - base.get_height())

class Font():
    def __init__(self):
        self.digits = [pygame.image.load(f"sprites/{i}.png") for i in range(10)]
        self.width = [self.digits[i].get_width() for i in range(10)]
        self.height = [self.digits[i].get_height() for i in range(10)]

    def render(self, number, position):
        digit_count = len(str(number))
        digit_list = list(int(digit) for digit in str(number))
        (posX, posY) = position

        for digit in digit_list:
            window.blit(self.digits[digit], (posX, posY))
            posX += self.width[digit]

class Button():
    def __init__(self, texture, position):
        self.texture = texture
        self.width = self.texture.get_width()
        self.height = self.texture.get_height()
        self.position = position
    def draw(self):
        window.blit(self.texture, self.position)
    def canClick(self):
        (mousePosX, mousePosY) = pygame.mouse.get_pos()
        if mousePosX <= self.position[0] + self.width and mousePosX >= self.position[0]:
            if mousePosY <= self.position[1] + self.height and mousePosY >= self.position[1]:
                return True
        return False


bird = Player(WIDTH // 2 - 30, HEIGHT // 2 - 50, 34, 24, 11)
custom_font = Font()
pipes = [Pipe(WIDTH, random.randint(50, HEIGHT - 130 - base.get_height()), 130)]
pipes.append((Pipe(WIDTH + 200, random.randint(50, HEIGHT - 130 - base.get_height()), 130)))
pipes.append((Pipe(WIDTH + 400, random.randint(50, HEIGHT - 130 - base.get_height()), 130)))
baseX = 0

def display():
    global bird, bg, base, baseX, pipe, font

    window.blit(bg, (0, 0))

    if bird.started:
        bird.update(pipes)
        for pipe in pipes:
            pipe.update()
    else:
        message = pygame.image.load("sprites/message.png")
        window.blit(message, (WIDTH // 2 - message.get_width() // 2, HEIGHT // 2 - message.get_height() // 2))

    for pipe in pipes:
        pipe.draw()

    digit_count = len(str(bird.score))
    length = 0
    for digit in list(int(dig) for dig in str(bird.score)):
        length += custom_font.width[digit]
    posX = WIDTH // 2 - length // 2
    posY = 50
    custom_font.render(bird.score, (posX, posY))

    window.blit(base, (baseX, HEIGHT - base.get_height() // 2))
    baseX -= 2
    if baseX == -(base.get_width() - WIDTH):
        baseX = 0

    if bird.started:
        bird.draw()

    pygame.display.update()

def gameOver():
    offset = 13
    if bird.posY + bird.height >= HEIGHT - base.get_height() // 2 + offset:
        return True
    for pipe in pipes:
        if bird.posX + bird.width - (offset + 6) >= pipe.posX and bird.posX <= pipe.posX + pipe.width:
            if bird.posY + bird.height - (offset - 5) >= pipe.posY + pipe.gap or bird.posY - (offset - 4) <= pipe.posY:
                return True
    return False

def main_loop():
    global bird
    isRunning = True
    while isRunning:
        clock.tick(60)
        #pygame.time.delay(15)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                bird.jump()
                flap_sound = pygame.mixer.Sound("audio/wing.wav")
                pygame.mixer.Sound.play(flap_sound)


        display()

        if gameOver():
            isRunning = False
            hit_sound = pygame.mixer.Sound("audio/hit.wav")
            pygame.mixer.Sound.play(hit_sound)
            bird.highscore = max(bird.score, bird.highscore)

    pygame.time.wait(1500)

    pygame.mixer.Sound.play(pygame.mixer.Sound("audio/swoosh.wav"))
    isRunning = True
    while isRunning:

        message = pygame.image.load("sprites/gameover.png")
        restartTexture = pygame.image.load("sprites/restart.png")
        restart = Button(restartTexture, (WIDTH // 2 - restartTexture.get_width() // 2, HEIGHT // 2 + message.get_height() // 2 + 25))
        window.blit(message, (WIDTH // 2 - message.get_width() // 2, HEIGHT // 2 - message.get_height() // 2))
        restart.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart.canClick():
                    return

        pygame.display.update()

def reset():
    global bird, pipes
    bird.posX = WIDTH // 2 - 30
    bird.posY = HEIGHT // 2 - 50
    bird.curr_vel = 0
    bird.started = False
    bird.index = 0
    bird.score = 0

    pipes.clear()
    pipes = [Pipe(WIDTH, random.randint(50, HEIGHT - 130 - base.get_height()), 130)]
    pipes.append((Pipe(WIDTH + 200, random.randint(50, HEIGHT - 130 - base.get_height()), 130)))
    pipes.append((Pipe(WIDTH + 400, random.randint(50, HEIGHT - 130 - base.get_height()), 130)))

def main():
    isRunning = True
    while isRunning:
        main_loop()
        reset()


main()
