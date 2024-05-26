import pygame
import random
import math

WIDTH, HEIGHT = 800, 600
NUM_BOIDS = 100  # Số boid
MAX_SPEED = 6
MAX_FORCE = 0.3

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flocking Simulation")

class Boid:
    def __init__(self):
        self.position = pygame.math.Vector2(random.uniform(0, WIDTH), random.uniform(0, HEIGHT))
        self.velocity = pygame.math.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
        self.velocity.scale_to_length(random.uniform(1, MAX_SPEED))
        self.acceleration = pygame.math.Vector2(0, 0)

    def update(self):
        self.velocity += self.acceleration
        if self.velocity.length() > MAX_SPEED:
            self.velocity.scale_to_length(MAX_SPEED)
        self.position += self.velocity
        self.acceleration = pygame.math.Vector2(0, 0)

    def apply_force(self, force):
        self.acceleration += force

    def edges(self):
        if self.position.x > WIDTH:
            self.position.x = 0
        elif self.position.x < 0:
            self.position.x = WIDTH
        if self.position.y > HEIGHT:
            self.position.y = 0
        elif self.position.y < 0:
            self.position.y = HEIGHT

    def show(self):
        angle = math.atan2(self.velocity.y, self.velocity.x)
        points = [
            (self.position.x + 5 * math.cos(angle), self.position.y + 5 * math.sin(angle)),  # Reduced size
            (self.position.x + 5 * math.cos(angle + 2.5), self.position.y + 5 * math.sin(angle + 2.5)),
            (self.position.x + 5 * math.cos(angle - 2.5), self.position.y + 5 * math.sin(angle - 2.5)),
        ]
        pygame.draw.polygon(screen, (255, 255, 255), points)

    def flock(self, boids, mouse_pos):
        perception_radius = 50
        separation_radius = 25
        alignment = pygame.math.Vector2(0, 0)
        cohesion = pygame.math.Vector2(0, 0)
        separation = pygame.math.Vector2(0, 0)
        total = 0
        for other in boids:
            if other == self:
                continue
            distance = self.position.distance_to(other.position)
            if distance < perception_radius:
                alignment += other.velocity
                cohesion += other.position
                total += 1
                if distance < separation_radius:
                    diff = self.position - other.position
                    diff /= distance
                    separation += diff
        if total > 0:
            alignment /= total
            alignment.scale_to_length(MAX_SPEED)
            alignment -= self.velocity
            if alignment.length() > MAX_FORCE:
                alignment.scale_to_length(MAX_FORCE)

            cohesion /= total
            cohesion -= self.position
            cohesion.scale_to_length(MAX_SPEED)
            cohesion -= self.velocity
            if cohesion.length() > MAX_FORCE:
                cohesion.scale_to_length(MAX_FORCE)

            separation /= total
            if separation.length() > MAX_FORCE:
                separation.scale_to_length(MAX_FORCE)

        # Con trỏ chuột
        mouse_force = (mouse_pos - self.position)
        if mouse_force.length() > 0:
            mouse_force.scale_to_length(MAX_SPEED)
            mouse_force -= self.velocity
            if mouse_force.length() > MAX_FORCE:
                mouse_force.scale_to_length(MAX_FORCE)

        self.apply_force(alignment)
        self.apply_force(cohesion)
        self.apply_force(separation)
        self.apply_force(mouse_force)

boids = [Boid() for _ in range(NUM_BOIDS)]

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    mouse_pos = pygame.math.Vector2(pygame.mouse.get_pos())

    for boid in boids:
        boid.edges()
        boid.flock(boids, mouse_pos)
        boid.update()
        boid.show()

    pygame.display.flip()
    pygame.time.delay(30)

pygame.quit()
