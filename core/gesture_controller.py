# core/gesture_controller.py
class GestureInterpreter:
    def __init__(self, screen_size):
        self.screen_size = screen_size
        self.MOVE_SENSITIVITY = 0.2  # 横向移动灵敏度
        self.JUMP_THRESHOLD = 0.3  # 跳跃动作阈值
        # 上半身关键点索引
        self.UPPER_BODY_LANDMARKS = [0, 11, 12, 13, 14, 15, 16]

    def interpret(self, landmarks):
        """将人体关键点转换为游戏控制指令"""
        # 检查 landmarks 是否为序列类型
        if not isinstance(landmarks, (list, tuple)):
            print(f"Error: landmarks should be a list or tuple, but got {type(landmarks)}")
            return {
                'move_left': False,
                'move_right': False,
                'jump': False
            }
        # 筛选上半身关键点
        upper_body_landmarks = [landmarks[i] for i in self.UPPER_BODY_LANDMARKS if i < len(landmarks)]
        return {
            'move_left': self._detect_left_arm(upper_body_landmarks),
            'move_right': self._detect_right_arm(upper_body_landmarks),
            'jump': self._detect_jump(upper_body_landmarks)
        }

    def _detect_left_arm(self, landmarks):
        """检测左臂水平移动（关键点索引根据mediapipe定义）"""
        if not landmarks:
            return False

        # 左肩(11) 和 左腕(15) 的横向位置比较
        left_shoulder = self._get_landmark_x(landmarks, self.UPPER_BODY_LANDMARKS.index(11))
        left_wrist = self._get_landmark_x(landmarks, self.UPPER_BODY_LANDMARKS.index(15))
        if left_shoulder is not None and left_wrist is not None:
            return (left_wrist - left_shoulder) < -self.MOVE_SENSITIVITY
        return False

    def _detect_right_arm(self, landmarks):
        """检测右臂水平移动"""
        if not landmarks:
            return False

        # 右肩(12) 和 右腕(16) 的横向位置比较
        right_shoulder = self._get_landmark_x(landmarks, self.UPPER_BODY_LANDMARKS.index(12))
        right_wrist = self._get_landmark_x(landmarks, self.UPPER_BODY_LANDMARKS.index(16))
        if right_shoulder is not None and right_wrist is not None:
            return (right_wrist - right_shoulder) > self.MOVE_SENSITIVITY
        return False

    def _detect_jump(self, landmarks):
        """通过头部垂直移动检测跳跃动作"""
        if not landmarks:
            return False

        # 鼻子(0) 的垂直位置变化
        nose = self._get_landmark_y(landmarks, self.UPPER_BODY_LANDMARKS.index(0))
        # 由于只检测上半身，这里可以使用其他上半身关键点代替左髋部
        left_shoulder = self._get_landmark_y(landmarks, self.UPPER_BODY_LANDMARKS.index(11))
        if nose is not None and left_shoulder is not None:
            return (left_shoulder - nose) > self.JUMP_THRESHOLD
        return False

    # 新增安全访问方法
    def _get_landmark(self, landmarks, index):
        """安全获取关键点"""
        if landmarks and 0 <= index < len(landmarks):
            return landmarks[index]
        return None

    def _get_landmark_x(self, landmarks, index):
        """安全地获取指定索引关键点的 x 坐标。"""
        landmark = self._get_landmark(landmarks, index)
        if landmark is not None:
            return landmark.x
        return None

    def _get_landmark_y(self, landmarks, index):
        """安全地获取指定索引关键点的 y 坐标。"""
        landmark = self._get_landmark(landmarks, index)
        if landmark is not None:
            return landmark.y
        return None