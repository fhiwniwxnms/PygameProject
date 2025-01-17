import pygame
import random
import copy

pygame.init()

from nltk.corpus import words

wordlist = words.words()
len_index = []
length = 1

wordlist.sort(key=len)
for i in range(len(wordlist)):
    if len(wordlist[i]) > length:
        length += 1
        len_index.append(i)
len_index.append(len(wordlist))
print(len_index)

WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Клавиатурные бега')
icon = pygame.image.load('images/icon.png')
pygame.display.set_icon(icon)
surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
timer = pygame.time.Clock()
fps = 60
level = 0
active_string = '12345678'
score = 0
high_score = 1
lives = 5
paused = False
submit = ''
word_objects = []
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
           'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

header_font = pygame.font.Font('fonts/PressStart2P.ttf', 23)
pause_font = pygame.font.Font('fonts/1up.ttf', 38)
banner_font = pygame.font.Font('fonts/DotGothic16.ttf', 28)
string_font = pygame.font.Font('fonts/PressStart2P.ttf', 44)


class Button:
    def __init__(self, x_pos, y_pos, text, clicked, surf):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.text = text
        self.clicked = clicked
        self.surf = surf

    def draw(self):
        cir = pygame.draw.circle(self.surf, (45, 89, 135), (self.x_pos, self.y_pos), 35)
        if cir.collidepoint(pygame.mouse.get_pos()):
            butts = pygame.mouse.get_pressed()
            if butts[0]:
                pygame.draw.circle(self.surf, '#223954', (self.x_pos, self.y_pos), 35)
                self.clicked = True
            else:
                pygame.draw.circle(self.surf, '#2d4c70', (self.x_pos, self.y_pos), 35)
        pygame.draw.circle(self.surf, 'white', (self.x_pos, self.y_pos), 35, 3)
        self.surf.blit(pause_font.render(self.text, True, 'white'), (self.x_pos - 16, self.y_pos - 28))


def draw_screen():
    pygame.draw.rect(screen, '#39608c', [0, HEIGHT - 100, WIDTH, 100])
    pygame.draw.rect(screen, 'white', [0, 0, WIDTH, HEIGHT], 5)
    pygame.draw.line(screen, 'white', (250, HEIGHT - 100), (250, HEIGHT), 2)
    pygame.draw.line(screen, 'white', (700, HEIGHT - 100), (700, HEIGHT), 2)
    pygame.draw.line(screen, 'white', (0, HEIGHT - 100), (WIDTH, HEIGHT - 100), 2)
    pygame.draw.rect(screen, 'black', [0, 0, WIDTH, HEIGHT], 1)

    screen.blit(header_font.render(f'УРОВЕНЬ: {level}', True, 'white'), (10, HEIGHT - 60))
    screen.blit(string_font.render(f'"{active_string}"', True, 'white'), (258, HEIGHT - 70))
    pause_btn = Button(748, HEIGHT - 52, 'II', False, screen)
    pause_btn.draw()
    screen.blit(banner_font.render(f'Счёт: {score}', True, '#39608c'), (250, 10))
    screen.blit(banner_font.render(f'Рекорд: {high_score}', True, '#39608c'), (500, 10))
    screen.blit(banner_font.render(f'Жизни: {lives}', True, '#39608c'), (10, 10))
    return pause_btn.clicked


def draw_pause():
    pass


def generate_level():
    word_objs = []

    return word_objs


running = True
while running:
    screen.fill('#d7e5ee')
    timer.tick(fps)
    pause_butt = draw_screen()
    if paused:
        draw_pause()
    elif new_level:
        word_objects = generate_level()
        new_level = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if not paused:
                if event.unicode.lower() in letters:
                    active_string += event.unicode.lower()
                if event.key == pygame.K_BACKSPACE and len(active_string) > 0:
                    active_string = active_string[:-1]
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    submit = active_string
                    active_string = ''

    pygame.display.flip()
pygame.quit()
