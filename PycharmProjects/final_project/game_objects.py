import pygame
import math
import random
from pygame.sprite import Sprite


# Define the Background class
class Background(Sprite):
    def __init__(self, image_path):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()

    def update(self, player_pos):
        # Update background scroll based on player position
        if player_pos[0] > 400 and self.rect.x > -self.rect.width:
            self.rect.x -= player_pos[0] - 400

    def draw(self, screen):
        # Draw the background image on the screen
        screen.blit(self.image, self.rect)

    def reset_scroll(self):
        # Reset the background scroll position
        self.rect.x = 0


# Define the Player class
class Player(Sprite):
    def __init__(self, pos=(10, 630), walking_speed=1.5, screen_width=900, screen_height=800):
        super().__init__()
        self.pos = list(pos)
        self.prev_pos = self.pos.copy()
        self.walking_speed = walking_speed
        self.is_walking = False
        self.walking_index = 0
        self.walking_animation_counter = 0
        self.stop_image = pygame.image.load("media/man_walk4.png")
        self.walk_images = [
            pygame.image.load("media/man_walk1.png"),
            pygame.image.load("media/man_walk2.png"),
            pygame.image.load("media/man_walk3.png"),
            pygame.image.load("media/man_walk4.png")
        ]
        self.image = self.stop_image
        self.screen_width = screen_width
        self.screen_height = screen_height

    def update(self, keys):
        # Update player position based on key inputs
        self.prev_pos = self.pos.copy()
        if keys[pygame.K_LEFT]:
            self.pos[0] -= self.walking_speed
            self.is_walking = True
        elif keys[pygame.K_RIGHT]:
            self.pos[0] += self.walking_speed
            self.is_walking = True
        elif keys[pygame.K_UP]:
            self.pos[1] -= self.walking_speed
            self.is_walking = True
        elif keys[pygame.K_DOWN]:
            self.pos[1] += self.walking_speed
            self.is_walking = True
        else:
            self.is_walking = False

        # Limit player's position to stay within the screen boundaries
        self.pos[0] = max(0, min(self.pos[0], self.screen_width))

        if self.pos == self.prev_pos:
            self.is_walking = False

        # Update walking animation
        if self.is_walking:
            self.walking_animation_counter += 1
            if self.walking_animation_counter >= 5:
                self.walking_animation_counter = 0
                self.walking_index = (self.walking_index + 1) % len(self.walk_images)
            self.image = self.walk_images[self.walking_index]
        else:
            self.image = self.stop_image

    def draw(self, screen):
        # Draw the player on the screen
        screen.blit(self.image, self.pos)


# Define the Ghost class
class Ghost(Sprite):
    def __init__(self, pos=(2000, 100), speed=5, sheet="media/ghost_sheet.png", death_sheet="media/ghost_death.png"):
        super().__init__()
        self.pos = list(pos)
        self.starting_pos = list(pos)  # Store starting position for death animation
        self.speed = speed
        self.sheet = pygame.image.load(sheet)
        self.death_sheet = pygame.image.load(death_sheet)
        self.frame_width = 32
        self.frame_height = 32
        self.frames_per_row = 4
        self.frame_rects = [
            pygame.Rect((i % self.frames_per_row) * self.frame_width, (i // self.frames_per_row)
                        * self.frame_height, self.frame_width, self.frame_height) for i in range(8)
        ]
        self.current_frame = 0
        self.frame_counter = 0
        self.animation_speed = 2
        self.is_dead = False
        self.is_hit_by_flashlight = False

    def update(self, target_pos=None, flashlight_pos=None, flashlight_beam=None):
        # Update ghost movement or death animation
        if not self.is_hit_by_flashlight:
            if target_pos is None:
                # Generate random movement for the floating ghost
                direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
                self.pos[0] += direction[0] * self.speed
                self.pos[1] += direction[1] * self.speed
            else:
                # Update method for the following ghosts
                direction_x = target_pos[0] - self.pos[0]
                direction_y = target_pos[1] - self.pos[1]
                length = math.sqrt(direction_x ** 2 + direction_y ** 2)
                if length != 0:
                    direction_x /= length
                    direction_y /= length
                self.pos[0] += direction_x * self.speed
                self.pos[1] += direction_y * self.speed
        else:
            # Ghost is hit and dying, play death animation
            self.frame_counter += 1
            if self.frame_counter >= self.animation_speed * 2:
                self.frame_counter = 0
                self.current_frame = (self.current_frame + 1) % len(self.frame_rects)
                self.pos[1] -= self.speed
                if self.current_frame == 0:
                    self.is_dead = True
                    self.is_hit_by_flashlight = False

    def draw(self, screen):
        # Draw the ghost on the screen
        if not self.is_dead:
            current_frame_rect = self.frame_rects[self.current_frame]
            if self.is_hit_by_flashlight:
                screen.blit(self.death_sheet, self.pos, current_frame_rect)
            else:
                screen.blit(self.sheet, self.pos, current_frame_rect)


# Define the function to make user hit return before starting level 2
def wait_for_key(key=pygame.K_RETURN):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == key:
                return
