import pygame
import random
from direction import Direction
from collections import namedtuple
import time

pygame.init()

font = pygame.font.SysFont('arial.ttf', 25)

Point = namedtuple('Point', ['x', 'y'])
BLOCK_SIZE = 20
SPEED = 10

# rgb colors
WHITE = (255, 255, 255)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0, 0, 0)

class SnakeGame:
    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h

        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption("Snake")
        self.clock = pygame.time.Clock()

        self.direction = Direction.RIGHT

        self.head = Point(self.w / 2, self.h / 2)
        self.snake = [self.head,
                      Point(self.head.x-BLOCK_SIZE, self.head.y),
                      Point(self.head.x-(2*BLOCK_SIZE), self.head.y)
                      ]
        self.score = 0
        self.food = None
        self.enemy = None
        self.enemy_spawn = None
        self._place_food()
        self._place_enemy()



    def play_step(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT:
                    self.direction = Direction.RIGHT
                elif event.key == pygame.K_UP:
                    self.direction = Direction.UP
                elif event.key == pygame.K_DOWN:
                    self.direction = Direction.DOWN
        
        self._move(self.direction)
        self.snake.insert(0,self.head)

        game_over = False
        if self._is_collision():
            game_over = True
            return game_over, self.score

        if self.head == self.food:
            self.score += 1
            self._place_food()
        else:
            self.snake.pop()

        self.handle_enemy()
        self._update_ui()
        self.clock.tick(SPEED)

        return game_over, self.score

    def _place_food(self):
        x = random.randint(0, (self.w-BLOCK_SIZE)//BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (self.h-BLOCK_SIZE)//BLOCK_SIZE) * BLOCK_SIZE
        self.food = Point(x,y)
        if self.food in self.snake or self.food == self.enemy:
            self._place_food()

    def _place_enemy(self):
        x = random.randint(0, (self.w-BLOCK_SIZE)//BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (self.h-BLOCK_SIZE)//BLOCK_SIZE) * BLOCK_SIZE
        self.enemy = Point(x,y)
        self.enemy_spawn = time.time()
        if self.enemy in self.snake or self.enemy == self.food:
            self._place_enemy()

    def _update_ui(self):
        self.display.fill(BLACK)

        for pt in self.snake:
            pygame.draw.rect(self.display,
                        BLUE1,
                        pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE)
                        )

            pygame.draw.rect(self.display,
                        BLUE2,
                        pygame.Rect(pt.x+4, pt.y+4, 12, 12)
                        )

        pygame.draw.rect(self.display,
                    GREEN,
                    pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE)
                    )

        pygame.draw.rect(self.display,
                    RED,
                    pygame.Rect(self.enemy.x, self.enemy.y, BLOCK_SIZE, BLOCK_SIZE)
                    )

        text = font.render("Score: "+str(self.score), True, WHITE)
        self.display.blit(text,[0,0])
        pygame.display.flip()

    def _move(self, direction):
        x = self.head.x
        y = self.head.y
        if direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif direction == Direction.UP:
            y -= BLOCK_SIZE

        self.head = Point(x,y)

    def _is_collision(self):
        if self.head.x > self.w - BLOCK_SIZE or \
                self.head.x < 0 or \
                self.head.y > self.h -BLOCK_SIZE or \
                self.head.y < 0:
            return True

        if self.head in self.snake[1:]:
            return True

        if self.head == self.enemy:
            return True

        return False

    def handle_enemy(self):
        now = time.time()
        if now - self.enemy_spawn > 10:
            self._place_enemy()
