import pyautogui
import time
from pyautogui import ImageNotFoundException

def locate_and_click(image_path, delay=0):
    """
    Locates an image on screen and clicks it.
    """
    try:
        location = pyautogui.locateOnScreen(image_path, confidence=0.8)
        if location:
            time.sleep(delay)
            center = pyautogui.center(location)
            pyautogui.moveTo(center)
            pyautogui.mouseDown()
            pyautogui.mouseUp()
            return True
    except ImageNotFoundException:
        return False
    return False


def image_exists(image_path, confidence=0.8):
    """
    Checks if an image is visible on the screen.
    """
    try:
        return pyautogui.locateOnScreen(image_path, confidence=confidence) is not None
    except ImageNotFoundException:
        return False
    except Exception as e:
        print(f"[ERROR] Unexpected error while checking image {image_path}: {e}")
        return False