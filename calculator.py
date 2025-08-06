import cv2
import mediapipe as mp
import time
import os
from buttons import Button

try:
    from playsound import playsound
    SOUND_ENABLED = True
except:
    SOUND_ENABLED = False

# Mediapipe setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.8)
mp_draw = mp.solutions.drawing_utils

# Camera setup
cap = cv2.VideoCapture(0)
cap.set(3, 800)  # width
cap.set(4, 600)  # height

cam_width = int(cap.get(3))
cam_height = int(cap.get(4))

# Calculator setup
button_size = 70  # SMALLER size
buttons = []
button_values = [
    ['7', '8', '9', '/'],
    ['4', '5', '6', '*'],
    ['1', '2', '3', '-'],
    ['0', 'C', '=', '+']
]

# Position calculator in visible area
offset_x = cam_width - (button_size * 4) - 40
offset_y = 80

for i in range(4):
    for j in range(4):
        x = offset_x + (button_size * j)
        y = offset_y + (button_size * i)
        buttons.append(Button((x, y), button_size, button_values[i][j]))

# Calculator logic
equation = ""
pressed_button = None
press_start_time = None

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    # Calculator background
    overlay = img.copy()
    cv2.rectangle(overlay, (offset_x - 20, offset_y - 60),
                  (offset_x + button_size * 4 + 20, offset_y + button_size * 4 + 40),
                  (50, 50, 50), cv2.FILLED)
    img = cv2.addWeighted(overlay, 0.3, img, 0.7, 0)

    # Display equation
    cv2.rectangle(img, (offset_x - 15, offset_y - 50),
                  (offset_x + button_size * 4 + 15, offset_y - 10),
                  (255, 255, 255), cv2.FILLED)
    cv2.putText(img, equation, (offset_x, offset_y - 20),
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 0), 2)

    # Draw buttons
    for button in buttons:
        button.draw(img)

    highlighted_button = None

    # Hand tracking
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            h, w, _ = img.shape
            finger_x = int(hand_landmarks.landmark[8].x * w)
            finger_y = int(hand_landmarks.landmark[8].y * h)
            cv2.circle(img, (finger_x, finger_y), 8, (255, 0, 255), cv2.FILLED)

            for button in buttons:
                if button.is_clicked(finger_x, finger_y):
                    highlighted_button = button
                    if pressed_button != button:
                        pressed_button = button
                        press_start_time = time.time()
                    else:
                        if time.time() - press_start_time >= 1.0:  
                            if SOUND_ENABLED and os.path.exists("click.mp3"):
                                playsound("click.mp3", block=False)

                            if button.value == 'C':
                                equation = ""
                            elif button.value == '=':
                                try:
                                    equation = str(eval(equation))
                                except:
                                    equation = "Error"
                            else:
                                equation += button.value
                            pressed_button = None
                else:
                    if pressed_button == button:
                        pressed_button = None
                        press_start_time = None

    # Highlight effect
    if highlighted_button:
        highlighted_button.draw(img, is_highlighted=True)

    cv2.imshow("Virtual Calculator", img)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC to exit
        break

cap.release()
cv2.destroyAllWindows()
