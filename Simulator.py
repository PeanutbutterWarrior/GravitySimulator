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
    x_position_change = 0
    y_position_change = 0


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

SCREEN_WIDTH = 2000
SCREEN_HEIGHT = 1000
DISTANCE_SCALE_FACTOR = 8e5
FRAMES_PER_SECOND = 30
SIM_SECONDS_PER_FRAME = 60 * 60
STEPS_PER_FRAME = 200

G = 6.67430e-11

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Gravity Simulator')

bodies = [
    Body('Earth', 0, 0, 0, 12.5, 5.97237e24, 50, (0, 0, 200)),
    Body('Moon', 3.85e8, 0, 0, -1018, 7.348e22, 20, (200, 200, 200)),
    Body('Spaceship', 7e7, 0, 0, -3000, 5, 5, WHITE),
    #Body('Mars', 0, 0, 0, 0, 6.417e23, 40, (175, 0, 0)),
    #Body('Phobos', 9.4e6, 0, 0, 2138, 1.0659e16, 10, (200, 200, 200)),
    #Body('Deimos', -2e7, 0, 0, 1351.3, 1.4762e15, 6, (150, 150, 150)),
]

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    # Physics Calc
    for _ in range(STEPS_PER_FRAME):
        for body1 in bodies:
            for body2 in bodies:
                if body1 is body2:
                    continue

                dx = body2.x_position + body2.x_position_change - body1.x_position - body1.x_position_change
                dy = body2.y_position + body2.y_position_change - body1.y_position - body1.y_position_change
                distance2 = dx * dx + dy * dy
                force = G * (body1.mass * body2.mass) / distance2
                acceleration = force / body1.mass

                scale = acceleration / math.sqrt(distance2)
                x_acceleration = dx * scale
                y_acceleration = dy * scale

                body1.x_velocity += x_acceleration * SIM_SECONDS_PER_FRAME / STEPS_PER_FRAME
                body1.y_velocity += y_acceleration * SIM_SECONDS_PER_FRAME / STEPS_PER_FRAME

                body1.x_position_change = body1.x_velocity * SIM_SECONDS_PER_FRAME / STEPS_PER_FRAME
                body1.y_position_change = body1.y_velocity * SIM_SECONDS_PER_FRAME / STEPS_PER_FRAME

        for body in bodies:
            body.x_position += body.x_position_change
            body.y_position += body.y_position_change
            body.x_position_change = 0
            body.y_position_change = 0

    # Rendering
    screen.fill(BLACK)
    for body in bodies:
        pygame.draw.circle(
            screen,
            body.color,
            (
                int(body.x_position / DISTANCE_SCALE_FACTOR + SCREEN_WIDTH / 2),
                int(body.y_position / DISTANCE_SCALE_FACTOR + SCREEN_HEIGHT / 2),
            ),
            body.radius
        )
    pygame.display.flip()

    clock.tick(FRAMES_PER_SECOND)
