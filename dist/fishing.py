import pyautogui
import time

from PIL import Image

num_seconds = 1.5
fish = Image.open('./login.jpg')
setfish = Image.open('./fishset.jpg')
getfish = Image.open('./fishget.jpg')
screen_width, screen_height = pyautogui.size()      # 獲取螢幕大小

def main():
    print("請在 5 秒內將滑鼠移到你想要的座標...")
    time.sleep(5)

    x, y = pyautogui.position()
    print(f"當前滑鼠座標: ({x}, {y})")

    pyautogui.moveTo(x, y, duration = num_seconds)

    if within_screen(x, y, screen_width, screen_height):
        print(f"座標 ({x}, {y}) 在螢幕內。")
    else:
        print(f"座標 ({x}, {y}) 不在螢幕內。")

    check_fish()
    set_fish()
    get_fish()

def check_fish():
    try:
        print(fish)
        location = pyautogui.locateOnScreen(fish)
        if location:
            print("找到釣魚按鈕！位置:", location)

        else:
            print("未找到釣魚按鈕。")
    except Exception as e:
        print("錯誤:釣魚按鈕", e)

    pyautogui.click(x, y)

def set_fish():
    try:
        location = pyautogui.locateOnScreen(setfish)
        if location:
            print("找到拋竿按鈕！位置:", location)

        else:
            print("未找到拋竿按鈕。")
    except Exception as e:
        print("錯誤:拋竿按鈕", e)

    pyautogui.click(x, y)

def get_fish():
    try:
        location = pyautogui.locateOnScreen(getfish)
        if location:
            print("找到提竿按鈕！位置:", location)

        else:
            print("未找到提竿按鈕。")
    except Exception as e:
        print("錯誤:提竿按鈕", e)

    pyautogui.click(x, y)

def within_screen(x, y, screen_width, screen_height):
    if 0 <= x < screen_width and 0 <= y < screen_height:        # 判斷座標是否在螢幕內
        return True
    else:
        return False


if __name__ == '__main__':
    main()
