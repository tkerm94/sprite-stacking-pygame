import sys

from characters import Player
from menus import *
from PIL import Image, ImageFilter

from cache import Cache
from scene import Scene
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
        self.in_game = False
        self.won = False
        self.lost = False
        self.music_name = "main_theme"
        self.loading_to = ""
        self.icons = dict()
        for key, val in ICONS.items():
            img = pygame.image.load(val)
            img = pygame.transform.scale(img, vec2(img.get_size()) * 2)
            self.icons[key] = img
        self.font = pygame.font.Font(pygame.font.get_default_font(), 32)

    def start_game(self, loading=False):
        self.main_group = pygame.sprite.LayeredUpdates()
        self.collision_group = pygame.sprite.Group()
        self.coins_level = 0
        self.coins_level_collected = 0
        self.coins_collected = 0
        self.enemies_killed = 0
        self.bullets_shot = 0
        self.boxes_destroyed = 0
        self.hp_healed = 0
        self.level_number = 1
        self.level_completed = False
        self.cache = Cache()
        self.player = Player(self, PLAYER_HP)
        if loading:
            if pygame.mixer.music.get_busy() and self.music_name != "main_theme":
                pygame.mixer.music.fadeout(100)
                pygame.mixer.music.load(Path("assets/sounds/theme_main.wav"))
                pygame.mixer.music.play(-1, fade_ms=100)
            save = SAVES[self.loading_to[:-4]]
            with open(save, "r") as file:
                for line in file.readlines():
                    key, val = line.split()
                    if key == "hp":
                        self.player.hp = int(val)
                        self.player.hp_on_start = int(val)
                    elif key == "level_number":
                        self.level_number = int(val)
                    elif key == "coins_collected":
                        self.coins_collected = int(val)
                    elif key == "enemies_killed":
                        self.enemies_killed = int(val)
                    elif key == "bullets_shot":
                        self.bullets_shot = int(val)
                    elif key == "boxes_destroyed":
                        self.boxes_destroyed = int(val)
                    elif key == "hp_healed":
                        self.hp_healed = int(val)
                    else:
                        print("corrupted save file")
                        pygame.quit()
                        sys.exit(1)
        self.to_save = {
            "hp": self.player.hp_on_start,
            "level_number": self.level_number,
            "coins_collected": self.coins_collected,
            "enemies_killed": self.enemies_killed,
            "bullets_shot": self.bullets_shot,
            "boxes_destroyed": self.boxes_destroyed,
            "hp_healed": self.hp_healed,
        }
        self.loading_to = ""
        self.scene = Scene(self)

    def update(self):
        self.scene.update()
        self.main_group.update()

    def draw(self):
        self.screen.fill(BG_COLOR)
        self.main_group.draw(self.screen)

    def draw_ui(self):
        icon = self.icons["health"]
        pygame.draw.rect(
            self.screen,
            MENU_COLOR,
            (0, 0, icon.get_width() + 160, icon.get_height() * 2 + 40),
            border_bottom_right_radius=5,
        )
        pygame.draw.rect(
            self.screen,
            MENU_ALT_COLOR,
            (-2, -2, icon.get_width() + 164, icon.get_height() * 2 + 44),
            border_bottom_right_radius=5,
            width=2,
        )
        pygame.draw.rect(
            self.screen,
            MENU_COLOR,
            (
                H_WIDTH - icon.get_width() - 30,
                0,
                icon.get_width() * 2 + 60,
                icon.get_height() + 40,
            ),
            border_bottom_right_radius=5,
            border_bottom_left_radius=5,
        )
        pygame.draw.rect(
            self.screen,
            MENU_ALT_COLOR,
            (
                H_WIDTH - icon.get_width() - 32,
                -2,
                icon.get_width() * 2 + 64,
                icon.get_height() + 44,
            ),
            border_bottom_right_radius=5,
            border_bottom_left_radius=5,
            width=2,
        )
        pygame.draw.rect(
            self.screen,
            MENU_COLOR,
            (
                WIDTH - icon.get_width() - 160,
                0,
                icon.get_width() + 160,
                icon.get_height() * 2 + 40,
            ),
            border_bottom_left_radius=5,
        )
        pygame.draw.rect(
            self.screen,
            MENU_ALT_COLOR,
            (
                WIDTH - icon.get_width() - 162,
                -2,
                icon.get_width() + 164,
                icon.get_height() * 2 + 44,
            ),
            border_bottom_left_radius=5,
            width=2,
        )
        rect = pygame.Rect(40 + icon.get_width(), 33, 100, icon.get_height() - 20)
        slider_rect = pygame.Rect(
            42 + icon.get_width(),
            35,
            96 / self.player.max_hp * self.player.hp,
            icon.get_height() - 24,
        )
        self.screen.blit(icon, (20, 20))
        pygame.draw.rect(self.screen, MENU_ALT_COLOR, rect, border_radius=5)
        pygame.draw.rect(self.screen, "red", slider_rect, border_radius=5)
        icon = self.icons["coins"]
        rect = pygame.Rect(
            40 + icon.get_width(), icon.get_height() + 31, 100, icon.get_height() - 20
        )
        if self.coins_level:
            slider_rect = pygame.Rect(
                42 + icon.get_width(),
                icon.get_height() + 33,
                96 / self.coins_level * self.coins_level_collected,
                icon.get_height() - 24,
            )
        else:
            slider_rect = pygame.Rect(
                42 + icon.get_width(), icon.get_height() + 33, 0, icon.get_height() - 24
            )
        self.screen.blit(icon, (20, icon.get_height() + 20))
        pygame.draw.rect(self.screen, MENU_ALT_COLOR, rect, border_radius=5)
        pygame.draw.rect(self.screen, "yellow", slider_rect, border_radius=5)
        icon = self.icons["level"]
        self.screen.blit(icon, (H_WIDTH - icon.get_width() - 10, 20))
        font = pygame.font.Font(pygame.font.get_default_font(), 50)
        text = font.render(str(self.level_number), True, MENU_ALT_COLOR)
        self.screen.blit(
            text,
            text.get_rect(
                center=pygame.Rect(
                    H_WIDTH, 0, icon.get_width() + 30, icon.get_height() + 45
                ).center
            ),
        )
        icon = self.icons["reloading"]
        rect = pygame.Rect(WIDTH - 120, 33, 100, icon.get_height() - 20)
        slider_rect = pygame.Rect(
            WIDTH - 118, 35, 96 / 20 * self.player.reload_cycles, icon.get_height() - 24
        )
        self.screen.blit(icon, (WIDTH - icon.get_width() - 140, 20))
        pygame.draw.rect(self.screen, MENU_ALT_COLOR, rect, border_radius=5)
        pygame.draw.rect(self.screen, "blue", slider_rect, border_radius=5)
        icon = self.icons["sprinting"]
        rect = pygame.Rect(
            WIDTH - 120, icon.get_height() + 36, 100, icon.get_height() - 20
        )
        slider_rect = pygame.Rect(
            WIDTH - 118,
            icon.get_height() + 38,
            96 / 30 * self.player.sprint_cycles,
            icon.get_height() - 24,
        )
        self.screen.blit(icon, (WIDTH - icon.get_width() - 140, icon.get_height() + 23))
        pygame.draw.rect(self.screen, MENU_ALT_COLOR, rect, border_radius=5)
        pygame.draw.rect(self.screen, "green", slider_rect, border_radius=5)

    def check_events(self):
        self.anim_trigger = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == self.anim_event:
                self.anim_trigger = True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.on_pause()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    self.player.shoot()

    def get_time(self):
        self.time = pygame.time.get_ticks() * 0.001

    def on_pause(self):
        pygame.mouse.set_visible(1)
        for _, sound in SOUNDS.items():
            sound.stop()
        for _, channel in CHANNELS.items():
            channel.pause()
        menu = PauseMenu(self.screen, self.font, self)
        self.draw()
        screenshot = pygame.image.tostring(self.screen, "RGBA")
        pic = Image.frombytes("RGBA", self.screen.get_size(), screenshot).filter(
            ImageFilter.GaussianBlur(radius=10)
        )
        pic = pygame.image.fromstring(
            pic.tobytes("raw", "RGBA"), self.screen.get_size(), "RGBA"
        )
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    ok, name = menu.check_click(event.pos)  # type: ignore
                    if ok and name == "resume":
                        break
                    elif ok and name == "ok":
                        self.in_game = False
                        break
                    elif ok:
                        self.loading_to = name
                        break
                    elif name[-2:] == "_s":
                        name = name[:-2]
                        SAVES[name] = Path(f"data/saves/{name}.txt")
                        with open(SAVES[name], "w") as file:
                            for key, val in self.to_save.items():
                                file.write(f"{key} {val}\n")
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    break
                elif event.type == pygame.KEYDOWN and menu.active_input:
                    menu.process_input(event)
                elif event.type == self.anim_event:
                    menu.anim_trigger = True
            else:
                self.screen.blit(pic, (0, 0))
                menu.render(pygame.mouse.get_pos(), outline=True)
                self.draw_ui()
                pygame.display.flip()
                self.clock.tick(self.fps)
                continue
            break
        for _, channel in CHANNELS.items():
            channel.unpause()
        pygame.mouse.set_visible(0)

    def main_menu(self):
        pygame.mouse.set_visible(1)
        for _, sound in SOUNDS.items():
            sound.stop()
        for _, channel in CHANNELS.items():
            channel.stop()
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.fadeout(100)
        pygame.mixer.music.load(Path("assets/sounds/theme_main.wav"))
        pygame.mixer.music.play(-1, fade_ms=100)
        self.music_name = "main_theme"
        menu = MainMenu(self.screen, self.font)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    ok, name = menu.check_click(event.pos)  # type: ignore
                    if ok and name == "new game":
                        break
                    elif ok and name == "ok":
                        pygame.quit()
                        sys.exit()
                    elif ok:
                        self.loading_to = name
                        break
                elif event.type == self.anim_event:
                    menu.anim_trigger = True
            else:
                self.screen.fill("black")
                menu.render(pygame.mouse.get_pos())
                pygame.display.flip()
                self.clock.tick(self.fps)
                continue
            break
        pygame.mouse.set_visible(0)

    def win_menu(self):
        pygame.mouse.set_visible(1)
        for _, sound in SOUNDS.items():
            sound.stop()
        for _, channel in CHANNELS.items():
            channel.stop()
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.fadeout(100)
        pygame.mixer.music.load(Path("assets/sounds/theme_win.wav"))
        pygame.mixer.music.play(-1, fade_ms=100)
        self.music_name = "win_theme"
        menu = WinMenu(self.screen, self.font, self)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    ok, _ = menu.check_click(event.pos)
                    if ok:
                        self.in_game = False
                        break
                elif event.type == self.anim_event:
                    menu.anim_trigger = True
            else:
                self.screen.fill("black")
                menu.render(pygame.mouse.get_pos())
                pygame.display.flip()
                self.clock.tick(self.fps)
                continue
            break
        pygame.mouse.set_visible(0)

    def lose_menu(self):
        pygame.mouse.set_visible(1)
        for _, sound in SOUNDS.items():
            sound.stop()
        for _, channel in CHANNELS.items():
            channel.stop()
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.fadeout(100)
        pygame.mixer.music.load(Path("assets/sounds/theme_lose.wav"))
        pygame.mixer.music.play(-1, fade_ms=100)
        self.music_name = "lose_menu"
        menu = LoseMenu(self.screen, self.font)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    ok, name = menu.check_click(event.pos)  # type: ignore
                    if ok and not name:
                        self.in_game = False
                        break
                    elif ok:
                        self.loading_to = name
                        break
                elif event.type == self.anim_event:
                    menu.anim_trigger = True
            else:
                self.screen.fill("black")
                menu.render(pygame.mouse.get_pos())
                pygame.display.flip()
                self.clock.tick(self.fps)
                continue
            break
        pygame.mouse.set_visible(0)

    def loading_screen(self):
        self.screen.fill("black")
        big_font = pygame.font.Font(pygame.font.get_default_font(), 85)
        text = big_font.render("Loading...", True, "white")
        text_rect = text.get_rect(center=self.screen.get_rect().center)
        self.screen.blit(text, text_rect)
        pygame.display.flip()

    def run(self):
        while True:
            if not self.in_game:
                self.main_menu()
                self.loading_screen()
                if self.loading_to:
                    self.start_game(loading=True)
                else:
                    self.start_game()
                self.in_game = True
            if self.loading_to:
                self.loading_screen()
                self.start_game(loading=True)
                continue
            if self.won:
                self.won = False
                self.win_menu()
                continue
            if self.lost:
                self.lost = False
                self.lose_menu()
                continue
            self.check_events()
            if not self.in_game:
                continue
            self.get_time()
            self.update()
            self.draw()
            self.draw_ui()
            pygame.display.flip()
            self.clock.tick(self.fps)


if __name__ == "__main__":
    game = Game(1000, 120)
    game.run()
