import pygame
import random
import copy
# Импортируем нужные библиотеки

pygame.init()  # Инициализируем Pygame

# Загружаем английские и русские слова из текстовых файлов
words_eng = open('assets/files/eng_words.txt', encoding='utf-8').read()
words_rus = open('assets/files/rus_words.txt', encoding='utf-8').read()

WIDTH = 800
HEIGHT = 600  # Устанавливаем размеры окна игры
screen = pygame.display.set_mode([WIDTH, HEIGHT])  # Создаем окно заданных размеров
pygame.display.set_caption('Клавиатурные бега')  # Устанавливаем заголовок окна
surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)  # Создаем поверхность для отрисовки
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
rus_letters = ['а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'и', 'к', 'л', 'м', 'н', 'о', 'п',
               'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я']
new_level = True
choices = [False, True, False, False, False, False, False]
language = [False, True]
speed = [True, False, False]
# Устанавливаем необходимые значения по умолчанию,
# а также создаем список из русского и английского алфавита

header_font = pygame.font.Font('assets/fonts/PressStart2P.ttf', 25)
level_font = pygame.font.Font('assets/fonts/PressStart2P.ttf', 17)
pause_font = pygame.font.Font('assets/fonts/1up.ttf', 38)
banner_font = pygame.font.Font('assets/fonts/DotGothic16.ttf', 28)
string_font = pygame.font.Font('assets/fonts/PressStart2P.ttf', 44)
label_font = pygame.font.Font('assets/fonts/PressStart2P.ttf', 35)
font = pygame.font.Font('assets/fonts/PressStart2P.ttf', 44)
# Задаем шрифты для отображения текста на экране

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
# Задаем музыку для проигрывания во время игры

file = open('assets/files/high_score.txt', 'r')
read = file.readlines()
high_score = int(read[0])
file.close()
# Берем значение рекордного счета из файла


# Класс для прорисовки слов на экране
class Word:
    def __init__(self, text, sp, x_pos, y_pos):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.text = text
        self.speed = sp

    def draw(self):
        screen.blit(font.render(self.text, True, '#39608c'), (self.x_pos, self.y_pos))
        act_len = len(active_string)
        if active_string == self.text[:act_len]:
            screen.blit(font.render(active_string, True, '#5aadd1'), (self.x_pos, self.y_pos))

    def update(self):
        self.x_pos -= self.speed


# Класс для прорисовки кнопок на экране
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


# Класс для прорисовки основного экрана игры
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


# Класс для прорисовки экрана паузы
def draw_pause():
    choice_commits = copy.deepcopy(choices)
    language_commits = copy.deepcopy(language)
    speed_commits = copy.deepcopy(speed)
    surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    pygame.draw.rect(surface, '#afbfd1', [50, 100, 700, 375], 0, 5)
    pygame.draw.rect(surface, '#607fa3', [50, 100, 700, 375], 5, 5)
    resume_btn = Button(110, 200, 'A', False, surface)
    resume_btn.draw()
    quit_btn = Button(400, 200, 'X', False, surface)
    quit_btn.draw()

    surface.blit(label_font.render('МЕНЮ', True, 'white'), (65, 115))
    surface.blit(header_font.render('Уровень', True, 'white'), (490, 115))
    surface.blit(header_font.render('сложности:', True, 'white'), (505, 145))
    surface.blit(label_font.render('СТАРТ!', True, 'white'), (155, 190))
    surface.blit(label_font.render('ВЫХОД', True, 'white'), (442, 190))
    surface.blit(label_font.render('Длина слов:', True, 'white'), (70, 250))
    surface.blit(header_font.render('Русс', True, 'white'), (230, 410))
    surface.blit(header_font.render('Англ', True, 'white'), (370, 410))
    surface.blit(level_font.render('Легко', True, 'white'), (645, 180))
    surface.blit(level_font.render('Средне', True, 'white'), (638, 270))
    surface.blit(level_font.render('Сложно', True, 'white'), (638, 360))

    # Кнопки выбора длин слов
    for i in range(len(choices)):
        btn = Button(110 + (i * 80), 330, str(i + 2), False, surface)
        btn.draw()
        if btn.clicked:
            if choice_commits[i]:
                choice_commits[i] = False
            else:
                choice_commits[i] = True
        if choices[i]:
            pygame.draw.circle(surface, '#5aadd1', (110 + (i * 80), 330), 35, 5)

    # Кнопки выбора языка
    butt_text = ['R', 'E']
    for i in range(len(language)):
        btn = Button(190 + (i * 320), 420, butt_text[i], False, surface)
        btn.draw()
        if btn.clicked:
            if language_commits[i]:
                language_commits[i] = False
            else:
                language_commits[i] = True
        if language[i]:
            pygame.draw.circle(surface, '#5aadd1', (190 + (i * 320), 420), 35, 5)

    # Кнопки выбора уровня сложности
    speed_text = ['L', 'M', 'H']
    for i in range(len(speed)):
        btn = Button(690, 235 + (i * 90), speed_text[i], False, surface)
        btn.draw()
        if btn.clicked:
            if speed_commits[i]:
                speed_commits[i] = False
            else:
                speed_commits[i] = True
        if speed[i]:
            pygame.draw.circle(surface, '#5aadd1', (690, 235 + (i * 90)), 35, 5)

    screen.blit(surface, (0, 0))
    return resume_btn.clicked, choice_commits, quit_btn.clicked, language_commits, speed_commits


