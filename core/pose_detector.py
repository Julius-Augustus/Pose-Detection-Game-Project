# pose_detector.py
import mediapipe as mp

class PoseDetector:
    def __init__(self, config):
        self.pose = mp.solutions.pose.Pose(
            min_detection_confidence=config.MIN_DETECTION_CONFIDENCE,
            min_tracking_confidence=config.MIN_TRACKING_CONFIDENCE
        )

    def detect(self, frame):
        results = self.pose.process(frame)
        # 检查结果是否有效
        if results.pose_landmarks is None:
            print("No pose landmarks detected.")
        return results