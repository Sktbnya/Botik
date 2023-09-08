import random
import time
import pytesseract
import camf
import cv_finder



CUSTOM_CONFIG = r'-l rus --oem 3 --psm 6 -c tessedit_char_whitelist=0,1,2,3,4,5,6,7,8,9,р,у,б,л,е,й'
global COUNT_BUYOUT_ON_PAGE,item_complete_buy
item_complete_buy=False
COUNT_BUYOUT_ON_PAGE = 9


def page_count():
    bboxpages_x1 = BUYOUT_X - 328  # 880 980
    bboxpages_y1 = BUYOUT_Y + 388  # 770
    bboxpages_x2 = BUYOUT_X - 18  # 1380 1290
    bboxpages_y2 = BUYOUT_Y + 408  # 790
    bboxpages = (bboxpages_x1, bboxpages_y1, bboxpages_x2, bboxpages_y2)
    time.sleep(3)
    pages_screen = cv_finder.take_screenshot_bbox('page_count', 'Screenshot/tesseract/online/', bboxpages)
    CUSTOM_CONFIG = r'-l eng --oem 3 --psm 6 -c tessedit_char_whitelist=1,2,3,4,5,6,7,8,9,10,11,12,13'
    page_counttext = pytesseract.image_to_string(pages_screen, config=CUSTOM_CONFIG)
    count = len(page_counttext)
    countD = 0
    full = 0
    countA = 0
    if count > 9:
        countB = count - 9
        countA = countB / 2
        full = 9
    else:
        countD = count
    page_count = full + countA + countD
    page_count = int(page_count)
    print('page_count',page_count)
    return page_count
    # 335 350 1170 1300


def search_input():
    global BUYOUT_X, BUYOUT_Y
    BUYOUT_X, BUYOUT_Y = cv_finder.coordinates_text_buyout()
    search_x = BUYOUT_X - random.randint(15, 25)
    search_y = BUYOUT_Y - random.randint(36, 39)
    camf.move_mouse_smoothly(search_x, search_y)
    time.sleep(random.uniform(0.1, 0.5))
    camf.mouseclick()
    time.sleep(0.5)
    camf.search_input(item_name)

def search_delete_input():
    x = BUYOUT_X - random.randint(15, 25)
    y = BUYOUT_Y - random.randint(36, 39)
    camf.move_mouse_smoothly(x, y)
    time.sleep(random.uniform(0.1, 0.5))
    camf.mouseclick()
    time.sleep(0.5)
    camf.delete_text()

def search_button():
    search_button_x = BUYOUT_X + random.randint(0, 60)
    search_button_y = BUYOUT_Y - random.randint(35, 40)  # 335 353 1306 1379
    camf.move_mouse_smoothly(search_button_x, search_button_y)
    camf.mouseclick()
    camf.buyot_sort()
    time.sleep(1)



def buyout_price_each():

    buyoutprice = {}
    buyout_x1 = BUYOUT_X - 65
    buyout_y1 = BUYOUT_Y-40
    buyout_x2 = BUYOUT_X + 75
    buyout_y2=buyout_y1+40
    for i in range(1,COUNT_BUYOUT_ON_PAGE+1):
        buyout_x1 = buyout_x1  # 1245
        buyout_x2 = buyout_x2  # 1380
        buyout_y1 = buyout_y1 + 38 # 395
        buyout_y2 = buyout_y1 + 40 # 430
        print('bbox buyout', buyout_x1, buyout_y1, buyout_x2, buyout_y2)
        bboxbuyout = (buyout_x1, buyout_y1, buyout_x2, buyout_y2)
        time.sleep(3)
        buyout_png = cv_finder.take_screenshot_bbox('buyout'+f'{i}', 'Screenshot/tesseract/online/buyout/', bboxbuyout)
        textbuyout = pytesseract.image_to_string(buyout_png, config=CUSTOM_CONFIG)
        print(textbuyout)
        digits_buyout = ''.join(filter(str.isdigit, textbuyout))
        price = int(digits_buyout) if digits_buyout else 0
        buyoutprice[i] = price
    return buyoutprice


