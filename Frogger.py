from pygame import *

init()

# Set up screen dimensions
width = 600
height = 400
screen = display.set_mode((width, height))
display.set_caption('frogger')

# Game flag
game_over = False

# Load frog image and scale it
frog_img = image.load("frog.png")
frog_img = transform.scale(frog_img, (40, 40))

# Frog position
frog = Rect(280, 350, 40, 40)

# Road and kerb positions
road = Rect(100, 50, 400, 300)
kerb_left = Rect(90, 50, 10, 300)
kerb_right = Rect(490, 50, 10, 300)

# Movement speed
move_speed = 5

# Game loop
while not game_over:
    for e in event.get():  # Changed 'event' to 'e'
        if e.type == QUIT:
            game_over = True

    # Key controls
    keys = key.get_pressed()
    if keys[K_LEFT]:
        frog.x -= move_speed
    if keys[K_RIGHT]:
        frog.x += move_speed
    if keys[K_UP]:
        frog.y -= move_speed
    if keys[K_DOWN]:
        frog.y += move_speed

    # Prevent frog going out of bounds
    frog.x = max(kerb_left.right, min(frog.x, kerb_right.left - frog.width))
    frog.y = max(road.top, min(frog.y, road.bottom - frog.height))

    # Fill screen
    screen.fill((0, 0, 0))

    # Draw road and kerbs
    draw.rect(screen, (50, 50, 50), road)
    draw.rect(screen, (0, 0, 0), kerb_left)
    draw.rect(screen, (0, 0, 0), kerb_right)

    # Draw frog
    screen.blit(frog_img, frog)

    # Update screen
    display.update()

    # Control frame rate
    time.delay(30)

quit()

# end of week 1 coding
# ISSUES WITH ADDING MUSIC AND SOUND FIX
