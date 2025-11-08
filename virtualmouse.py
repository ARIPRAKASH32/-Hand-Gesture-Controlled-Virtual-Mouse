@@ -0,0 +1,195 @@
import cv2
import mediapipe as mp
import pyautogui
import random
import numpy as np
import os
import time
from pynput.mouse import Button, Controller

mouse = Controller()
screen_width, screen_height = pyautogui.size()

mpHands = mp.solutions.hands
hands = mpHands.Hands(
    static_image_mode=False,
    model_complexity=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7,
    max_num_hands=1
)

draw = mp.solutions.drawing_utils
screenshot_dir = r'C:\Users\Arun E\OneDrive\Desktop\virtulmouse screenshoot'
os.makedirs(screenshot_dir, exist_ok=True)

hand_open = False
prev_x, prev_y = 0, 0
smoothening = 7
gesture_prev_state = False
last_scroll_time = time.time()
scroll_delay = 0.5

def get_angle(a, b, c):
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(np.degrees(radians))
    return angle

def get_distance(landmark_list):
    if len(landmark_list) < 2:
        return 0
    (x1, y1), (x2, y2) = landmark_list[0], landmark_list[1]
    L = np.hypot(x2 - x1, y2 - y1)
    return np.interp(L, [0, 1], [0, 1000])

def find_finger_tip(processed):
    if processed.multi_hand_landmarks:
        hand_landmarks = processed.multi_hand_landmarks[0]
        return hand_landmarks.landmark[mpHands.HandLandmark.INDEX_FINGER_TIP]
    return None

def move_mouse(index_finger_tip):
    global prev_x, prev_y
    if index_finger_tip is not None:
        target_x = int(index_finger_tip.x * screen_width)
        target_y = int(index_finger_tip.y / 2 * screen_height)
        curr_x = prev_x + (target_x - prev_x) / smoothening
        curr_y = prev_y + (target_y - prev_y) / smoothening
        pyautogui.moveTo(curr_x, curr_y)
        prev_x, prev_y = curr_x, curr_y

def is_left_click(landmark_list, thumb_index_dist):
    return get_angle(landmark_list[5], landmark_list[6], landmark_list[8]) < 50 and \
           get_angle(landmark_list[9], landmark_list[10], landmark_list[12]) > 90 and \
           thumb_index_dist > 50

def is_right_click(landmark_list, thumb_index_dist):
    return get_angle(landmark_list[9], landmark_list[10], landmark_list[12]) < 50 and \
           get_angle(landmark_list[5], landmark_list[6], landmark_list[8]) > 90 and \
           thumb_index_dist > 50

def is_custom_double_click_pose(landmark_list):
    if len(landmark_list) < 21:
        return False
    return get_angle(landmark_list[5], landmark_list[6], landmark_list[8]) < 60 and \
           get_angle(landmark_list[9], landmark_list[10], landmark_list[12]) < 60 and \
           get_angle(landmark_list[13], landmark_list[14], landmark_list[16]) < 60 and \
           get_angle(landmark_list[2], landmark_list[3], landmark_list[4]) > 150 and \
           get_angle(landmark_list[17], landmark_list[18], landmark_list[20]) > 150

def is_hand_open(landmark_list):
    return all(get_angle(landmark_list[0], landmark_list[i], landmark_list[i+3]) > 150 for i in [5, 9, 13, 17])

def is_hand_closed(landmark_list):
    return all(get_angle(landmark_list[0], landmark_list[i], landmark_list[i+3]) < 60 for i in [5, 9, 13, 17])

def is_movement_gesture(landmark_list):
    return get_angle(landmark_list[5], landmark_list[6], landmark_list[8]) > 90 and \
           get_angle(landmark_list[9], landmark_list[10], landmark_list[12]) > 90 and \
           get_angle(landmark_list[2], landmark_list[3], landmark_list[4]) > 40 and \
           get_angle(landmark_list[13], landmark_list[14], landmark_list[16]) < 60 and \
           get_angle(landmark_list[17], landmark_list[18], landmark_list[20]) < 60

