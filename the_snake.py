from random import choice, randint

import pygame as pg

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
ALL_DIRECTION = (UP, DOWN, LEFT, RIGHT)

BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption(f'Змейка: Для выхода нажмите ESC')

# Настройка времени:
clock = pg.time.Clock()


class GameObject:
    """Класс GameObject используется как базовый
    класс от которого наследуются другие игровые объекты.
    """

    def __init__(self, position: tuple = None, body_color: tuple = None) -> None:
        """Метод инициализотор атрибутов экземплера класса."""
        if not position and not body_color:
            raise ValueError(
                'Необходимо указать параметры объекта %s.'
                % (self.__class__.__name__))
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Метод отрисовки обьекта на игровом поле."""
        raise NotImplementedError(
            'Определите draw в %s.' % (self.__class__.__name__))


class Apple(GameObject):
    """Класс описывающий яблоко на игровом поле."""

    def __init__(self, snake_position: tuple = None, body_color: tuple = APPLE_COLOR) -> None:
        """Метод инициализатор атрибутов объекта яблоко."""
        super().__init__(body_color = body_color)
        self.randomize_position(snake_position)

    def randomize_position(self, snake_position) -> tuple:
        """Метод генерации случайного положения объекта яблоко."""
        while True:
            self.position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
            for self.position in snake_position:
                continue
            else:
                return self.position
                
        
    def draw(self) -> None:
        """Метод отрисовки объекта яблоко."""
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс описывающий змейку на игровом поле."""

    length = 1

    def __init__(self, position: tuple = CENTER, body_color: tuple = SNAKE_COLOR) -> None:
        """Метод инициализатор атрибутов объекта змейка."""
        super().__init__(position, body_color)
        self.positions = [self.position]
        self.direction = RIGHT
        # self.length = 1
        # self.next_direction = None
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

    def update_direction(self, next_direction) -> None:
        """Метод обновления направления после нажатия на кнопку."""
        self.direction = next_direction
            
    def get_head_position(self) -> tuple:
        """Метод опредления положения головы змейки."""
        return self.positions[0]

    def reset(self) -> None:
        """Метод сброса змейки в начальное состоянии после
        столкновения с собой.
        """
        self.length = 1
        self.positions = [self.position]
        self.direction = choice(ALL_DIRECTION)

    def draw(self) -> None:
        """Метод отрисовки объекта змейки, проверка состояния
        последнего элемента в списке положения змейки.
        """
        for position in self.positions[:-1]:
            rect = (pg.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pg.draw.rect(screen, self.body_color, rect)
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)
        # Отрисовка головы змейки
        head_rect = pg.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, head_rect)
        pg.draw.rect(screen, BORDER_COLOR, head_rect, 1)
        # Затирание последнего сегмента
        if self.last:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


def handle_keys(snake) -> None:
    """Функция обработки действий пользователя."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and snake.direction != DOWN:
                snake.update_direction(UP)
                #snake.next_direction = UP
            elif event.key == pg.K_DOWN and snake.direction != UP:
                snake.update_direction(DOWN)
                #snake.next_direction = DOWN
            elif event.key == pg.K_LEFT and snake.direction != RIGHT:
                snake.update_direction(LEFT)
                #snake.next_direction = LEFT
            elif event.key == pg.K_RIGHT and snake.direction != LEFT:
                snake.update_direction(RIGHT)
                #snake.next_direction = RIGHT
            elif event.key == pg.K_ESCAPE:
                pg.quit()
            

def main():
    """Функция запуска игрового процесса."""
    pg.init()
    snake = Snake()
    apple = Apple(snake.positions)
    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.move()
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)
        elif snake.positions[0] in snake.positions[4:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()
        pg.display.update()


if __name__ == '__main__':
    main()

# Метод draw класса Apple
# def draw(self):
#     rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
#     pg.draw.rect(screen, self.body_color, rect)
#     pg.draw.rect(screen, BORDER_COLOR, rect, 1)

# # Метод draw класса Snake
# def draw(self):
#     for position in self.positions[:-1]:
#         rect = (pg.Rect(position, (GRID_SIZE, GRID_SIZE)))
#         pg.draw.rect(screen, self.body_color, rect)
#         pg.draw.rect(screen, BORDER_COLOR, rect, 1)

#     # Отрисовка головы змейки
#     head_rect = pg.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
#     pg.draw.rect(screen, self.body_color, head_rect)
#     pg.draw.rect(screen, BORDER_COLOR, head_rect, 1)

#     # Затирание последнего сегмента
#     if self.last:
#         last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
#         pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

# Функция обработки действий пользователя
# def handle_keys(game_object):
#     for event in pg.event.get():
#         if event.type == pg.QUIT:
#             pg.quit()
#             raise SystemExit
#         elif event.type == pg.KEYDOWN:
#             if event.key == pg.K_UP and game_object.direction != DOWN:
#                 game_object.next_direction = UP
#             elif event.key == pg.K_DOWN and game_object.direction != UP:
#                 game_object.next_direction = DOWN
#             elif event.key ==
#                   pg.K_LEFT and game_object.direction != RIGHT:
#                 game_object.next_direction = LEFT
#             elif event.key ==
#                   pg.K_RIGHT and game_object.direction != LEFT:
#                 game_object.next_direction = RIGHT

# Метод обновления направления после нажатия на кнопку
# def update_direction(self):
#     if self.next_direction:
#         self.direction = self.next_direction
#         self.next_direction = None
