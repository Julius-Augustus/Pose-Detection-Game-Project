# utils/visualizer.py
import cv2
import mediapipe as mp

class DetectionVisualizer:
    # 预定义上半身关键点连接关系
    UPPER_BODY_POSE_CONNECTIONS = frozenset([
        (0, 11), (0, 12), (11, 13), (13, 15), (12, 14), (14, 16)
    ])

    # 颜色配置
    LANDMARK_COLOR = (0, 255, 0)  # 关键点颜色（BGR）
    CONNECTION_COLOR = (255, 128, 0)  # 连接线颜色
    TEXT_COLOR = (0, 0, 255)  # 文本颜色

    @classmethod
    def draw_landmarks(cls, frame, landmarks, show_index=False, line_thickness=2):
        """
        在视频帧上绘制姿态关键点及连接线

        参数:
            frame: 输入图像帧 (BGR格式)
            landmarks: mediapipe检测到的姿态关键点列表
            show_index: 是否显示关键点索引
            line_thickness: 连接线粗细
        """
        if landmarks is None:
            return frame

        frame_height, frame_width = frame.shape[:2]
        # 上半身关键点索引
        UPPER_BODY_LANDMARKS = [0, 11, 12, 13, 14, 15, 16]
        upper_body_landmarks = [landmarks[i] for i in UPPER_BODY_LANDMARKS if i < len(landmarks)]

        # 绘制连接线
        for connection in cls.UPPER_BODY_POSE_CONNECTIONS:
            start_idx, end_idx = connection
            start_point = cls._get_pixel_coord(upper_body_landmarks[UPPER_BODY_LANDMARKS.index(start_idx)], frame_width, frame_height)
            end_point = cls._get_pixel_coord(upper_body_landmarks[UPPER_BODY_LANDMARKS.index(end_idx)], frame_width, frame_height)

            if start_point and end_point:
                cv2.line(frame, start_point, end_point, cls.CONNECTION_COLOR, line_thickness)

        # 绘制关键点
        for idx, landmark in enumerate(upper_body_landmarks):
            center = cls._get_pixel_coord(landmark, frame_width, frame_height)
            if center:
                # 绘制圆形关键点
                cv2.circle(frame, center, 5, cls.LANDMARK_COLOR, -1)

                # 显示索引编号
                if show_index:
                    cv2.putText(frame, str(UPPER_BODY_LANDMARKS[idx]),
                                (center[0] + 5, center[1] - 5),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                cls.TEXT_COLOR, 1)

        return frame

    @staticmethod
    def _get_pixel_coord(landmark, frame_width, frame_height):
        """将归一化坐标转换为像素坐标"""
        if landmark.visibility < 0.5:  # 过滤低可见度关键点
            return None
        return (
            int(landmark.x * frame_width),
            int(landmark.y * frame_height)
        )

    @classmethod
    def draw_debug_info(cls, frame, controls, fps):
        """在画面上叠加调试信息"""
        info_text = [
            f"FPS: {fps:.1f}",
            f"Controls: {controls}"
        ]

        y_offset = 30
        for text in info_text:
            cv2.putText(frame, text, (10, y_offset),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                        cls.TEXT_COLOR, 2)
            y_offset += 30

        return frame