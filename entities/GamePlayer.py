import pygame


class GamePlayer:
    def __init__(self, start_pos, size=40):
        # 加载不同状态的图片
        self.stand_image = pygame.image.load(r'C:\Users\123\PycharmProjects\Final_exam\OIP-C.jpg')
        self.move_left_image = pygame.image.load(r'C:\Users\123\PycharmProjects\Final_exam\OIP-C.jpg')
        self.move_right_image = pygame.image.load(r'C:\Users\123\PycharmProjects\Final_exam\OIP-C.jpg')
        self.jump_image = pygame.image.load(r'C:\Users\123\PycharmProjects\Final_exam\OIP-C.jpg')

        self.rect = pygame.Rect(start_pos[0], start_pos[1], size, size)
        self.velocity = pygame.math.Vector2(0, 0)
        self.on_ground = True
        self.size = size
        self.current_image = self.stand_image
        self.jump_scale = 1.0  # 跳跃缩放比例

    def reset(self, pos):
        """重置玩家状态"""
        self.rect.topleft = pos
        self.velocity = pygame.math.Vector2(0, 0)
        self.on_ground = True
        self.current_image = self.stand_image
        self.jump_scale = 1.0

    def update_image(self, controls):
        if controls['move_left']:
            self.current_image = self.move_left_image
        elif controls['move_right']:
            self.current_image = self.move_right_image
        elif controls['jump']:
            self.current_image = self.jump_image
        else:
            self.current_image = self.stand_image

    def apply_jump_scale(self):
        if not self.on_ground:
            # 根据跳跃状态调整缩放比例，这里简单线性缩放，可按需调整
            if self.velocity.y < 0:
                self.jump_scale = 1.2
            elif self.velocity.y > 0:
                self.jump_scale = 0.8
        else:
            self.jump_scale = 1.0

    def get_scaled_image(self):
        scaled_width = int(self.current_image.get_width() * self.jump_scale)
        scaled_height = int(self.current_image.get_height() * self.jump_scale)
        return pygame.transform.scale(self.current_image, (scaled_width, scaled_height))