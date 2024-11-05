from random import randint
import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвета:
BOARD_BACKGROUND_COLOR = (0, 0, 0)  # Черный фон
BORDER_COLOR = (93, 216, 228)        # Цвет границы ячейки
APPLE_COLOR = (255, 0, 0)           # Цвет яблока
SNAKE_COLOR = (0, 255, 0)           # Цвет змейки

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self, position=None, body_color=None):
        """Инициализация координат и цвета объекта."""
        if position is None:
            position = (0, 0)
        self.position = position
        self.body_color = body_color if body_color is not None else SNAKE_COLOR

    def draw(self):
        """
        Метод для отрисовки объекта.
        Должен быть переопределен в дочерних классах.
        """
        pass


class Apple(GameObject):
    """Класс для яблока."""

    def __init__(self):
        """Инициализация яблока с случайной позицией."""
        super().__init__(self.randomize_position(), APPLE_COLOR)

    def randomize_position(self):
        """Устанавливает случайное положение яблока на игровом поле."""
        x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        return (x, y)

    def draw(self):
        """Отрисовывает яблоко на игровом поле."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс для змейки."""

    def __init__(self):
        """Инициализация змейки с начальной позицией и направлением."""
        super().__init__((GRID_WIDTH // 2 * GRID_SIZE,
                          GRID_HEIGHT // 2 * GRID_SIZE), SNAKE_COLOR)
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            # Проверяем на возможность смены направления
            if (self.next_direction[0] * -1 != self.direction[0]
                    or self.next_direction[1] * -1 != self.direction[1]):
                self.direction = self.next_direction

    def move(self):
        """Обновляет позицию змейки."""
        head_x, head_y = self.positions[0]
        new_head_position = (head_x + self.direction[0] * GRID_SIZE,
                             head_y + self.direction[1] * GRID_SIZE)
        # Проверяем на столкновение со стенами
        if (new_head_position[0] < 0 or new_head_position[0] >= SCREEN_WIDTH
                or new_head_position[1] < 0 or new_head_position[1] >= SCREEN_HEIGHT):
            return False  # Столкновение со стеной

        # Добавляем новую голову в начало списка позиций
        self.positions.insert(0, new_head_position)

        # Удаляем последний элемент списка, если длина не увеличилась
        if len(self.positions) > self.length:
            self.positions.pop()

        return True

    def draw(self):
        """Отрисовывает змейку на экране."""
        for position in self.positions[:-1]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

    def reset(self):
        """Сбрасывает змейку в начальное состояние после столкновения с собой."""
        self.length = 1
        self.positions = [(GRID_WIDTH // 2 * GRID_SIZE,
                           GRID_HEIGHT // 2 * GRID_SIZE)]
        self.direction = RIGHT


def handle_keys(snake):
    """Обрабатывает нажатия клавиш для изменения направления движения змейки."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != DOWN:
                snake.next_direction = UP
            elif event.key == pygame.K_DOWN and snake.direction != UP:
                snake.next_direction = DOWN
            elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                snake.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                snake.next_direction = RIGHT


def main():
    """Основная функция игры."""
    # Инициализация PyGame:
    pygame.init()

    # Создаем экземпляры классов.
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)

        handle_keys(snake)

        snake.update_direction()

        # Двигаем змейку и проверяем столкновение со стенами
        if not snake.move():
            snake.reset()  # Сбрасываем игру при столкновении со стеной

        # Проверяем столкновение с яблоком
        if snake.positions[0] == apple.position:
            snake.length += 1
            apple.position = apple.randomize_position()  # Перемещаем яблоко

            # Проверяем не попало ли новое яблоко в тело змейки
            while apple.position in snake.positions:
                apple.position = apple.randomize_position()

        # Проверяем столкновение с самой собой
        if snake.positions[0] in snake.positions[1:]:
            snake.reset()

        # Отрисовка объектов
        screen.fill(BOARD_BACKGROUND_COLOR)  # Черный фон
        snake.draw()
        apple.draw()

        pygame.display.update()


if __name__ == '__main__':
    main()
