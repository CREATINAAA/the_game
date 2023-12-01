#-------MAIN-----------

from module_1 import *
# Игровой цикл
clock = pygame.time.Clock()
running = True

while running:
    clock.tick(FPS)
    handle_events()
    update()
    draw()
# Выход из игры

pygame.quit()
exit()