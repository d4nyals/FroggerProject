import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Set up screen dimensions with a 9:16 aspect ratio (540x960)
width = 540
height = 960
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Frogger')

# Game flags
game_over = False
lives = 3

# Load frog image (keep it at a fixed size)
frog_img = pygame.image.load("frog.png")
frog_img = pygame.transform.scale(frog_img, (50, 50))  # Scale the image for the frog

# Current frog position
frog = pygame.Rect(240, 880, 60, 60)

# Load car image
car_img = pygame.image.load("car.png")
car_img = pygame.transform.scale(car_img, (120, 100))  # Resize car image

# Road and kerb positions (vertical road now becomes horizontal)
road = pygame.Rect(70, 150, 400, 700)  # Large road area for the cars to move
kerb_top = pygame.Rect(70, 150, 400, 10)  # Top kerb
kerb_bottom = pygame.Rect(70, 850, 400, 10)  # Bottom kerb

# Movement speed
move_speed = 40  # Slower speed for frog's movement (steps)

# Background music
pygame.mixer.music.load("background_music.ogg")  # Convert to .ogg if needed
pygame.mixer.music.play(-1, 0.0)  # Loop the background music

# Car lanes (adjusted for horizontal lanes, vertical position on screen)
# Reduced lane height to compress the lanes and add more space between them
car_lanes = [200, 280, 360, 440, 520]  # 5 lanes for cars (from top to bottom of the screen)
car_spawn_delay = 2  # Delay between spawning new car in a lane (in seconds)
last_spawn_times = [0] * len(car_lanes)  # Track last spawn time for each lane


# Function to generate a car with random attributes
def generate_car():
    car_y = random.choice(car_lanes)  # Randomly place car in one of the lanes
    car_x = random.choice([0, width])  # Randomly start from left (0) or right (width)
    direction = "East" if car_x == 0 else "West"  # If starting from 0, move East, otherwise West
    car_speed = 6  # Set all cars speed to 6
    car_rect = pygame.Rect(car_x, car_y, 120, 80)  # Rectangle for car
    return {"rect": car_rect, "direction": direction, "speed": car_speed}


# Create an array to store cars and track last exit time for each lane
cars = [None] * len(car_lanes)  # Initially no cars in any lanes

# Game loop
clock = pygame.time.Clock()  # Create a clock object for controlling the frame rate
while not game_over:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            game_over = True

    # Key controls (move one step per key press)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        frog.x -= move_speed
    if keys[pygame.K_RIGHT]:
        frog.x += move_speed
    if keys[pygame.K_UP]:
        frog.y -= move_speed
    if keys[pygame.K_DOWN]:
        frog.y += move_speed

    # Prevent frog from going out of bounds horizontally (left/right)
    frog.x = max(kerb_top.right, min(frog.x, kerb_bottom.left - frog.width))

    # Prevent frog from going out of bounds vertically (top/bottom)
    frog.y = max(road.top, min(frog.y, road.bottom - frog.height))

    # Move and generate cars in lanes with controlled delays
    current_time = time.time()  # Get the current time
    for i, lane in enumerate(car_lanes):
        # If it's time to spawn a new car in this lane
        if cars[i] is None and current_time - last_spawn_times[i] >= car_spawn_delay:
            # Generate a new car
            cars[i] = generate_car()
            last_spawn_times[i] = current_time  # Update last spawn time for this lane

        # Move the car in the current lane if it exists
        if cars[i] is not None:
            car = cars[i]
            car_rect = car["rect"]
            direction = car["direction"]
            speed = car["speed"]

            # Move car depending on its direction
            if direction == "East":
                car_rect.move_ip(speed, 0)  # Move right (East)
                if car_rect.left > width:  # If the car moves off the screen, reset to left
                    car_rect.right = 0
                    car_rect.top = lane  # Keep car in the same lane
                    cars[i] = None  # Remove car from lane after it exits
            elif direction == "West":
                car_rect.move_ip(-speed, 0)  # Move left (West)
                if car_rect.right < 0:  # If the car moves off the screen, reset to right
                    car_rect.left = width
                    car_rect.top = lane  # Keep car in the same lane
                    cars[i] = None  # Remove car from lane after it exits

    # Fill screen with black background
    screen.fill((0, 0, 0))

    # Draw road and kerbs (road area for cars)
    pygame.draw.rect(screen, (50, 50, 50), road)  # Dark grey for the road
    pygame.draw.rect(screen, (0, 0, 0), kerb_top)  # Black for top kerb
    pygame.draw.rect(screen, (0, 0, 0), kerb_bottom)  # Black for bottom kerb

    # Draw lane dividers (horizontal white lines)
    lane_divider_color = (255, 255, 255)  # White color for the dividers
    for i in range(1, len(car_lanes)):
        lane_y = car_lanes[i]  # Y position of lane divider
        pygame.draw.line(screen, lane_divider_color, (road.left, lane_y), (road.right, lane_y), 5)

    # Draw cars with their respective direction (flip horizontally if facing West)
    for car_lane in cars:
        if car_lane is not None:
            car_rect = car_lane["rect"]
            if car_lane["direction"] == "West":
                # Flip the car image for West direction
                flipped_car_img = pygame.transform.flip(car_img, True, False)
                screen.blit(flipped_car_img, car_rect)
            else:
                # Normal car image for East direction
                screen.blit(car_img, car_rect)

    # Draw frog
    screen.blit(frog_img, frog)

    # Update screen
    pygame.display.update()

    # Control frame rate to smoothen car movement
    clock.tick(60)  # Set the frame rate to 60 FPS to ensure smooth movement

pygame.quit()
