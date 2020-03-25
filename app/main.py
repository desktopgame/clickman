import pyautogui


screen_x, screen_y = pyautogui.size()
mouse_x, mouse_y = pyautogui.position()

print(f'screenX={screen_x} screenY={screen_y}')
print(f'mouseX={mouse_x} mouseY={mouse_y}')
