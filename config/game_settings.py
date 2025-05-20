# game_settings.py
class GameConfig:
    SCREEN_SIZE = (800, 600)
    PLAYER_SIZE = 40
    GRAVITY = 1
    JUMP_FORCE = -20
    FPS = 30
class AnimationConfig:
    IDLE_FRAMES = 4
    RUN_FRAMES = 6
    FRAME_DURATION = 100  # 每帧显示时间(ms)
