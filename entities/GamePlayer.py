import pygame

class GamePlayer:
    def __init__(self, start_pos, size=40):
        self.rect = pygame.Rect(start_pos[0], start_pos[1], size, size)
        self.velocity = pygame.math.Vector2(0, 0)
        self.on_ground = True
        self.size = size

    def reset(self, pos):
        """重置玩家状态"""
        self.rect.topleft = pos
        self.velocity = pygame.math.Vector2(0, 0)
        self.on_ground = True