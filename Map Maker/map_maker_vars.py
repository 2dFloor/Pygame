import pygame



screen_width = 1000
screen_height = 750
clock = pygame.time.Clock()


mouse_positions = []
mouse_difference = (0,0)
mouse_adjusted_x = 0
mouse_adjusted_y = 0

background = pygame.sprite.Group()

render_group = pygame.sprite.Group()