def is_drag_gesture(landmark_list):
    return get_distance([landmark_list[4], landmark_list[8]]) < 30

def is_scroll_up_gesture(landmark_list):
    return get_angle(landmark_list[5], landmark_list[6], landmark_list[8]) > 150 and \
           get_angle(landmark_list[9], landmark_list[10], landmark_list[12]) > 150 and \
           get_angle(landmark_list[13], landmark_list[14], landmark_list[16]) < 60 and \
           get_angle(landmark_list[17], landmark_list[18], landmark_list[20]) < 60

def is_scroll_down_gesture(landmark_list):
    return get_angle(landmark_list[5], landmark_list[6], landmark_list[8]) < 60 and \
           get_angle(landmark_list[9], landmark_list[10], landmark_list[12]) < 60 and \
           get_angle(landmark_list[13], landmark_list[14], landmark_list[16]) < 60 and \
           get_angle(landmark_list[17], landmark_list[18], landmark_list[20]) < 60

def detect_gesture(frame, landmark_list, processed):
    global hand_open, gesture_prev_state, last_scroll_time

    if len(landmark_list) >= 21:
        index_finger_tip = find_finger_tip(processed)
        thumb_index_dist = get_distance([landmark_list[4], landmark_list[5]])

        # Drag
        if is_drag_gesture(landmark_list):
            mouse.press(Button.left)
            move_mouse(index_finger_tip)
            cv2.putText(frame, "Dragging", (50, 170), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
        else:
            mouse.release(Button.left)

        # Scroll Up
        if is_scroll_up_gesture(landmark_list) and time.time() - last_scroll_time > scroll_delay:
            pyautogui.scroll(20)
            last_scroll_time = time.time()
            cv2.putText(frame, "Scroll Up", (50, 210), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Scroll Down
        elif is_scroll_down_gesture(landmark_list) and time.time() - last_scroll_time > scroll_delay:
            pyautogui.scroll(-20)
            last_scroll_time = time.time()
            cv2.putText(frame, "Scroll Down", (50, 210), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        elif is_movement_gesture(landmark_list):
            move_mouse(index_finger_tip)
            cv2.putText(frame, "Mouse Moving", (50, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
        else:
            cv2.putText(frame, "Move Gesture Not Detected", (50, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        if is_left_click(landmark_list, thumb_index_dist):
            mouse.press(Button.left)
            mouse.release(Button.left)
            cv2.putText(frame, "Left Click", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        elif is_right_click(landmark_list, thumb_index_dist):
            mouse.press(Button.right)
            mouse.release(Button.right)
            cv2.putText(frame, "Right Click", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        gesture_current = is_custom_double_click_pose(landmark_list)
        if gesture_current and not gesture_prev_state:
            pyautogui.doubleClick()
            cv2.putText(frame, "Double Click (Custom)", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
        gesture_prev_state = gesture_current

        if is_hand_open(landmark_list):
            hand_open = True
        elif hand_open and is_hand_closed(landmark_list):
            hand_open = False
            im1 = pyautogui.screenshot()
            label = random.randint(1, 1000)
            file_path = os.path.join(screenshot_dir, f'my_screenshot_{label}.png')
            im1.save(file_path)
            cv2.putText(frame, "Screenshot Taken", (50, 130), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

def main():
    cap = cv2.VideoCapture(0)
    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            frame = cv2.flip(frame, 1)
            frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            processed = hands.process(frameRGB)

            landmark_list = []
            if processed.multi_hand_landmarks:
                hand_landmarks = processed.multi_hand_landmarks[0]
                draw.draw_landmarks(frame, hand_landmarks, mpHands.HAND_CONNECTIONS)
                for lm in hand_landmarks.landmark:
                    landmark_list.append((lm.x, lm.y))

            detect_gesture(frame, landmark_list, processed)

            cv2.imshow('Virtual Mouse', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
