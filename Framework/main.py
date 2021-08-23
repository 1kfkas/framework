import sys, os, pygame, subprocess
from pygame.locals import *

pygame.init()
pygame.display.init()

display = pygame.display.set_mode((800, 600))

mp3 = './MP3/mp3_player.py';

if sys.platform.startswith('win32'):
    mp3 = '.\MP3\mp3_player.py';

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                subprocess.run(['python3', mp3], check=True);

    display.fill((0, 255, 255))

    pygame.display.flip();
