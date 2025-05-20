from flask import Flask, Response, render_template, request, jsonify
import cv2
import time
from config.game_settings import GameConfig
from config.detection_params import DetectionConfig
from core.pose_detector import PoseDetector
from core.gesture_controller import GestureInterpreter
from core.game_engine import GameEngine
from entities.GamePlayer import GamePlayer
from utils.visualizer import DetectionVisualizer

app = Flask(__name__)

# 控制游戏状态的全局变量
game_state = {
    "is_running": False
}


def generate_frames():
    # 初始化系统
    game_config = GameConfig()
    detection_config = DetectionConfig()

    # 创建核心组件
    detector = PoseDetector(detection_config)
    interpreter = GestureInterpreter(game_config.SCREEN_SIZE)
    engine = GameEngine(game_config)

    # 定义玩家的起始位置
    start_pos = (100, 100)
    player = GamePlayer(start_pos, game_config.PLAYER_SIZE)

    # 视频采集
    cap = cv2.VideoCapture(detection_config.CAMERA_INDEX)

    prev_time = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # 检测流程
        if game_state["is_running"]:
            results = detector.detect(frame)
            landmarks = []
            if results.pose_landmarks:
                landmarks = list(results.pose_landmarks.landmark)
                frame = DetectionVisualizer.draw_landmarks(frame, results.pose_landmarks.landmark)

            controls = interpreter.interpret(landmarks)

            # 计算FPS
            current_time = time.time()
            fps = 1 / (current_time - prev_time)
            prev_time = current_time

            # 在画面上叠加调试信息
            frame = DetectionVisualizer.draw_debug_info(frame, controls, fps)

            # 游戏循环
            engine.update(controls, player)
            engine.render(player)
        else:
            # 如果游戏未运行，显示提示信息
            cv2.putText(frame, "点击'开始游戏'按钮开始", (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # 编码为JPEG格式
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        # 生成MJPEG流
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def index():
    return render_template('index.html', game_state=game_state)


@app.route('/toggle_game', methods=['POST'])
def toggle_game():
    global game_state
    data = request.json
    if 'start_game' in data:
        game_state['is_running'] = data['start_game']
    return jsonify({"status": "success", "is_running": game_state['is_running']})


if __name__ == '__main__':
    app.run(debug=True)