def cost_numb():

    numb_y1 = BUYOUT_Y-28
    numb_x1 = BUYOUT_X - 420  # 890
    numb_x2 = numb_x1 + 40  # 925
    numb = {}
    for i in range(1,COUNT_BUYOUT_ON_PAGE+1):
        numb_y1 = numb_y1 + 37 # 390
        numb_y2 = numb_y1 + 37  # 425
        bboxnumb = (numb_x1, numb_y1, numb_x2, numb_y2)
        print('bbox numb', numb_x1, numb_y1, numb_x2, numb_y2)
        time.sleep(3)
        numb_png = cv_finder.take_screenshot_bbox('numb'+f'{i}', 'Screenshot/tesseract/online/numb/', bboxnumb)
        textnumb = pytesseract.image_to_string(numb_png, config=CUSTOM_CONFIG)
        print(textnumb)
        digits_numb = ''.join(filter(str.isdigit, textnumb))
        textnumb_int = int(digits_numb) if digits_numb else 1
        numb[i] = textnumb_int
    return numb


def cost_per_item():
    price = buyout_price_each()
    numb = cost_numb()
    cost_per_item = {}
    for i in range(1, COUNT_BUYOUT_ON_PAGE+1):
        pricei = price.get(i, 0)  # Get the price for item i or set it to 0 if not available
        numbi = numb.get(i, 1)  # Get the number for item i or set it to 1 if not available
        if pricei != 0:
            cost_per_item[i] = round(pricei / numbi)
        else:
            cost_per_item[i] = 0
    return cost_per_item

def buyout_x_y():

    x = BUYOUT_X - random.randint(1, 360)
    y = BUYOUT_Y
    buyout_x_y = {}
    for i in range(1, COUNT_BUYOUT_ON_PAGE+1):
        y = y + random.randint(32, 37)
        buyout_x_y[i] = x, y
    return buyout_x_y


def buy_page():
    buyout_coords = buyout_x_y()
    cost_per_item_values = cost_per_item()

    for i in range(1, COUNT_BUYOUT_ON_PAGE + 1):
        step=40*i
        x, y = buyout_coords[i]
        cost_item = cost_per_item_values[i]
        if cost_item !=0 and cost_item<rprice:
            camf.move_mouse_smoothly(x,y)
            camf.mouseclick()
            x=BUYOUT_X+random.randint(1,50)
            y=BUYOUT_Y+random.randint(1,20)+step
            camf.move_mouse_smoothly(x,y)
            camf.mouseclick()
            time.sleep(0.5)
            print('buy',x,y)
            x=BUYOUT_X-random.randint(160,380)
            y=BUYOUT_Y+random.randint(130,180) #y 569 498 accept x 912 1140
            #y = BUYOUT_Y + random.randint(170, 190) #y 550 579 no money x 912 1140
            camf.move_mouse_smoothly(x,y)
            camf.mouseclick()
            time.sleep(0.5)
            print('accept',x,y)
            item_complete_buy=True
            return item_complete_buy

def fullstack():
    global rprice, item_name
    item_complete_buy=False
    rprice = int(input('Введите стоимость:'))
    item_name = input('Введите название предмета:')
    search_input()
    search_button()
    page_amount=page_count()
    if page_amount !=1:
        while not item_complete_buy:
            item_complete_buy = buy_page()
            for i in range(1,4):
                camf.scroll2(i)
                buy_page()
            for i in range(2,page_amount+1):
                x,y=cv_finder.coordinates_pages(page_amount,i)
                camf.move_mouse_smoothly(x,y)
                camf.mouseclick()
                for i in range(1, 4):
                    camf.scroll2(i)
                    item_complete_buy=buy_page()
            search_delete_input()

    else:
        item_complete_buy = buy_page()
        search_delete_input()
    return item_complete_buy

fullstack()