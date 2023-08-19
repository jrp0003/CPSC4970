import pygame
import sys
import boo_blaster_level_2
from game_objects import Background, Player, Ghost, wait_for_key


def display_instructions(screen):
    font = pygame.font.Font(None, 36)
    text1 = font.render("Welcome to Boo Blaster!", True, (255, 255, 255))
    text2 = font.render("Use arrow keys to move. Press Spacebar to use flashlight.", True, (255, 255, 255))
    text3 = font.render("Blast all the ghosts with the flashlight and reach the end to win!", True, (255, 255, 255))
    text4 = font.render("Press Enter to start Level 1.", True, (255, 255, 255))

    screen.blit(text1, (50, 50))
    screen.blit(text2, (50, 100))
    screen.blit(text3, (50, 150))
    screen.blit(text4, (50, 200))
    pygame.display.flip()
    wait_for_key()  # Wait for Enter key press to start the game


def display_you_died(screen):
    font = pygame.font.Font(None, 36)
    text = font.render("You died. Start over.", True, (255, 0, 0))
    screen.blit(text, (50, 250))
    pygame.display.flip()

    pygame.time.delay(2000)  # Delay for 2 seconds before restarting the level


def display_level_completed(screen):
    font = pygame.font.Font(None, 36)
    text = font.render("Level 1 completed! Press Enter to start Level 2.", True, (255, 255, 255))
    screen.blit(text, (50, 250))
    pygame.display.flip()
    wait_for_key()


def main():
    pygame.init()
    pygame.mixer.init()  # Initialize the mixer
    pygame.mixer.music.load("media/background_music.mp3")  # Load music
    sound_effect = pygame.mixer.Sound("media/blast.wav")  # Load sound effect
    screen_width = 900
    screen_height = 768
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Boo Blaster Level 1")
    clock = pygame.time.Clock()

    # Display instructions
    display_instructions(screen)
    pygame.mixer.music.play(loops=-2)  # Play the music

    # Initialize game objects for level 1
    background = Background("media/haunted_cemetery2.jpg")
    player = Player(screen_width=screen_width, screen_height=screen_height)
    ghosts = [
        Ghost(),
        Ghost(pos=(1200, 800), speed=1),
        Ghost(pos=(500, 500), speed=2)
    ]
    flashlight_beam = pygame.image.load("media/flashlight_beam.png")
    flashlight_beam_offset = (75, -115)

    game_over = False
    level_completed = False

    # Variables for scrolling
    scroll_speed = 2
    scroll_x = 0

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        player.update(keys)

        screen.fill((0, 0, 0))

        # Update background scroll
        if player.pos[0] > screen_width / 2:
            scroll_x -= scroll_speed

        # Ensure the background stops at the end
        if scroll_x < -background.rect.width + screen_width:
            scroll_x = -background.rect.width + screen_width

        screen.blit(background.image, (scroll_x, 0))
        player.draw(screen)

        all_ghosts_dead = all(ghost.is_dead for ghost in ghosts)

        for ghost in ghosts:
            if not ghost.is_dead:
                ghost.update(player.pos, (player.pos[0] + flashlight_beam_offset[0], player.pos[1]
                                          + flashlight_beam_offset[1]), flashlight_beam)
            ghost.draw(screen)  # Draw the ghost

            # Check collision with player
            if (ghost.pos[0] < player.pos[0] < ghost.pos[0] + ghost.frame_width and
                    ghost.pos[1] < player.pos[1] < ghost.pos[1] + ghost.frame_height):
                # Player is hit by ghost, restart
                game_over = True
                display_you_died(screen)
                main()

            # Check collision with flashlight beam
            if keys[pygame.K_SPACE]:
                beam_rect = pygame.Rect(player.pos[0] + flashlight_beam_offset[0], player.pos[1]
                                        + flashlight_beam_offset[1], flashlight_beam.get_width(),
                                        flashlight_beam.get_height())
                ghost_rect = pygame.Rect(ghost.pos[0], ghost.pos[1], ghost.frame_width, ghost.frame_height)
                if beam_rect.colliderect(ghost_rect):
                    ghost.is_hit_by_flashlight = True
                    sound_effect.play()  # Play the sound effect

        if keys[pygame.K_SPACE]:
            screen.blit(flashlight_beam, (player.pos[0] + flashlight_beam_offset[0], player.pos[1]
                                          + flashlight_beam_offset[1]))

        if all_ghosts_dead and player.pos[0] >= 900 and not level_completed:
            display_level_completed(screen)
            level_completed = True

            # Start level 2
            if level_completed:
                pygame.time.delay(1000)
                boo_blaster_level_2.main()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
