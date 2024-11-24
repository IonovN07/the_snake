from random import choice, randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
CENTER = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Класс GameObject используется как базовый
    класс от которого наследуются другие игровые объекты.
    """

    def __init__(self, body_color: tuple = None) -> None:
        """Метод инициализотор атрибутов экземплера класса."""
        self.position = (CENTER)
        self.body_color = body_color

    def draw(self):
        """Метод отрисовки обьекта на игровом поле."""
        pass


class Apple(GameObject):
    """Класс описывающий яблоко на игровом поле."""

    def __init__(self) -> None:
        """Метод инициализатор атрибутов объекта яблоко."""
        super().__init__(APPLE_COLOR)
        self.position = self.randomize_position()

    def randomize_position(self) -> tuple:
        """Метод генерации случайного положения объекта яблоко."""
        position_not_center = True
        while position_not_center:
            self.position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
            if self.position != CENTER:
                position_not_center = False
        return self.position

    def draw(self) -> None:
        """Метод отрисовки объекта яблоко."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс описывающий змейку на игровом поле."""

    def __init__(self) -> None:
        """Метод инициализатор атрибутов объекта змейка."""
        super().__init__(SNAKE_COLOR)
        self.positions = [self.position]
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def move(self) -> None:
        """Метод отвечает за передвижение объекта змейка, получает
        начальные координаты головы змейки и добавляет в начало списка
        новую позицию согласно значению нажатой кнопки.
        """
        x_position, y_position = self.get_head_position()
        x_next_position, y_next_position = self.direction
        x_new_position = (
            x_position
            + x_next_position
            * GRID_SIZE) % SCREEN_WIDTH
        y_new_position = (
            y_position
            + y_next_position
            * GRID_SIZE) % SCREEN_HEIGHT
        position = (x_new_position, y_new_position)
        self.positions.insert(0, position)
        # Проверка длины змейки
        if self.length < len(self.positions):
            self.last = self.positions.pop()

    def update_direction(self) -> None:
        """Метод обновления направления после нажатия на кнопку."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def get_head_position(self) -> tuple:
        """Метод опредления положения головы змейки."""
        head_position_snake = self.positions[0]
        return head_position_snake

    def reset(self) -> None:
        """Метод сброса змейки в начальное состоянии после
        столкновения с собой.
        """
        self.length = 1
        self.positions = [self.position]
        all_direction = (RIGHT, LEFT, DOWN, UP)
        self.direction = choice(all_direction)
        screen.fill(BOARD_BACKGROUND_COLOR)

    def draw(self) -> None:
        """Метод отрисовки объекта змейки, проверка состояния
        последнего элемента в списке положения змейки.
        """
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)
    # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)
    # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


def handle_keys(game_object) -> None:
    """Функция обработки действий пользователя."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Функция запуска игрового процесса."""
    pygame.init()
    apple = Apple()
    snake = Snake()
    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        apple.draw()
        snake.draw()
        if snake.positions[0] == apple.position:
            snake.length += 1
            apple.position = apple.randomize_position()
        if snake.positions[0] in snake.positions[1:]:
            snake.reset()
        pygame.display.update()


if __name__ == '__main__':
    main()

# Метод draw класса Apple
# def draw(self):
#     rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
#     pygame.draw.rect(screen, self.body_color, rect)
#     pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

# # Метод draw класса Snake
# def draw(self):
#     for position in self.positions[:-1]:
#         rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
#         pygame.draw.rect(screen, self.body_color, rect)
#         pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

#     # Отрисовка головы змейки
#     head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
#     pygame.draw.rect(screen, self.body_color, head_rect)
#     pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

#     # Затирание последнего сегмента
#     if self.last:
#         last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
#         pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

# Функция обработки действий пользователя
# def handle_keys(game_object):
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             raise SystemExit
#         elif event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_UP and game_object.direction != DOWN:
#                 game_object.next_direction = UP
#             elif event.key == pygame.K_DOWN and game_object.direction != UP:
#                 game_object.next_direction = DOWN
#             elif event.key ==
#                   pygame.K_LEFT and game_object.direction != RIGHT:
#                 game_object.next_direction = LEFT
#             elif event.key ==
#                   pygame.K_RIGHT and game_object.direction != LEFT:
#                 game_object.next_direction = RIGHT

# Метод обновления направления после нажатия на кнопку
# def update_direction(self):
#     if self.next_direction:
#         self.direction = self.next_direction
#         self.next_direction = None
