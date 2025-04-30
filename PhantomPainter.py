import cv2
import mediapipe as mp
import numpy as np

mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# 初始化画布
canvas = np.zeros((480, 640, 3), dtype=np.uint8)
prev_point = None

cap = cv2.VideoCapture(0)
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(rgb_frame)

    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark
        left_wrist = (int(landmarks[mp_pose.PoseLandmark.LEFT_WRIST].x * frame.shape[1]),
                      int(landmarks[mp_pose.PoseLandmark.LEFT_WRIST].y * frame.shape[0]))

        if prev_point:
            cv2.line(canvas, prev_point, left_wrist, (0, 255, 0), 5)

        prev_point = left_wrist

    combined_frame = cv2.addWeighted(frame, 0.7, canvas, 0.3, 0)
    cv2.imshow('空中画笔游戏', combined_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()