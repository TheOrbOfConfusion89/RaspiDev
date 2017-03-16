import logging
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG) #CHANGE TO DEBUG TO SEE MORE
logging.basicConfig(level=logging.DEBUG)

handler = logging.FileHandler('fbtft.log')
handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

log.addHandler(handler)

log.info("Define modules...")
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
import sys,pygame,time,subprocess,os,datetime
from pygame.locals import *
import re
log.debug("Define modules...OK")

#log.info("Setting /dev/fb1...")
#os.putenv('SDL_FBDEV','/dev/fb1') #Which framebuffer?
pygame.init()
#log.debug("Setting /dev/fb1...OK")

''' Defines '''

size = w, h = 160, 128 
log.info("Starting in " + str(size))
screen = pygame.display.set_mode(size)
pygame.mouse.set_visible(False)
log.debug("Starting...OK")

### RGB Colors
black = 0,0,0
white = 255,255,255
red = 255,0,0
dred = 127,0,0
green = 0,255,0
blue = 0,0,255
goodgrade = 0,255,190
### Custom Colors
bg = 50,65,60

wi=screen.get_width()
he=screen.get_height()
log.debug("Resolution: " + str(wi) + "x" + str(he))
pygame.draw.rect(screen,bg,[0,0,35,64])
pygame.display.update()



def ButtonPressed(channel):
    log.debug("Button has been pressed!")

git 
GPIO.add_event_detect(4, GPIO.BOTH, callback=ButtonPressed, bouncetime=1000)
