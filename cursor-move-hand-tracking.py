import cv2
import mediapipe as mp
import pyautogui

capture_hands = mp.solutions.hands.Hands()
drawing_option = mp.solutions.drawing_utils
screen_width, screen_height = pyautogui.size()
camera = cv2.VideoCapture(0)
x1 = y1 = x2 = y2 = 0

while True:
    ret, image = camera.read()
    if not ret:
        break
    image = cv2.flip(image, 1)
    image_height, image_width, _ = image.shape
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    output_hands = capture_hands.process(rgb_image)

    if output_hands.multi_hand_landmarks:
        for hand in output_hands.multi_hand_landmarks:
            drawing_option.draw_landmarks(image, hand, mp.solutions.hands.HAND_CONNECTIONS)
            one_hand_landmarks = hand.landmark
            for id, lm in enumerate(one_hand_landmarks):
                x = int(lm.x * image_width)  
                y = int(lm.y * image_height)  

                if id == 8: 
                    mouse_x = int(x / image_width * screen_width)
                    mouse_y = int(y / image_height * screen_height)
                    cv2.circle(image, (x, y), 10, (0, 255, 255), -1)
                    pyautogui.moveTo(mouse_x, mouse_y)
                    x1, y1 = x, y

                if id == 4:  
                    x2, y2 = x, y
                    cv2.circle(image, (x, y), 10, (0, 0, 255), -1)

           
            dist = abs(y2 - y1)
            if dist < 20:
                pyautogui.click()

    
    cv2.imshow("Hand Movement Video Capture", image)

    
    key = cv2.waitKey(1)
    if key == 27:  
        break

camera.release()
cv2.destroyAllWindows()
