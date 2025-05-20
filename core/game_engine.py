import pygame
from pygame.math import Vector2


class GameEngine:
    def __init__(self, config):
        pygame.init()
        self.screen = pygame.display.set_mode(config.SCREEN_SIZE)
        pygame.display.set_caption("Motion Controlled Game")
        self.clock = pygame.time.Clock()
        self.gravity = Vector2(0, 0.98)
        self.jump_force = -18
        self.ground_level = config.SCREEN_SIZE[1] - 50

        # 初始化颜色配置
        self.bg_color = (30, 30, 30)
        self.player_color = (0, 255, 128)
        self.ground_color = (64, 64, 64)

    def update(self, controls, player):
        """处理游戏逻辑更新"""
        # 处理系统事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

        # 横向移动控制
        horizontal_speed = 0
        if controls['move_left']:
            horizontal_speed = -8
        elif controls['move_right']:
            horizontal_speed = 8

        # 应用跳跃物理
        if controls['jump'] and player.on_ground:
            player.velocity.y = self.jump_force
            player.on_ground = False

        # 更新玩家速度
        player.velocity.x = horizontal_speed
        player.velocity += self.gravity

        # 限制垂直速度
        player.velocity.y = min(player.velocity.y, 20)

        # 更新玩家位置
        player.rect.x += player.velocity.x
        player.rect.y += player.velocity.y

        # 地面碰撞检测
        if player.rect.bottom >= self.ground_level:
            player.rect.bottom = self.ground_level
            player.velocity.y = 0
            player.on_ground = True

        # 屏幕边界限制
        player.rect.x = max(0, min(player.rect.x, self.screen.get_width() - player.rect.width))

        player.update_image(controls)
        player.apply_jump_scale()

        return True

    def render(self, player):
        """渲染游戏画面"""
        # 绘制背景
        self.screen.fill(self.bg_color)

        # 绘制地面
        pygame.draw.rect(self.screen, self.ground_color,
                         (0, self.ground_level,
                          self.screen.get_width(),
                          self.screen.get_height() - self.ground_level))

        # 绘制玩家
        scaled_image = player.get_scaled_image()
        image_rect = scaled_image.get_rect(center=player.rect.center)
        self.screen.blit(scaled_image, image_rect)

        # 更新显示
        pygame.display.flip()
        self.clock.tick(60)