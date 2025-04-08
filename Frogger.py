import pygame
import random

# --- constants ---
WIDTH = 960  # 16:9 aspect ratio width
HEIGHT = 700  # 16:9 aspect ratio height
FPS = 30
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BROWN = (165, 42, 42)  # brown for the logs
GREY = (128, 128, 128)  # grey for the road


# --- classes ---
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 30))  # player is a green square
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 5
        self.direction = 'right'

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.direction = 'left'
            self.rect.x -= self.speed  # move player left
        if keys[pygame.K_RIGHT]:
            self.direction = 'right'
            self.rect.x += self.speed  # move player right
        if keys[pygame.K_UP]:
            self.direction = 'up'
            self.rect.y -= self.speed  # move player up
        if keys[pygame.K_DOWN]:
            self.direction = 'down'
            self.rect.y += self.speed  # move player down

        # keep player within screen bounds
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT


class Log(pygame.sprite.Sprite):
    def __init__(self, x, y, length):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((length, 30))  # logs are horizontally long
        self.image.fill(BROWN)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 2  # all logs move at the same speed
        self.direction = 'right'  # logs always move from right to left

    def update(self):
        if self.direction == 'right':
            self.rect.x += self.speed  # move log right
            if self.rect.left > WIDTH:  # if log goes off screen
                self.rect.right = 0  # wrap around to the left


class Car(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((60, 30))  # cars are horizontally longer
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        # set a random speed with a minimum of 3 and maximum of 5
        self.speed = random.randint(3, 5)  # random speed between 3 and 5
        self.direction = 'left'

    def update(self):
        if self.direction == 'left':
            self.rect.x -= self.speed  # move car left
            if self.rect.right < 0:  # if car goes off screen
                self.rect.left = WIDTH  # wrap around to the right side
        else:
            self.rect.x += self.speed  # move car right
            if self.rect.left > WIDTH:  # if car goes off screen
                self.rect.right = 0  # wrap around to the left side


# --- game setup ---
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Frogger")
clock = pygame.time.Clock()

# --- sprites ---
all_sprites = pygame.sprite.Group()
player = Player(WIDTH // 2, HEIGHT - 80)  # give space for the player to spawn
all_sprites.add(player)

logs = pygame.sprite.Group()
cars = pygame.sprite.Group()

# --- road ---
road_y = 350  # adjust the road's vertical position for more space
road_height = 200  # increased road height for proper car fitting
road_color = GREY

# --- cars ---
for i in range(5):
    car = Car(WIDTH, road_y + i * 40)  # car spawn positions with space between each
    cars.add(car)

# --- river ---
river_y = 100  # move the river up to provide a gap for the road
river_height = 180  # increased height of the river for better visibility
river_color = BLUE

# --- logs ---
log_rows = 5  # number of rows of logs
log_length = 200  # fixed length for all logs
log_width = 100  # log width is fixed
log_gap = 70  # a bit of space between logs
log_speed = 2  # speed of the logs (same for all)

# create logs in rows with fixed length and speed
for i in range(log_rows):
    for j in range(4):  # 4 logs per row
        log_x = j * (log_length + log_gap) + random.randint(100, 400)  # random starting X with space
        log_y = river_y + i * (river_height // log_rows) + 20  # move logs down by 20 units
        log = Log(log_x, log_y, log_length)  # create log with fixed length
        log.speed = log_speed  # set the speed for each log
        logs.add(log)


# --- finish line ---
finish_line_rect = pygame.Rect(0, 0, WIDTH, 30)

# function to draw alternating black and white lines for the finish line
def draw_finish_line():
    line_width = 20
    for i in range(0, WIDTH, line_width * 2):  # draw alternating black and white lines
        pygame.draw.rect(screen, WHITE, (i, 0, line_width, 30))
        pygame.draw.rect(screen, BLACK, (i + line_width, 0, line_width, 30))


# --- game loop ---
running = True
while running:
    # --- event handling ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- update ---
    all_sprites.update()
    logs.update()
    cars.update()

    # --- collisions ---
    # check for player collisions with cars
    hits = pygame.sprite.spritecollide(player, cars, False)
    if hits:
        # player hit a car, game over
        print("game over!")
        running = False

    # check for player collisions with logs
    hits = pygame.sprite.spritecollide(player, logs, False)
    if hits:
        # player is on a log, move with the log
        player.rect.x += hits[0].speed

    # check if player reaches the finish line
    if player.rect.colliderect(finish_line_rect):
        print("you win!")
        running = False

    # --- handle river collision ---
    river_rect = pygame.Rect(0, river_y, WIDTH, river_height)
    river_top_edge = pygame.Rect(0, river_y, WIDTH, 30)  # just the top 30 pixels of the river

    # check if the player touches the top edge of the river but is on a log (does not die)
    if player.rect.colliderect(river_top_edge) and not pygame.sprite.spritecollide(player, logs, False):
        # player is touching the top of the river but not on a log, they can continue without dying
        pass
    elif player.rect.colliderect(river_rect) and not pygame.sprite.spritecollide(player, logs, False):
        # player is not on a log and is in the body of the river, they fall in
        print("you fell in the river! game over!")
        running = False

    # --- draw ---
    screen.fill(BLACK)  # background color (black)

    # draw river (blue rectangle)
    pygame.draw.rect(screen, river_color, (0, river_y, WIDTH, river_height))

    # draw logs
    logs.draw(screen)

    # draw road (grey rectangle)
    pygame.draw.rect(screen, road_color, (0, road_y, WIDTH, road_height))

    # draw cars
    cars.draw(screen)

    # draw player and finish line
    all_sprites.draw(screen)
    draw_finish_line()  # draw the finish line

    # --- flip ---
    pygame.display.flip()

    # --- clock tick ---
    clock.tick(FPS)

# --- quit ---
pygame.quit()
