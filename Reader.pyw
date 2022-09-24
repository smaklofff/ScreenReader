import pyautogui
from pynput import mouse
import cv2
import pytesseract
import keyboard
import pyperclip
from pathlib import Path

LIST_CORD = []



def on_click(x, y, button, pressed):  # Прослушивание мыши
    if pressed and button.name == "left":
        LIST_CORD.append([x, y])
    elif len(LIST_CORD) == 2:
        cv2.destroyAllWindows()
        # Остановка прослушивания
        print(LIST_CORD)
        return False


def take_screenshot():  # получение и обработка скриншота
    im = pyautogui.screenshot()
    im.save(Path(Path.home(), "Pictures", "screen.png"))
    img = cv2.imread(str(Path(Path.home(), "Pictures", "screen.png")))

    max_x, min_x = 0, 10000000
    max_y, min_y = 0, 10000000
    for list in LIST_CORD:
        if list[0] < min_x:
            min_x = list[0]
        if list[0] > max_x:
            max_x = list[0]
        if list[1] < min_y:
            min_y = list[1]
        if list[1] > max_y: 
            max_y = list[1]

    img = img[min_y: max_y, min_x: max_x]
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    config = r'--oem 3 --psm 6'
    data = pytesseract.image_to_string(img, config=config, lang="rus+eng")
    return data



def main():  # Основыной блок
    with mouse.Listener(on_click=on_click) as listener:
        listener.join()
        img = take_screenshot()
        try:
            pyperclip.copy(img)
        except SystemError:
            pyperclip.copy('Вы ввели неправильные координаты.')
        finally:
            LIST_CORD.clear()  # Очистка массива с координатами области скриншота


def hot_key():  # Создание горячей клавиши
    pytesseract.pytesseract.tesseract_cmd = Path("Tesseract", "tesseract.exe")
    keyboard.wait('Ctrl + F1')
    main()


while True:
    hot_key()
