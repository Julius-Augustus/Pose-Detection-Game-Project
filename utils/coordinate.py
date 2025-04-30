# coordinate.py
class CoordinateTransformer:
    def __init__(self, camera_res, screen_res):
        self.camera_w, self.camera_h = camera_res
        self.screen_w, self.screen_h = screen_res
        self.aspect_ratio = camera_res[0] / camera_res[1]  # 保持宽高比

    def camera_to_screen(self, x, y):
        """将摄像头坐标系转换为屏幕坐标系（保持比例适配）"""
        # 标准化到0-1范围
        normalized_x = x / self.camera_w
        normalized_y = y / self.camera_h

        # 计算适配后的有效显示区域
        if (self.screen_w / self.screen_h) > self.aspect_ratio:
            # 以高度为基准适配
            display_width = self.screen_h * self.aspect_ratio
            display_height = self.screen_h
        else:
            # 以宽度为基准适配
            display_width = self.screen_w
            display_height = self.screen_w / self.aspect_ratio

        # 转换为屏幕坐标（居中显示）
        screen_x = (self.screen_w - display_width) / 2 + normalized_x * display_width
        screen_y = (self.screen_h - display_height) / 2 + normalized_y * display_height

        return int(screen_x), int(screen_y)