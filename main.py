import pygame
import random
import copy

pygame.init()

words_eng = open('eng_words.txt', encoding='utf-8').read()
wordlist_eng = words_eng.lower().split('\n')
len_index = []
length = 1

wordlist_eng.sort(key=len)
for i in range(len(wordlist_eng)):
    if len(wordlist_eng[i]) > length:
        length += 1
        len_index.append(i)
len_index.append(len(wordlist_eng))

WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Клавиатурные бега')
# icon = pygame.image.load('assets/images/icon.png')
# pygame.display.set_icon(icon)
surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
timer = pygame.time.Clock()
fps = 60
level = 1
active_string = ''
score = 0
lives = 5
paused = True
submit = ''
word_objects = []
eng_letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
               'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
new_level = True
choices = [False, True, False, False, False, False, False]

header_font = pygame.font.Font('assets/fonts/PressStart2P.ttf', 25)
pause_font = pygame.font.Font('assets/fonts/1up.ttf', 38)
banner_font = pygame.font.Font('assets/fonts/DotGothic16.ttf', 28)
string_font = pygame.font.Font('assets/fonts/PressStart2P.ttf', 44)
label_font = pygame.font.Font('assets/fonts/PressStart2P.ttf', 35)
font = pygame.font.Font('assets/fonts/PressStart2P.ttf', 44)

pygame.mixer.init()
pygame.mixer.music.load('assets/music/29 Palms.mp3')
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1)
click = pygame.mixer.Sound('assets/music/click.mp3')
correct = pygame.mixer.Sound('assets/music/correct.mp3')
wrong = pygame.mixer.Sound('assets/music/vine-boom.mp3')
lose = pygame.mixer.Sound('assets/music/the-sims-3-pc-broken-object-music.mp3')
lives_less = pygame.mixer.Sound('assets/music/stationary-kill_gDwMUvN.mp3')
click.set_volume(0.3)
correct.set_volume(0.2)
wrong.set_volume(0.3)
lose.set_volume(0.5)
lives_less.set_volume(0.5)

file = open('high_score.txt', 'r')
read = file.readlines()
high_score = int(read[0])
file.close()


class Word:
    def __init__(self, text, speed, x_pos, y_pos):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.text = text
        self.speed = speed

    def draw(self):
        screen.blit(font.render(self.text, True, '#39608c'), (self.x_pos, self.y_pos))
        act_len = len(active_string)
        if active_string == self.text[:act_len]:
            screen.blit(font.render(active_string, True, '#5aadd1'), (self.x_pos, self.y_pos))

    def update(self):
        self.x_pos -= self.speed


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

    screen.blit(header_font.render(f'УРОВЕНЬ:{level}', True, 'white'), (10, HEIGHT - 60))
    screen.blit(string_font.render(f'"{active_string}"', True, 'white'), (258, HEIGHT - 70))
    pause_btn = Button(748, HEIGHT - 52, 'II', False, screen)
    pause_btn.draw()
    screen.blit(banner_font.render(f'Счёт: {score}', True, '#39608c'), (270, 10))
    screen.blit(banner_font.render(f'Рекорд: {high_score}', True, '#39608c'), (500, 10))
    screen.blit(banner_font.render(f'Жизни: {lives}', True, '#39608c'), (10, 10))
    return pause_btn.clicked


def draw_pause():
    choice_commits = copy.deepcopy(choices)
    surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    pygame.draw.rect(surface, '#afbfd1', [100, 100, 600, 300], 0, 5)
    pygame.draw.rect(surface, '#607fa3', [100, 100, 600, 300], 5, 5)
    resume_btn = Button(160, 200, 'A', False, surface)
    resume_btn.draw()
    quit_btn = Button(450, 200, 'X', False, surface)
    quit_btn.draw()

    surface.blit(label_font.render('МЕНЮ', True, 'white'), (115, 115))
    surface.blit(label_font.render('СТАРТ!', True, 'white'), (205, 190))
    surface.blit(label_font.render('ВЫХОД', True, 'white'), (492, 190))
    surface.blit(label_font.render('Длина слов:', True, 'white'), (110, 250))

    for i in range(len(choices)):
        btn = Button(160 + (i * 80), 350, str(i + 2), False, surface)
        btn.draw()
        if btn.clicked:
            if choice_commits[i]:
                choice_commits[i] = False
            else:
                choice_commits[i] = True
        if choices[i]:
            pygame.draw.circle(surface, '#5aadd1', (160 + (i * 80), 350), 35, 5)

    screen.blit(surface, (0, 0))
    return resume_btn.clicked, choice_commits, quit_btn.clicked


def check_answer(scor):
    for wrd in word_objects:
        if wrd.text == submit:
            points = wrd.speed * len(wrd.text) * 10 * (len(wrd.text) / 3)
            scor += int(points)
            word_objects.remove(wrd)
            correct.play()
    return scor


def generate_level():
    word_objs = []
    include = []
    vertical_spacing = (HEIGHT - 150) // level
    if True not in choices:
        choices[0] = True
    for i in range(len(choices)):
        if choices[i]:
            include.append((len_index[i], len_index[i + 1]))
    for i in range(level):
        speed = random.randint(2, 3)
        y_pos = random.randint(50 + (i * vertical_spacing), (i + 1) * vertical_spacing)
        x_pos = random.randint(WIDTH, WIDTH + 1000)
        ind_sel = random.choice(include)
        index = random.randint(ind_sel[0], ind_sel[1])
        text = wordlist_eng[index].lower()
        new_word = Word(text, speed, x_pos, y_pos)
        word_objs.append(new_word)

    return word_objs


def check_high_score():
    global high_score
    if score > high_score:
        high_score = score
        file = open('high_score.txt', 'w')
        file.write(str(int(high_score)))
        file.close()


running = True
while running:
    screen.fill('#d7e5ee')
    timer.tick(fps)
    pause_butt = draw_screen()
    if paused:
        resume_butt, changes, quit_butt = draw_pause()
        if resume_butt:
            paused = False
        if quit_butt:
            check_high_score()
            running = False
    if new_level and not paused:
        word_objects = generate_level()
        new_level = False
    else:
        for w in word_objects:
            w.draw()
            if not paused:
                w.update()
            if w.x_pos < -200:
                word_objects.remove(w)
                lives -= 1
                score -= 20
                lives_less.play()
    if len(word_objects) <= 0 and not paused:
        level += 1
        new_level = True

    if submit != '':
        init = score
        score = check_answer(score)
        submit = ''
        if init == score:
            wrong.play()
            pass

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            check_high_score()
            running = False

        if event.type == pygame.KEYDOWN:
            if not paused:
                if event.unicode.lower() in eng_letters and len(active_string) <= 8:
                    active_string += event.unicode.lower()
                    click.play()
                if event.key == pygame.K_BACKSPACE and len(active_string) > 0:
                    active_string = active_string[:-1]
                    click.play()
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    submit = active_string
                    active_string = ''
            if event.key == pygame.K_ESCAPE:
                if paused:
                    paused = False
                else:
                    paused = True

        if event.type == pygame.MOUSEBUTTONUP and paused:
            if event.button == 1:
                choices = changes

    if pause_butt:
        paused = True

    if lives < 0:
        lose.play()
        paused = True
        level = 1
        lives = 5
        word_objects = []
        new_level = True
        check_high_score()
        score = 0

    pygame.display.flip()
pygame.quit()
