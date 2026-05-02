from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
ASSET_DIR = BASE_DIR / "assets" / "images"
SOUND_DIR = BASE_DIR / "assets" / "sounds"
SAVE_FILE = BASE_DIR / "save_data.json"

GAME_TITLE = "Sky Dash"

WIDTH = 432
HEIGHT = 768
FPS = 60

SKY_COLOR = (112, 197, 206)
GROUND_COLOR = (222, 216, 149)
GROUND_LINE_COLOR = (196, 178, 92)
GROUND_HEIGHT = 0

BIRD_X = 96
BIRD_RADIUS = 18
BIRD_COLLISION_WIDTH = 30
BIRD_COLLISION_HEIGHT = 26
BIRD_SIZE = (58, 42)
IMAGE_BACKGROUND_COLOR = (255, 255, 255)
IMAGE_BACKGROUND_TOLERANCE = 45
BIRD_GRAVITY = 0.45
BIRD_FLAP_STRENGTH = -8.5
BIRD_MAX_FALL_SPEED = 10
BIRD_ANIMATION_MS = 120

BIRD_FLAP_UP_VELOCITY = -5
BIRD_FLAP_MID_VELOCITY = -1
BIRD_FLAP_DOWN_VELOCITY = 3
BIRD_FALLING_VELOCITY = 7

PIPE_WIDTH = 72
PILLAR_VISUAL_WIDTH = 96
PIPE_GAP = 220
PIPE_SPEED = 3
PIPE_INTERVAL_MS = 1400
MIN_PIPE_HEIGHT = 70
PIPE_COLLISION_INSET_X = 10
PIPE_COLLISION_INSET_Y = 4
PLAYABLE_HEIGHT = HEIGHT - GROUND_HEIGHT
MAX_PIPE_TOP_HEIGHT = PLAYABLE_HEIGHT - PIPE_GAP - MIN_PIPE_HEIGHT

PILLAR_SMALL_MAX_HEIGHT = 150
PILLAR_MID_MAX_HEIGHT = 260

BIRD_IMAGES = {
    "flap_up": "bird_flap_up.png",
    "flap_mid": "bird_flap_mid.png",
    "flap_down": "bird_flap_down.png",
    "falling": "bird_falling.png",
    "falling_deep": "bird_falling_deep.png",
    "dead": "bird_dead.png",
}

PILLAR_IMAGES = {
    "small": "piller_small.png",
    "mid": "piller_mid.png",
    "tall": "piller_tall.png",
}

UI_IMAGES = {
    "background": "background.png",
    "logo": "logo_sky_dash.png",
    "play": "button_play.png",
    "retry": "button_retry.png",
    "home": "button_home.png",
    "settings": "button_settings.png",
    "exit": "button_exit.png",
    "sound_toggle": "button_sound_toggle.png",
}

BUTTON_SIZE = (240, 120)
SQUARE_BUTTON_SIZE = (92, 92)
TOGGLE_BUTTON_SIZE = (190, 95)
LOGO_SIZE = (350, 235)
PAUSE_BUTTON_SIZE = (78, 78)

SOUND_VOLUME = 0.55
SOUNDS = {
    "score": "score.wav",
    "crash": "crash.wav",
    "restart": "restart.wav",
}

if MAX_PIPE_TOP_HEIGHT < MIN_PIPE_HEIGHT:
    raise ValueError(
        "Pipe settings leave no room for a valid gap. "
        "Reduce PIPE_GAP/MIN_PIPE_HEIGHT or increase HEIGHT/GROUND_HEIGHT."
    )
