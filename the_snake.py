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
DIRECTION = {
    (LEFT, pg.K_UP): UP,
    (RIGHT, pg.K_UP): UP,
    (UP, pg.K_UP): UP,
    (LEFT, pg.K_DOWN): DOWN,
    (RIGHT, pg.K_DOWN): DOWN,
    (DOWN, pg.K_DOWN): DOWN,
    (UP, pg.K_LEFT): LEFT,
    (DOWN, pg.K_LEFT): LEFT,
    (LEFT, pg.K_LEFT): LEFT,
    (UP, pg.K_RIGHT): RIGHT,
    (DOWN, pg.K_RIGHT): RIGHT,
    (RIGHT, pg.K_RIGHT): RIGHT
}

BOARD_BACKGROUND_COLOR = (128, 128, 128)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
screen.fill(BOARD_BACKGROUND_COLOR)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка: Для выхода нажмите ESC')

# Настройка времени:
clock = pg.time.Clock()


class GameObject:
    """Класс GameObject используется как базовый
    класс от которого наследуются другие игровые объекты.
    """

    def __init__(
            self, position: tuple = None, body_color: tuple = None) -> None:
        """Метод инициализотор атрибутов экземплера класса."""
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Метод отрисовки обьекта на игровом поле."""
        raise NotImplementedError(
            'Определите draw в %s.' % (self.__class__.__name__))

    def drawing_one_cell(self, position, body_color=None):
        """Метод отрисовки одной ячейки."""
        if not body_color:
            body_color = self.body_color
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, body_color, rect)
        return rect


class Apple(GameObject):
    """Класс описывающий яблоко на игровом поле."""

    def __init__(
            self, snake_position: tuple = CENTER,
            body_color: tuple = APPLE_COLOR) -> None:
        """Метод инициализатор атрибутов объекта яблоко."""
        super().__init__(body_color=body_color)
        self.randomize_position(snake_position)

    def randomize_position(self, snake_position) -> tuple:
        """Метод генерации случайного положения объекта яблоко."""
        while True:
            self.position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
            if self.position in snake_position:
                continue
            else:
                return self.position

    def draw(self) -> None:
        """Метод отрисовки объекта яблоко."""
        rect = self.drawing_one_cell(self.position)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс описывающий змейку на игровом поле."""

    def __init__(
            self, position: tuple = CENTER,
            body_color: tuple = SNAKE_COLOR) -> None:
        """Метод инициализатор атрибутов объекта змейка."""
        super().__init__(position, body_color)
        self.reset()

    def move(self) -> None:
        """Метод отвечает за передвижение объекта змейка, получает
        начальные координаты головы змейки и добавляет в начало списка
        новую позицию согласно значению нажатой кнопки.
        """
        x_position, y_position = self.get_head_position()
        x_next_position, y_next_position = self.direction
        position = (
            (x_position + x_next_position * GRID_SIZE) % SCREEN_WIDTH,
            (y_position + y_next_position * GRID_SIZE) % SCREEN_HEIGHT)
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
        """Метод сброса змейки в начальное состоянии."""
        self.last = None
        self.length = 1
        self.positions = [self.position]
        self.direction = choice(ALL_DIRECTION)

    def draw(self) -> None:
        """Метод отрисовки объекта змейки, проверка состояния
        последнего элемента в списке положения змейки.
        """
        # Отрисовка головы змейки
        head_rect = self.drawing_one_cell(self.get_head_position())
        pg.draw.rect(screen, BORDER_COLOR, head_rect, 1)
        # Затирание последнего сегмента
        if self.last:
            self.drawing_one_cell(self.last, BOARD_BACKGROUND_COLOR)


def handle_keys(snake) -> None:
    """Функция обработки действий пользователя."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and snake.direction != DOWN:
                snake.update_direction(
                    dict.get(DIRECTION, (snake.direction, event.key)))
            elif event.key == pg.K_DOWN and snake.direction != UP:
                snake.update_direction(
                    dict.get(DIRECTION, (snake.direction, event.key)))
            elif event.key == pg.K_LEFT and snake.direction != RIGHT:
                snake.update_direction(
                    dict.get(DIRECTION, (snake.direction, event.key)))
            elif event.key == pg.K_RIGHT and snake.direction != LEFT:
                snake.update_direction(
                    dict.get(DIRECTION, (snake.direction, event.key)))
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
