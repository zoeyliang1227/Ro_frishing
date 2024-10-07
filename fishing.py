import numpy as np
import pyautogui
import time
import cv2


num_seconds = 1.5
t = 5
fish = cv2.imread('./fish.jpg')
setfish = cv2.imread('./fishset.jpg')
getfish = cv2.imread('./fishget.jpg')
leave = cv2.imread('./leave.jpg')
screen_width, screen_height = pyautogui.size()      # 獲取螢幕大小

def main():
    print('請在 5 秒內將滑鼠移到你想要的座標...')
    time.sleep(t)

    x, y = pyautogui.position()
    print(f'當前滑鼠座標: ({x}, {y})')

    pyautogui.moveTo(x, y, duration = num_seconds)

    if within_screen(x, y, screen_width, screen_height):
        print(f'座標 ({x}, {y}) 在螢幕內。')
    else:
        print(f'座標 ({x}, {y}) 不在螢幕內。')

    check_fish(x, y)
    time.sleep(t)
    leave_button(x, y)
    time.sleep(t)
    set_fish(x, y)
    time.sleep(t)
    get_fish(x, y)

def orb(imga, imgb, x, y, success, fail):
    grayA = cv2.cvtColor(imga, cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(imgb, cv2.COLOR_BGR2GRAY)
    orb = cv2.ORB_create()
    keypointsA, descriptorsA = orb.detectAndCompute(grayA, None)
    keypointsB, descriptorsB = orb.detectAndCompute(grayB, None)
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(descriptorsA, descriptorsB)
    matches = sorted(matches, key=lambda x: x.distance)
    # 計算匹配的比例
    good_matches = [m for m in matches if m.distance < 30]  # 調整距離閾值
    if len(good_matches) < 10:  # 這裡的數量閾值可以根據需要調整
        print(success)
        pyautogui.click(x, y)

    else:
        print(fail)

def check_fish(x, y):
    fish_B = pyautogui.screenshot()
    fish_B = cv2.cvtColor(np.array(fish_B), cv2.COLOR_RGB2BGR)

    orb(fish, fish_B, x, y, '找到釣魚按鈕！', '未找到釣魚按鈕。')

def leave_button(x, y):
    leave_B = pyautogui.screenshot()
    leave_B = cv2.cvtColor(np.array(leave_B), cv2.COLOR_RGB2BGR)

    orb(leave, leave_B, x, y, '已進入釣魚狀態！', '未進入釣魚狀態。')

def set_fish(x, y):
    location = pyautogui.locateOnScreen(setfish, confidence=0.8)

    if location:
        print(f'找到圖片的位置: {location}')
        # print(location[0], location[1])
    else:
        print('圖片未找到。')

    pyautogui.moveTo(location[0], location[1], duration = num_seconds)
    
    setfish_B = pyautogui.screenshot()
    setfish_B = cv2.cvtColor(np.array(setfish_B), cv2.COLOR_RGB2BGR)

    orb(setfish, setfish_B, x, y, '找到拋竿按鈕！', '未找到拋竿按鈕。')

def get_fish(x, y):
    getfish_B = pyautogui.screenshot()
    getfish_B = cv2.cvtColor(np.array(getfish_B), cv2.COLOR_RGB2BGR)

    orb(getfish, getfish_B, x, y, '找到提竿按鈕！', '未找到提竿按鈕。')

def within_screen(x, y, screen_width, screen_height):
    if 0 <= x < screen_width and 0 <= y < screen_height:        # 判斷座標是否在螢幕內
        return True
    else:
        return False


if __name__ == '__main__':
    main()
    input('按 Enter 鍵退出...')
