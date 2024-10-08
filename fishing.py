import numpy as np
import pyautogui
import time
import cv2

from PIL import Image
from datetime import datetime


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

    screen_image = pyautogui.screenshot()
    screen_image = cv2.cvtColor(np.array(screen_image), cv2.COLOR_RGB2BGR)

    check_fish(x, y, screen_image)
    time.sleep(t)
    leave_button(screen_image)
    time.sleep(t)
    set_fish(screen_image)
    time.sleep(t)
    get_fish(screen_image)

def check_fish(x, y, screen_image):
    check_image = image(fish, screen_image)
    if check_image:
        screenshot(x, y)
        print('找到釣魚按鈕！')
        pyautogui.click(x, y)
        # pyautogui.doubleClick(x, y)
        # pyautogui.doubleClick(x, y)

    else:
        print('未找到釣魚按鈕。')

def leave_button(screen_image):
    check_image = image(leave, screen_image)
    if check_image:
        # match_x, match_y = matching(check_image[1], check_image[2], check_image[3])
        # matching(leave, leave_B)
        # print(matching)
        pyautogui.moveTo(int(check_image[0]), int(check_image[1]), duration = num_seconds)
        screenshot(int(check_image[0]), int(check_image[1]))
        print('已進入釣魚狀態！')

    else:
        print('未進入釣魚狀態。')

def set_fish(screen_image):    
    check_image = image(setfish, screen_image)
    if check_image:
        # match_x, match_y = matching(check_image[1], check_image[2], check_image[3])
        # matching(setfish, setfish_B)
        pyautogui.moveTo(int(check_image[0]), int(check_image[1]), duration = num_seconds)
        screenshot(int(check_image[0]), int(check_image[1]))
        print('找到拋竿按鈕！')
        pyautogui.click(match_x, match_y)
        # pyautogui.doubleClick(match_x, match_y)
        # pyautogui.doubleClick(match_x, match_y)

    else:
        print('未找到拋竿按鈕。')

def get_fish(screen_image):
    check_image = image(getfish, screen_image)
    if check_image:
        # match_x, match_y = matching(check_image[1], check_image[2], check_image[3])
        # matching(getfish, getfish_B)
        pyautogui.moveTo(int(check_image[0]), int(check_image[1]), duration = num_seconds)
        screenshot(int(check_image[0]), int(check_image[1]))
        print('找到提竿按鈕！')
        pyautogui.click(match_x, match_y)
        # pyautogui.doubleClick(match_x, match_y)
        # pyautogui.doubleClick(match_x, match_y)

    else:
        print('未找到提竿按鈕。')


def within_screen(x, y, screen_width, screen_height):
    if 0 <= x < screen_width and 0 <= y < screen_height:        # 判斷座標是否在螢幕內
        return True
        
    else:
        return False

def image(imga, imgb):
    grayA = cv2.cvtColor(imga, cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(imgb, cv2.COLOR_BGR2GRAY)

    fuzzA = cv2.medianBlur(grayA, 7)                 # 模糊化，去除雜訊
    fuzzB = cv2.medianBlur(grayB, 7)                 # 模糊化，去除雜訊

    outputA = cv2.Laplacian(fuzzA, -1, 1, 5)        # 偵測邊緣
    outputB = cv2.Laplacian(fuzzB, -1, 1, 5)        # 偵測邊緣

    sift = cv2.SIFT_create()
    keypointsA, descriptorsA = sift.detectAndCompute(outputA, None)
    keypointsB, descriptorsB = sift.detectAndCompute(outputB, None)

    bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=False)
    matches = bf.match(descriptorsA, descriptorsB)
    matches = sorted(matches, key=lambda x: x.distance)

    threshold = 1  # 根据需要调整
    theight, twidth = imga.shape[:2]
    result = cv2.matchTemplate(imgb, imga, cv2.TM_CCOEFF_NORMED)
    cv2.normalize(result, result, 0, 1, cv2.NORM_MINMAX, 1)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)


    # 判断是否有精准匹配
    if min_val <= threshold:
        print("精确匹配，最小值:", min_val)

        # 找到匹配的左上角坐标
        top_left = min_loc
        bottom_right = (top_left[0] + twidth, top_left[1] + theight)

        # 计算中心坐标
        center_x = top_left[0] + twidth // 2
        center_y = top_left[1] + theight // 2
        center_coords = (center_x, center_y)

        # 绘制矩形
        cv2.rectangle(imgb, top_left, bottom_right, (0, 0, 225), 2)

        # 打印匹配的中心坐标
        print("匹配位置 (中心):", center_coords)

    else:
        print("未找到精准匹配，最小值:", min_val)

    # 显示结果（可选）
    # cv2.imshow('Matched Result', imgb)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    return center_coords

# def matching(keypointsA, keypointsB, good_matches):
#     #獲取有效匹配的特徵點坐標
#     matched_keypoints1 = np.float32([keypointsA[m.queryIdx].pt for m in good_matches])
#     matched_keypoints2 = np.float32([keypointsB[m.trainIdx].pt for m in good_matches])

#     # 輸出有效匹配的坐標
#     for pt1, pt2 in zip(matched_keypoints1, matched_keypoints2):
#         print(f'有效匹配的特徵點坐標： {pt2}')
#         pyautogui.moveTo(int(pt2[0]), int(pt2[1]), duration = num_seconds)
#         break 

#     return int(pt2[0]), int(pt2[1])    

def screenshot(x, y):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot = pyautogui.screenshot()

    scale=0.2
    width = int(screenshot.width * scale)
    height = int(screenshot.height * scale)
    
    # 裁剪出滑鼠周圍的區域
    left = x - width // 2
    top = y - height // 2
    right = left + width
    bottom = top + height

    # 確保裁剪範圍在螢幕範圍內
    left = max(0, left)
    top = max(0, top)
    right = min(screenshot.width, right)
    bottom = min(screenshot.height, bottom)

    cropped_image = screenshot.crop((left, top, right, bottom))     # 裁剪圖像

    image_path = f"{timestamp}.png"
    cropped_image.save(image_path)  # 先保存為臨時文件
    # cropped_image.show()  # 這會打開預設圖像查看器

if __name__ == '__main__':
    main()
    input('按 Enter 鍵退出...')
