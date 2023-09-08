import cv_finder
import camf
import pytesseract
import cv2
import numpy
#
# method=cv2.TM_SQDIFF_NORMED
# pages_screen = r'Screenshot\\tesseract\\online\\Screenshot_1.png'
# CUSTOM_CONFIG = r'-l eng --oem 3 --psm 6 -c tessedit_char_whitelist=1,2,3,4,5,6,7,8,9,10,11,12,13'
# page_counttext = pytesseract.image_to_string(pages_screen, config=CUSTOM_CONFIG)
# print(page_counttext)
# count=len(page_counttext)
# countD=0
# full=0
# countA=0
# if count>9:
#     countB=count-9
#     countA=countB/2
#     full=9
# else:
#     countD=count
# full=full+countA+countD
# full=int(full)
# print(full)
# # BUYOUT_X, BUYOUT_Y = cv_finder.coordinates_text_buyout()
# # print(BUYOUT_X, BUYOUT_Y)
# page_amount=13
# for i in range(2,full+1):
#     print(i)
