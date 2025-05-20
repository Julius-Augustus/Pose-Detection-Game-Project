import cv2
import pygame  # 假设需要导入 pygame
import time  # 用于计算 FPS

# 修复后的导入语句
from config.game_settings import GameConfig
from config.detection_params import DetectionConfig
from core.pose_detector import PoseDetector
from core.gesture_controller import GestureInterpreter
from core.game_engine import GameEngine
from entities.GamePlayer import GamePlayer 
from utils.visualizer import DetectionVisualizer  # 修改导入路径

def main():
    # 初始化系统
    game_config = GameConfig()
    detection_config = DetectionConfig()

    # 创建核心组件
    detector = PoseDetector(detection_config)
    interpreter = GestureInterpreter(game_config.SCREEN_SIZE)  # 这里传入屏幕尺寸
    engine = GameEngine(game_config)

    # 定义玩家的起始位置
    start_pos = (100, 100)  # 这里可以根据需求调整起始位置
    player = GamePlayer(start_pos, game_config.PLAYER_SIZE)

    # 视频采集
    cap = cv2.VideoCapture(detection_config.CAMERA_INDEX)

    prev_time = 0  # 用于计算 FPS

    while True:
        # 处理输入
        ret, frame = cap.read()
        if not ret:
            break

        # 检测流程
        results = detector.detect(frame)
        landmarks = []
        if results.pose_landmarks:
            landmarks = list(results.pose_landmarks.landmark)  # 将 RepeatedCompositeContainer 转换为列表
        controls = interpreter.interpret(landmarks)

        # 绘制骨骼关键点和连接线
        if results.pose_landmarks:
            frame = DetectionVisualizer.draw_landmarks(frame, results.pose_landmarks.landmark)

        # 计算 FPS
        current_time = time.time()
        fps = 1 / (current_time - prev_time)
        prev_time = current_time

        # 在画面上叠加调试信息
        frame = DetectionVisualizer.draw_debug_info(frame, controls, fps)

        # 游戏循环
        engine.update(controls, player)
        engine.render(player)

        # 显示处理后的帧
        cv2.imshow('Motion Controlled Game', frame)

        # 退出检测
        if cv2.waitKey(1) == ord('q'):
            break

    # 资源释放
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()