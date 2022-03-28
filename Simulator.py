import dataclasses
import pygame
import math


@dataclasses.dataclass
class Body:
    name: str
    x_position: float
    y_position: float
    x_velocity: float
    y_velocity: float
    mass: float
    radius: int
    color: tuple[int, int, int]
    new_x_position = 0
    new_y_position = 0


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

SCREEN_WIDTH = 2000
SCREEN_HEIGHT = 1000

FRAMES_PER_SECOND = 30
SIM_SECONDS_PER_FRAME = 60 * 60 * 24 * 3
STEPS_PER_FRAME = 200

G = 6.67430e-11

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Gravity Simulator')

paused = False
distance_scale_factor = None
camera_x_offset = 0
camera_y_offset = 0

bodies = [
    # Body('Earth', 0, 0, 0, 12.5, 5.97237e24, 50, (0, 0, 200)),
    # Body('Moon', 3.85e8, 0, 0, -1018, 7.348e22, 20, (200, 200, 200)),
    # Body('Spaceship', 7e7, 0, 0, -100, 5, 5, WHITE),

    #Body('Mars', 0, 0, 0, 0, 6.417e23, 40, (175, 0, 0)),
    #Body('Phobos', 9.4e6, 0, 0, 2138, 1.0659e16, 10, (200, 200, 200)),
    #Body('Deimos', -2e7, 0, 0, 1351.3, 1.4762e15, 6, (150, 150, 150)),

    Body('Sun', 0, 0, 0, 0, 1.9885e30, 30, (255, 255, 0)),
    Body('Mercury', 58e9, 0, 0, -47.36e3, 3.3011e23, 8, (200, 200, 200)),
    Body('Venus', -108e9, 0, 0, -35e3, 4.8675e24, 13, (255, 125, 0)),
    Body('Earth', 150e9, 0, 0, 29.78e3, 5.97237e24, 15, (0, 255, 0)),
    Body('Mars', -227e9, 0, 0, -24e3, 6.417e23, 12, (255, 0, 0)),
    Body('Jupiter', 50e9, -350e9, 10e3, 25e3, 8e29, 20, (200, 200, 125)),
]

distance_scale_factor_x = (max(bodies, key=lambda i: i.x_position).x_position -
                           min(bodies, key=lambda i: i.x_position).x_position
                           ) / SCREEN_WIDTH * 2
distance_scale_factor_y = (max(bodies, key=lambda i: i.y_position).y_position -
                           min(bodies, key=lambda i: i.y_position).y_position
                           ) / SCREEN_HEIGHT * 2
distance_scale_factor = max(distance_scale_factor_x, distance_scale_factor_y)

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                paused = not paused
        elif event.type == pygame.MOUSEWHEEL:
            distance_scale_factor *= 1.25 ** event.y

    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[pygame.K_LEFT]:
        camera_x_offset -= distance_scale_factor / 20
    elif pressed_keys[pygame.K_RIGHT]:
        camera_x_offset += distance_scale_factor / 20
    if pressed_keys[pygame.K_UP]:
        camera_y_offset -= distance_scale_factor / 20
    elif pressed_keys[pygame.K_DOWN]:
        camera_y_offset += distance_scale_factor / 20

    if not paused:
        # Physics Calc
        for _ in range(STEPS_PER_FRAME):
            for body1 in bodies:
                for body2 in bodies:
                    if body1 is body2:
                        continue

                    dx = body2.x_position - body1.x_position
                    dy = body2.y_position - body1.y_position
                    distance2 = dx * dx + dy * dy
                    if distance2 == 0:
                        continue
                    force = G * (body1.mass * body2.mass) / distance2
                    acceleration = force / body1.mass

                    scale = acceleration / math.sqrt(distance2)
                    x_acceleration = dx * scale
                    y_acceleration = dy * scale

                    body1.x_velocity += x_acceleration * SIM_SECONDS_PER_FRAME / STEPS_PER_FRAME
                    body1.y_velocity += y_acceleration * SIM_SECONDS_PER_FRAME / STEPS_PER_FRAME

                    body1.new_x_position = body1.x_position + body1.x_velocity * SIM_SECONDS_PER_FRAME / STEPS_PER_FRAME
                    body1.new_y_position = body1.y_position + body1.y_velocity * SIM_SECONDS_PER_FRAME / STEPS_PER_FRAME

            for body in bodies:
                body.x_position = body.new_x_position
                body.y_position = body.new_y_position

    # Rendering
    screen.fill(BLACK)
    for body in bodies:
        pygame.draw.circle(
            screen,
            body.color,
            (
                int((body.x_position - camera_x_offset * SCREEN_WIDTH) / distance_scale_factor + SCREEN_WIDTH / 2),
                int((body.y_position - camera_y_offset * SCREEN_HEIGHT) / distance_scale_factor + SCREEN_HEIGHT / 2),
            ),
            body.radius
        )
    pygame.display.flip()

    clock.tick(FRAMES_PER_SECOND)
