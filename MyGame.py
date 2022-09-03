import pygame
from sys import exit
from random import randint, choice


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()  # Inherit functionalities of Sprite class
        player_walk_1 = pygame.image.load("Graphics\player_walk_1.png").convert_alpha()
        player_walk_2 = pygame.image.load("Graphics\player_walk_2.png").convert_alpha()

        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load(
            "Graphics\player_walk_1.png"
        ).convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(80, 300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound("Audio\jump_audio.wav")
        self.jump_sound.set_volume(0.5)  # 0 is mute, 1 is max volume

    def player_input(self):
        keys = pygame.key.get_pressed()  # Gets hold of all keys pressed simultaneously
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity  # Player progressively falls down faster
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):  # Function to run all processes at once
        self.player_input()
        self.apply_gravity()
        self.animation_state()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if type == "fly":  
            fly_1 = pygame.image.load(
                "Graphics\Fly1.png"                       
            ).convert_alpha()                             # Changes pixel format including per pixel alpha value
            fly_2 = pygame.image.load("Graphics\Fly2.png").convert_alpha() # Enables faster blitting
            self.frames = [fly_1, fly_2]
            y_pos = 210  # Flies fly above the ground
        else:
            snail_1 = pygame.image.load("Graphics\snail1.png").convert_alpha()
            snail_2 = pygame.image.load("Graphics\snail2.png").convert_alpha()
            self.frames = [snail_1, snail_2]
            y_pos = 300  # Snail moves on the ground

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(randint(900, 1100), y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()  # Remove sprite from all groups


def display_score():
    current_time = (
        int(pygame.time.get_ticks() / 1000) - start_time
    )  # Gives time since pygame was in initialised
    score_surf = test_font.render(f"Score: {current_time}", False, (64, 64, 64))
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)  # Draw score surface
    return current_time


def collision_sprite():  # bool indicates whether a sprite gets destroyed or not
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()  # Removes all the sprites from the group
        return False
    else:
        return True


pygame.init()  # Gets all methods defined in Pygame
screen = pygame.display.set_mode(
    (800, 400)
)  # Initialises screen of specified resolution
pygame.display.set_caption("Runner")  # Assigns Title
clock = pygame.time.Clock()  # Clock Object created to handle FPS
test_font = pygame.font.Font("Font\Pixeltype.ttf", 50)  # Text Font
game_active = False
start_time = 0
score = 0
bg_music = pygame.mixer.Sound("Audio\music.wav")
bg_music.play(loops=-1)  # loop infinitely

# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

sky_surface = pygame.image.load(
    "Graphics\sky.png"
).convert()  # Surface will have the same pixel format
ground_surface = pygame.image.load(
    "Graphics\ground.png"
).convert()  # as display surface

# Intro screen
player_stand = pygame.image.load("Graphics\player_stand.png").convert_alpha()
player_stand = pygame.transform.rotozoom(
    player_stand, 0, 2
)  # (surface, angle, scaling)
player_stand_rect = player_stand.get_rect(center=(400, 200))

game_name = test_font.render("Pixel Runner", False, (111, 196, 169))
game_name_rect = game_name.get_rect(center=(400, 80))

game_message = test_font.render("Press Space to run", False, (111, 196, 169))
game_message_rect = game_message.get_rect(center=(400, 330))

# Timer
obstacle_timer = (
    pygame.USEREVENT + 1
)  # +1 because some events are reserved for pygame itself
pygame.time.set_timer(obstacle_timer, 1500)

# Infinite game loop
while True:
    for event in pygame.event.get():  # Define individual events
        if event.type == pygame.QUIT:  # Method to exit game
            pygame.quit()
            exit()

        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(
                    Obstacle(choice(["fly", "snail", "snail", "snail"]))
                )  # 75:25 snail : fly occurrences

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)

    if game_active:
        # Lay one surface on another (Procedural execution)
        screen.blit(sky_surface, (0, 0))  # Draw sky surface
        screen.blit(ground_surface, (0, 300))  # Draw ground surface
        score = display_score()

        player.draw(screen)  # Draw player on screen
        player.update()  # Run all methods defined in the class at once

        obstacle_group.draw(screen)  # Draw obstacles on screen
        obstacle_group.update()  # Run all methods defined in the class at once

        game_active = collision_sprite()  # Collisions

    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rect)

        score_message = test_font.render(f"Your score: {score}", False, (111, 196, 169))
        score_message_rect = score_message.get_rect(center=(400, 330))
        screen.blit(game_name, game_name_rect)

        if score == 0:
            screen.blit(game_message, game_message_rect)
        else:
            screen.blit(score_message, score_message_rect)

    pygame.display.update()  # Constantly update screen with changes
    clock.tick(60)           # FPS counter for Clock object
