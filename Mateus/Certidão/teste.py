import pyautogui

verify = pyautogui.locateCenterOnScreen('verific.PNG', confidence=0.9)
pyautogui.click(verify)