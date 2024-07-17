import sys

from settings import *


class Game:
    def __init__(self, speed, fps):
        pygame.mouse.set_visible(0)
        self.screen = pygame.display.set_mode(RES, pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.time = 0
        self.speed = speed / fps
        self.anim_trigger = False
        self.anim_event = pygame.USEREVENT
        pygame.time.set_timer(self.anim_event, 100)

    def check_events(self):
        self.anim_trigger = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == self.anim_event:
                self.anim_trigger = True

    def run(self):
        while True:
            self.check_events()
            pygame.display.flip()
            self.clock.tick(self.fps)


if __name__ == "__main__":
    game = Game(1000, 120)
    game.run()
