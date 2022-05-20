import pygame
from pygame.locals import *
import random
from network import Network


pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 864
screen_height = 936

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Flappy Bird')

#define font
font = pygame.font.SysFont('Bauhaus 93', 60)

#define colours
white = (255, 255, 255)

#define game variables
ground_scroll = 0
scroll_speed = 4
flying = False
game_over = False
pipe_gap = 250
pipe_frequency = 1500 #milliseconds
last_pipe = pygame.time.get_ticks() - pipe_frequency
score = 0
pass_pipe = False


#load images
bg = pygame.image.load('bg.png')
ground_img = pygame.image.load('ground.png')
button_img = pygame.image.load('restart.png')


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def reset_game():
    pipe_group.empty()
    flappy.rect.x = 100
    flappy.rect.y = int(screen_height / 2)
    score = 0
    return score



class Bird(pygame.sprite.Sprite):
    def __init__(self, jugador, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        self.jugador = jugador
        for num in range(1, 4):
            img = pygame.image.load(f'bird{num}.png')
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 0
        self.clicked = False

    def update(self):

        if flying == True:
            #gravity
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8
            if self.rect.bottom < 768:
                self.rect.y += int(self.vel)

        if game_over == False:
            #jump
            if pygame.mouse.get_pressed()[self.jugador] == 1 and self.clicked == False:
                self.clicked = True
                self.vel = -10
            if pygame.mouse.get_pressed()[self.jugador] == 0:
                self.clicked = False

            #handle the animation
            self.counter += 1
            flap_cooldown = 5

            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index]

            #rotate the bird
            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)



class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('pipe.png')
        self.rect = self.image.get_rect()
        #position 1 is from the top, -1 is from the bottom
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(pipe_gap / 2)]
        if position == -1:
            self.rect.topleft = [x, y + int(pipe_gap / 2)]

    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill()


class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):

        action = False

        #get mouse position
        pos = pygame.mouse.get_pos()

        #check if mouse is over the button
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True

        #draw button
        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action
    
class Game:

    def __init__(self, w, h):
        self.net = Network()
        self.width = w
        self.height = h
        self.flappy = Bird(0,100, int(screen_height / 2))
        self.flappy22 = Bird(2,200, int(screen_height / 2))
        self.canvas = Canvas(self.width, self.height, "Testing...")
        self.clock = pygame.time.Clock()
        self.fps = 60
        
        self.screen_width = 864
        self.screen_height = 936
        
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.pygame.display.set_caption('Flappy Bird')
        
        #define font
        self.font = pygame.font.SysFont('Bauhaus 93', 60)
        
        #define colours
        self.white = (255, 255, 255)
        
        #define game variables
        self.ground_scroll = 0
        self.scroll_speed = 4
        self.flying = False
        self.game_over = False
        self.pipe_gap = 250
        self.pipe_frequency = 1500 #milliseconds
        self.last_pipe = pygame.time.get_ticks() - pipe_frequency
        self.score = 0
        self.pass_pipe = False


    def run(self):
        
        bird_group = pygame.sprite.Group()
        pipe_group = pygame.sprite.Group()
        
        bird_group.add(self.flappy)
        bird_group.add(flappy2)
        
        run = True
        while run:
        
            clock.tick(fps)
        
            #draw background
            screen.blit(bg, (0,0))
        
            bird_group.draw(screen)
            bird_group.update()
            pipe_group.draw(screen)
        
            #draw the ground
            screen.blit(ground_img, (ground_scroll, 768))
        
            #check the score
            if len(pipe_group) > 0:
                if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left\
                    and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right\
                    and self.pass_pipe == False:
                    pass_pipe = True
                if pass_pipe == True:
                    if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                        self.score += 1
                        pass_pipe = False
        
        
            draw_text(str(self.score), font, white, int(screen_width / 2), 20)
        
            #look for collision
            if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
                game_over = True
        
            #check if bird has hit the ground
            if flappy.rect.bottom >= 768:
                game_over = True
                flying = False
        
        
            if game_over == False and flying == True:
        
                #generate new pipes
                time_now = pygame.time.get_ticks()
                if time_now - self.last_pipe > pipe_frequency:
                    pipe_height = random.randint(-100, 100)
                    btm_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, -1)
                    top_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, 1)
                    pipe_group.add(btm_pipe)
                    pipe_group.add(top_pipe)
                    self.last_pipe = time_now
        
        
                #draw and scroll the ground
                self.ground_scroll -= scroll_speed
                if abs(self.ground_scroll) > 35:
                    self.ground_scroll = 0
        
                pipe_group.update()
        
        
            #check for game over and reset
            if game_over == True:
                if button.draw() == True:
                    game_over = False
                    self.score = reset_game()
        
        
        
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
                    flying = True
        
            pygame.display.update()
        
        pygame.quit()

        

    def send_data(self):
        """
        Send position to server
        :return: None
        """
        data = str(self.net.id) + ":" + str(self.player.x) + "," + str(self.player.y)
        reply = self.net.send(data)
        return reply

    @staticmethod
    def parse_data(data):
        try:
            d = data.split(":")[1].split(",")
            return int(d[0]), int(d[1])
        except:
            return 0,0

    
    







