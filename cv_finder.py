import time
import cv2
from PIL import ImageGrab


method = cv2.TM_SQDIFF_NORMED

def find_element_on_screen(finding_element_path, fullscreen_image_path):

    small = cv2.imread(finding_element_path)
    fullscreen = cv2.imread(fullscreen_image_path)


    small_grey=cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)
    fullscreen_grey=cv2.cvtColor(fullscreen, cv2.COLOR_BGR2GRAY)

    small_canny = cv2.Canny(small_grey, 50, 150)
    fullscreen_canny = cv2.Canny(fullscreen_grey, 100, 150)



    # Используем OpenCV для поиска элемента на экране
    result = cv2.matchTemplate(small_canny, fullscreen_canny, method)
    _, _, mnLoc, _ = cv2.minMaxLoc(result)
    x, y = mnLoc

    # Получаем размеры элемента
    h, w, _ = small.shape

    # Получаем координаты элемента относительно полного экрана
    x_fullscreen = x + w // 2
    y_fullscreen = y + h // 2

    return x_fullscreen, y_fullscreen

def find_element_on_screen_sobel(finding_element, fullscreen_image):
    finding = cv2.imread(finding_element)
    fullscreen = cv2.imread(fullscreen_image)

    finding_gray = cv2.cvtColor(finding, cv2.COLOR_BGR2GRAY)
    fullscreen_gray = cv2.cvtColor(fullscreen, cv2.COLOR_BGR2GRAY)

    # Compute gradients along the X and Y axis, respectively, for the finding element
    gX_finding = cv2.Sobel(finding_gray, cv2.CV_64F, 1, 0)
    gY_finding = cv2.Sobel(finding_gray, cv2.CV_64F, 0, 1)

    # Convert the gradients to positive integer format
    gX_finding = cv2.convertScaleAbs(gX_finding)
    gY_finding = cv2.convertScaleAbs(gY_finding)

    # Combine the Sobel X and Y gradients for the finding element with equal weights
    sobel_combined_finding = cv2.addWeighted(gX_finding, 0.5, gY_finding, 0.5, 0)

    # Show the images with the gradients for the finding element


    # Compute gradients along the X and Y axis, respectively, for the fullscreen image
    gX_fullscreen = cv2.Sobel(fullscreen_gray, cv2.CV_64F, 1, 0)
    gY_fullscreen = cv2.Sobel(fullscreen_gray, cv2.CV_64F, 0, 1)

    # Convert the gradients to positive integer format
    gX_fullscreen = cv2.convertScaleAbs(gX_fullscreen)
    gY_fullscreen = cv2.convertScaleAbs(gY_fullscreen)

    # Combine the Sobel X and Y gradients for the fullscreen image with equal weights
    sobel_combined_fullscreen = cv2.addWeighted(gX_fullscreen, 0.5, gY_fullscreen, 0.5, 0)

    # Show the images with the gradients for the fullscreen image

    # Use cv2.matchTemplate method to find the element on the fullscreen image using the Sobel gradients
    result = cv2.matchTemplate(sobel_combined_finding, sobel_combined_fullscreen, method)
    _, _, minLoc, _ = cv2.minMaxLoc(result)
    x, y = minLoc

    # Get the size of the finding element
    h, w = finding_gray.shape

    # Get the coordinates of the element on the fullscreen image
    x_fullscreen = x + w // 2
    y_fullscreen = y + h // 2

    # Print the coordinates of the element on the fullscreen image
    return x_fullscreen, y_fullscreen

def coordinates_pages(page_count, page_to_find):
    page_screenshot_path = r'Screenshot\\Pages\\page'
    fullscreen_image_path = 'Screenshot/tesseract/online/fullscreen_trade_menu.png'
    coordinates_pages = {}

    for i in range(1, page_count):
        page_number = str(i)
        finding_element = page_screenshot_path + page_number + '.png'
        x, y = find_element_on_screen_sobel(finding_element, fullscreen_image_path)
        coordinates_pages[i] = (x, y)
        if i == page_to_find:
            return x, y

    return None, None

    return coordinates_pages

def coordinates_auction():
    auction_png = r'Screenshot/auction.png'
    fullscreen_P_menu_png = r'Screenshot/fullscreen_P_menu.png'
    coordinates_auction=find_element_on_screen(auction_png, fullscreen_P_menu_png)

    return coordinates_auction


def take_screenshot_bbox(filename_prefix, save_directory, bbox=None):
    screenshot = ImageGrab.grab(bbox)
    screenshot.save(save_directory + filename_prefix + '.png')
    screenshot_path=save_directory + filename_prefix + '.png'
    return screenshot_path


def coordinates_text_buyout():
    filename_prefix='start_trade_menu'
    save_directory='screenshot/tesseract/online/'
    time.sleep(2)
    buyout_fullscreen=take_screenshot_bbox(filename_prefix, save_directory, None)
    buyot_text_find='screenshot/tesseract/text_buyout.png'
    coordinates_text_buyout= find_element_on_screen(buyot_text_find,buyout_fullscreen)

    return coordinates_text_buyout

