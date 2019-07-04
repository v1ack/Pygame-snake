import pygame
import sys
# Очередь - для частей змейки
from collections import deque
from random import randint

# Инициализация движка
pygame.init()

# Группы со спрайтами для более простого управления, одна для частей змейки, другая для еды
snake_parts_group = pygame.sprite.Group()
eat_group = pygame.sprite.Group()
block_group = pygame.sprite.Group()


# Спрайт части змеи - квадрата
class SnakePart(pygame.sprite.Sprite):
    def __init__(self, x, y):
        # Добавляем в группу со всеми частями змеи, обращаясь к __init__ родительского класса
        super().__init__(snake_parts_group)
        # Задаем прямоугольник с координатами x, y и размером 25х25
        self.rect = pygame.Rect(x, y, 25, 25)
        # Делаем для него поверхность такого же размера
        self.image = pygame.Surface((25, 25))
        # Заполняем поверхность цветом
        pygame.Surface.fill(self.image, (255, 255, 255))


# Спрайт еды, все тоже самое как и с частью змеи, но другой цвет
class Eat(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(eat_group)
        self.rect = pygame.Rect(x, y, 25, 25)
        self.image = pygame.image.load('apple.png')


# Спрайт блока, все тоже самое как и с частью змеи, но другой цвет
class Block(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(block_group)
        self.rect = pygame.Rect(x, y, 25, 25)
        self.image = pygame.Surface((25, 25))
        pygame.Surface.fill(self.image, (150, 150, 150))


# Сама змея
class Snake:
    def __init__(self, map_size):
        # Создаем очередь для её частей
        self.parts = deque()
        # Добавляем в нее один квадрат змеи с координатами 300, 300
        self.parts.append(SnakePart(300, 300))
        # Задаем переменную, в которой будет храниться позиция головы
        self.position = [300, 300]
        # Переменная для направления
        self.direction = 'up'
        # Запоминаем границы карты
        self.map_size = map_size

    # Функция для обновления змейки
    def update(self):
        # Получаем список нажатых клавиш
        key_state = pygame.key.get_pressed()
        # Если среди них есть нужные нам клавиши, то меняем направление змейки
        if key_state[pygame.K_UP]:
            self.direction = 'up'
        elif key_state[pygame.K_DOWN]:
            self.direction = 'down'
        elif key_state[pygame.K_LEFT]:
            self.direction = 'left'
        elif key_state[pygame.K_RIGHT]:
            self.direction = 'right'

        # По направлению змейки меняем позицию для головы
        if self.direction == 'up':
            self.position[1] -= 25
        if self.direction == 'down':
            self.position[1] += 25
        if self.direction == 'left':
            self.position[0] -= 25
        if self.direction == 'right':
            self.position[0] += 25

        # Проверяем новую позицию
        # Если выходит за рамки карты - меняем позицию на противоположенную
        if self.position[0] >= self.map_size[0]:
            self.position[0] = 0
        if self.position[0] < 0:
            self.position[0] = self.map_size[0]
        if self.position[1] >= self.map_size[1]:
            self.position[1] = 0
        if self.position[1] < 0:
            self.position[1] = self.map_size[1]

        # Проверяем совпадение головы (self.parts[-1] - последний элемент в нашей очереди) с объектами из группы еды
        # И сразу удаляем еду, если совпадение есть (третий аргумент - True)
        eat = pygame.sprite.spritecollide(self.parts[-1], eat_group, True)
        # Если совпадений не нашлось, значит еда не была съедена, удаляем первый элемент очереди - конец змейки
        if not eat:
            snake_parts_group.remove(self.parts.popleft())
        # Добавляем в конец очереди новую часть змейки, с новыми координатоми головы
        self.parts.append(SnakePart(self.position[0], self.position[1]))

        # Обработка столкновения змеи с сомой собой
        if len(self.parts):
            # Обрабатываем столкновения с блоками
            death = pygame.sprite.spritecollide(self.parts[-1], block_group, False)
            if death:
                sys.exit()
            # Наложение головы (последего элемента в очереди) на другие части змеи (группы частей змеи)
            game_over = pygame.sprite.spritecollide(self.parts[-1], snake_parts_group, False)
            # Проверяем количество наложений. Минимум 1 будет всегда, потомучто сама голова входит в эту группу
            if len(game_over) > 1:
                sys.exit()


class Game:
    def __init__(self, game_map):
        # Устанавливаем размеры экрана
        self.WIDTH = 800
        self.HEIGHT = 650
        # Создаем экран
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        # Ставим игре заголовок
        pygame.display.set_caption("Snake")
        # Это нужно для обновления экрана
        self.clock = pygame.time.Clock()
        # Создаем змею, передав ей границы карты
        self.snake = Snake((self.WIDTH, self.HEIGHT))
        # Загружаем карту из фала
        for j in range(int(self.WIDTH/25)):
            for i in range(int(self.HEIGHT/25)):
                if game_map[i][j] == 'x':
                    Block(j*25, i*25)

    # Главная функция, в которой всё происходит
    def loop(self):
        # FPS
        self.clock.tick(7)
        # Заполняем экран черным
        self.screen.fill((0, 0, 0))
        # Если список еды пуст - создаем еду в случайном месте
        if not len(eat_group):
            Eat(randint(0, 31) * 25, randint(0, 25) * 25)
        # Отрисовываем группы с частями змеи и едой на экране
        block_group.draw(self.screen)
        eat_group.draw(self.screen)
        snake_parts_group.draw(self.screen)
        # Обновляем змею
        self.snake.update()
        # Обновляем экран
        pygame.display.flip()
        # Обработка закрытия программы
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()


# Открываем карту
game_map = []
with open('map', 'r') as file:
    for line in file.readlines():
        t = []
        for i in line[:-1]:
            t.append(i)
        game_map.append(t)
# print(game_map)
# Создаем объект игры
snake = Game(game_map)
# И постоянно выполняем главную функцию игры
while True:
    snake.loop()