class Canvas:

    def __init__(self, w, h, name="None"):
        self.width = w
        self.height = h
        self.screen = pygame.display.set_mode((w,h))
        pygame.display.set_caption('Flappy Bird')
        self.font = pygame.font.SysFont('Bauhaus 93', 60)
        self.white = (255, 255, 255)
    
        #define game variables
        self.ground_scroll = 0
        self.scroll_speed = 4
        self.flying = False
        self.game_over = False
        self.pipe_gap = 250
        self.pipe_frequency = 1500 #milliseconds
        self.last_pipe = pygame.time.get_ticks() - pipe_frequency
        self.score = 0
        self.pass_pipe = False
        
         #load images
        self.bg = pygame.image.load('bg.png')
        self.ground_img = pygame.image.load('ground.png')
        self.button_img = pygame.image.load('restart.png')


    def draw_text(text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        screen.blit(img, (x, y))
    
    def reset_game():
        pipe_group.empty()
        flappy.rect.x = 100
        flappy.rect.y = int(screen_height / 2)
        score = 0
        return score
   

    @staticmethod
    def update():
        pygame.display.update()

    def draw_text2(self, text, size, x, y):
        pygame.font.init()
        font = pygame.font.SysFont("comicsans", size)
        render = font.render(text, 1, (0,0,0))

        self.screen.draw(render, (x,y))

    def get_canvas(self):
        return self.screen

    def draw_background(self):
        self.screen.fill((255,255,255))


    
    pygame.init()
    
    clock = pygame.time.Clock()
    fps = 60
    
    screen_width = 864
    screen_height = 936
    
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Flappy Bird')
    
    #define font
    font = pygame.font.SysFont('Bauhaus 93', 60)
    
    #define colours
    white = (255, 255, 255)
    
    #define game variables
    ground_scroll = 0
    scroll_speed = 4
    flying = False
    game_over = False
    pipe_gap = 250
    pipe_frequency = 1500 #milliseconds
    last_pipe = pygame.time.get_ticks() - pipe_frequency
    score = 0
    pass_pipe = False
    
    
    #load images
    bg = pygame.image.load('bg.png')
    ground_img = pygame.image.load('ground.png')
    button_img = pygame.image.load('restart.png')
    
    
    def draw_text3(text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        screen.blit(img, (x, y))
    
    
    def reset_game2():
        pipe_group.empty()
        flappy.rect.x = 100
        flappy.rect.y = int(screen_height / 2)
        score = 0
        return score


















bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

flappy = Bird(0,100, int(screen_height / 2))
flappy2 = Bird(2,200, int(screen_height / 2))

bird_group.add(flappy)
bird_group.add(flappy2)

#create restart button instance
button = Button(screen_width // 2 - 50, screen_height // 2 - 100, button_img)

run = True
while run:

    clock.tick(fps)

    #draw background
    screen.blit(bg, (0,0))

    bird_group.draw(screen)
    bird_group.update()
    pipe_group.draw(screen)

    #draw the ground
    screen.blit(ground_img, (ground_scroll, 768))

    #check the score
    if len(pipe_group) > 0:
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left\
            and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right\
            and pass_pipe == False:
            pass_pipe = True
        if pass_pipe == True:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score += 1
                pass_pipe = False


    draw_text(str(score), font, white, int(screen_width / 2), 20)

    #look for collision
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
        game_over = True

    #check if bird has hit the ground
    if flappy.rect.bottom >= 768:
        game_over = True
        flying = False


    if game_over == False and flying == True:

        #generate new pipes
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:
            pipe_height = random.randint(-100, 100)
            btm_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, -1)
            top_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, 1)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            last_pipe = time_now


        #draw and scroll the ground
        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 35:
            ground_scroll = 0

        pipe_group.update()


    #check for game over and reset
    if game_over == True:
        if button.draw() == True:
            game_over = False
            score = reset_game()



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
            flying = True

    pygame.display.update()

pygame.quit()

        