#  Метод для проверки введенного пользователем ответа
def check_answer(scor):
    for wrd in word_objects:
        if wrd.text == submit:
            points = wrd.speed * len(wrd.text) * 10 * (len(wrd.text) / 3)
            scor += int(points)
            word_objects.remove(wrd)
            correct.play()
    return scor


# Метод для генерации уровня
def generate_level():
    word_objs = []
    include = []
    vertical_spacing = (HEIGHT - 150) // level
    len_index = []
    length = 1
    test = ()

    if language[0]:
        wordlist = words_rus.lower().split('\n')
    else:
        wordlist = words_eng.lower().split('\n')

    wordlist.sort(key=len)
    for i in range(len(wordlist)):
        if len(wordlist[i]) > length:
            length += 1
            len_index.append(i)
    len_index.append(len(wordlist))

    # Установка значений по умолчанию
    if True not in choices:
        choices[0] = True
    if True not in language:
        language[1] = True
    if language[0] and language[1]:
        language[0] = False
    for i in range(len(choices)):
        if choices[i]:
            include.append((len_index[i], len_index[i + 1]))

    #  Установка уровня сложности в зависимости от выбора пользователя
    if speed[0]:
        test = [1, 1.2, 1.4, 1.6, 1.8, 2]
    if speed[1]:
        test = [2, 2.2, 2.4, 2.6, 2.8, 3]
    if speed[2]:
        test = [3.5, 3.2, 3.4, 3.6, 3.8, 4]

    if True not in speed:
        speed[1] = True
    if (speed[0] and speed[1]) or (speed[1] and speed[2]) or (speed[0] and speed[2]) or (speed[0] and speed[1] and speed[2]):
        speed[1] = True
        speed[0], speed[2] = False, False

    for i in range(level):
        sp = random.choice(test)
        y_pos = random.randint(50 + (i * vertical_spacing), (i + 1) * vertical_spacing)
        x_pos = random.randint(WIDTH, WIDTH + 1000)
        ind_sel = random.choice(include)
        index = random.randint(ind_sel[0], ind_sel[1])
        text = wordlist[index].lower()
        new_word = Word(text, sp, x_pos, y_pos)
        word_objs.append(new_word)

    return word_objs


#  Метод для записи лучшего результата в отдельный файл
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
        resume_butt, changes, quit_butt, changed_lang, changed_speed = draw_pause()
        if resume_butt:
            paused = False
        if quit_butt:
            check_high_score()
            running = False
        # Проверка значений кнопок выхода и старта игры

    if new_level and not paused:
        word_objects = generate_level()  # Генерация уровня
        new_level = False
    else:
        for w in word_objects:
            w.draw()
            if not paused:
                w.update()
            if w.x_pos < -200:  # Если пользователь не успел дописать слово
                word_objects.remove(w)
                lives -= 1
                score -= 20
                lives_less.play()
    if len(word_objects) <= 0 and not paused:  # Переход на новый уровень
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
            check_high_score()  # Запись рекорда при выходе из игры
            running = False

        if event.type == pygame.KEYDOWN:
            if not paused:
                if (event.unicode.lower() in eng_letters or event.unicode.lower() in rus_letters) and len(
                        active_string) <= 8:
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
                language = changed_lang
                speed = changed_speed

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
        # Замена значений на значения по умолчанию при пройгрыше

    pygame.display.flip()
pygame.quit()
