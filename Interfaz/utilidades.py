import pygame

def scale_image(img, factor):
    size = round(img.get_width()*factor), round(img.get_height()*factor)
    return pygame.transform.scale(img, size)

def blit_rotate_center(win, image, top_Left, angle): # Rotar desde el centro
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(topleft= top_Left).center)
    win.blit(rotated_image, new_rect.topleft)

