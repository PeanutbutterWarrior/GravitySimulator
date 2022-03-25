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
    x_position_change = 0
    y_position_change = 0


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
DISTANCE_SCALE_FACTOR = 1e6
FRAMES_PER_SECOND = 30
SIM_SECONDS_PER_FRAME = 60 * 60 * 24
STEPS_PER_FRAME = 10

G = 6.67430e-11

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Gravity Simulator')

bodies = [
    Body('Earth', 0, 0, 0, 0, 5.97237e24, 50),
    Body('Moon', 385000000, 0, 0, -1018, 7.348e22, 20),
]

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    # Physics Calc
    for body1 in bodies:
        for body2 in bodies:
            if body1 is body2:
                continue

            dx = body2.x_position - body1.x_position
            dy = body2.y_position - body1.y_position
            distance2 = dx * dx + dy * dy
            force = G * (body1.mass * body2.mass) / distance2
            acceleration = force / body1.mass

            scale = acceleration / math.sqrt(distance2)
            x_acceleration = dx * scale
            y_acceleration = dy * scale

            body1.x_velocity += x_acceleration * 60 * 60 * 24
            body1.y_velocity += y_acceleration * 60 * 60 * 24

            body1.x_position_change = body1.x_position + body1.x_velocity * 60 * 60 * 24  # Multiplied for a day per frame
            body1.y_position_change = body1.y_position + body1.y_velocity * 60 * 60 * 24  # Multiplied for a day per frame

    for body in bodies:
        body.x_position = body.x_position_change
        body.y_position = body.y_position_change

    # Rendering
    screen.fill(BLACK)
    for body in bodies:
        pygame.draw.circle(
            screen,
            WHITE,
            (
                int(body.x_position / DISTANCE_SCALE_FACTOR + SCREEN_WIDTH / 2),
                int(body.y_position / DISTANCE_SCALE_FACTOR + SCREEN_HEIGHT / 2),
            ),
            body.radius
        )
    pygame.display.flip()

    clock.tick(FRAMES_PER_SECOND)
