import random
import camf
import time
import logic


camf.stalcraft_foreground()
time.sleep(1)
camf.pressP()
camf.auction_click()
item_complete_buy=False
while not item_complete_buy:
    item_complete_buy=logic.fullstack()



