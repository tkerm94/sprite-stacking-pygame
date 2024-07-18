from pathlib import Path

import pygame

pygame.init()
vec2 = pygame.math.Vector2
info = pygame.display.Info()
RES = WIDTH, HEIGHT = vec2(info.current_w, info.current_h)
CENTER = H_WIDTH, H_HEIGHT = RES // 2
NUM_ANGLES = 180

ENTITY_SPRITE_ATTRS = {
    "player": {
        "walking": Path("assets/entities/player/player_walking.png"),
        "standing": Path("assets/entities/player/player_standing.png"),
        "dying": Path("assets/entities/player/player_dying.png"),
        "attacking": Path("assets/entities/player/player_attacking.png"),
        "damaging": Path("assets/entities/player/player_damaging.png"),
        "sprinting": Path("assets/entities/player/player_sprinting.png"),
        "mask_path": Path("assets/entities/player/mask.png"),
        "num_layers": 4,
        "scale": 8,
        "y_offset": 0,
    },
    "enemy": {
        "walking": Path("assets/entities/enemy/enemy_walking.png"),
        "standing": Path("assets/entities/enemy/enemy_standing.png"),
        "dying": Path("assets/entities/enemy/enemy_dying.png"),
        "attacking": Path("assets/entities/enemy/enemy_attacking.png"),
        "damaging": Path("assets/entities/enemy/enemy_damaging.png"),
        "mask_path": Path("assets/entities/enemy/mask.png"),
        "num_layers": 4,
        "scale": 8,
        "y_offset": 0,
    },
    "explosion": {
        "num_layers": 7,
        "scale": 1,
        "path": Path("assets/entities/explosion/explosion.png"),
        "y_offset": 50,
    },
    "bullet": {
        "num_layers": 1,
        "scale": 0.4,
        "path": Path("assets/entities/bullet/bullet.png"),
        "y_offset": 50,
    },
    "door": {
        "num_layers": 1,
        "scale": 4,
        "path": Path("assets/entities/door/door_closed.png"),
        "alt": Path("assets/entities/door/door_open.png"),
        "mask_path": Path("assets/entities/door/mask.png"),
        "y_offset": -30,
    },
}
# сложенные спрайты
STACKED_SPRITE_ATTRS = {
    "coin": {
        "path": Path("assets/stacked_sprites/coin.png"),
        "num_layers": 18,
        "scale": 5,
        "y_offset": 0,
    },
    "medkit": {
        "path": Path("assets/stacked_sprites/medkit.png"),
        "num_layers": 24,
        "scale": 3.5,
        "y_offset": 0,
    },
    "box": {
        "path": Path("assets/stacked_sprites/box.png"),
        "num_layers": 12,
        "scale": 8,
        "y_offset": 10,
    },
    "grass": {
        "path": Path("assets/stacked_sprites/grass.png"),
        "num_layers": 12,
        "scale": 7,
        "y_offset": 20,
        "outline": False,
    },
    "tree": {
        "path": Path("assets/stacked_sprites/tree.png"),
        "num_layers": 43,
        "scale": 8,
        "y_offset": -130,
        "transparency": True,
        "mask_layer": 3,
    },
    "wall": {
        "path": Path("assets/stacked_sprites/wall.png"),
        "num_layers": 21,
        "scale": 10,
        "y_offset": 10,
    },
    "tower": {
        "path": Path("assets/stacked_sprites/tower.png"),
        "num_layers": 21,
        "scale": 11,
        "y_offset": 10,
    },
}
