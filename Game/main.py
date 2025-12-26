import pygame
from pygame.locals import *
import time
import random

SIZE = 40

class Game:
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((1000, 500))
        pygame.display.set_caption("Snake Game")

        self.snake = Snake(self.surface, 1)
        self.apple = Apple(self.surface)

    def is_collision(self, x1, y1, x2, y2):
        return x1 == x2 and y1 == y2
    
    
    
    def display_score(self):
        font = pygame.font.SysFont('arial' , 30)
        score = font.render(f"Score: {self.snake.length}" , True , (0 , 0 , 0))
        self.surface.blit(score , (850 , 10))
    
    def reset(self):
        self.snake = Snake(self.surface, 1)
        self.apple = Apple(self.surface)


    def play(self):
        # 1️ Clear screen
        self.surface.fill((29, 235, 85))
        self.display_score()

        # 2️ Update logic
        self.snake.walk()

        if self.is_collision(self.apple.x, self.apple.y,
                             self.snake.x[0], self.snake.y[0]):
            self.snake.increase_length()
            self.apple.move()
        
        # Snake collision with itself
        if(self.snake.length > 2):
            for i in range(1 , self.snake.length):
                if( self.is_collision(self.snake.x[i] , self.snake.y[i] , self.snake.x[0] , self.snake.y[0])):
                    raise Exception("Game Over")    
    
        # Wall collision
        if (self.snake.x[0] < 0 or self.snake.x[0] >= 1000 or
            self.snake.y[0] < 0 or self.snake.y[0] >= 500):
               raise Exception("Game over")
            


        # 3️ Draw everything
        self.apple.draw()
        self.snake.draw()

        # 4️ Update display
        pygame.display.flip()
    def show_game_over(self):
        self.surface.fill((29, 235, 85))
        font = pygame.font.SysFont('arial', 36)

        line1 = font.render("GAME OVER", True, (255, 0, 0))
        line2 = font.render(f"Score : {self.snake.length}", True, (255, 0 , 0))
        line3 = font.render("Press ENTER to Play Again", True, (255, 0, 0))

        # CENTERED coordinates
        self.surface.blit(line1, (400, 180))   # Game Over
        self.surface.blit(line2, (420, 230))   # Score
        self.surface.blit(line3, (300, 280))   # Restart instruction

        pygame.display.flip()


    def run(self):
        running = True
        pause = False
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

                if event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        self.reset()
                        pause = False

                    if event.key == K_ESCAPE:
                        running = False
                    elif event.key == K_UP:
                        self.snake.move_up()
                    elif event.key == K_DOWN:
                        self.snake.move_down()
                    elif event.key == K_LEFT:
                        self.snake.move_left()
                    elif event.key == K_RIGHT:
                        self.snake.move_right()
            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause = True

            time.sleep(0.25)


class Snake:
    def __init__(self, parent_screen, length):
        self.parent_screen = parent_screen
        self.block = pygame.image.load("Resources/block.jpg").convert()
        self.length = length
        self.x = [SIZE] * length
        self.y = [SIZE] * length
        self.direction = "right"

    def increase_length(self):
        self.length += 1
        self.x.append(self.x[-1])
        self.y.append(self.y[-1])

    def move_up(self):
        if self.direction != "down":
            self.direction = "up"

    def move_down(self):
        if self.direction != "up":
            self.direction = "down"

    def move_left(self):
        if self.direction != "right":
            self.direction = "left"

    def move_right(self):
        if self.direction != "left":
            self.direction = "right"


    def walk(self):
        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        if self.direction == "up":
            self.y[0] -= SIZE
        elif self.direction == "down":
            self.y[0] += SIZE
        elif self.direction == "left":
            self.x[0] -= SIZE
        elif self.direction == "right":
            self.x[0] += SIZE

    def draw(self):
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))


class Apple:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("resources/apple.jpg").convert()
        self.move()

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))

    def move(self):
        self.x = random.randint(1, 24) * SIZE
        self.y = random.randint(1, 12) * SIZE


if __name__ == "__main__":
    game = Game()
    game.run()
