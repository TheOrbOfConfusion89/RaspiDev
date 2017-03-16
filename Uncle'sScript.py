from pathlib import *
import sys,logging,pygame,time,subprocess,os,datetime
from pygame.locals import *
import re
current_milli_time = lambda: int(round(time.time() * 1000))

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

log.debug("Define modules...OK")

os.chdir(os.path.dirname(os.path.abspath(__file__)))

#log.info("Setting /dev/fb1...")
#os.putenv('SDL_FBDEV','/dev/fb1') #Which framebuffer?
pygame.init()
#log.debug("Setting /dev/fb1...OK")

''' Defines '''
gpioChannel = 4
animationPath = "Uncle'sShaders"
defaultFrameDuration = 100
size = w, h = 160, 128 
log.info("Starting in " + str(size))
screen = pygame.display.set_mode(size)
pygame.mouse.set_visible(False)
log.debug("Starting...OK")

###Animations
Animations = []
CurrentAnimation = 0
CurrentFrame = 0
LastFrameChange = current_milli_time()
FPS = 30.0
MSPerFrame = 1.0/FPS
print("MSPerFrame = " + str(MSPerFrame))
###Button
ButtonIsDown = False
ButtonFirstWentDown = 0
ButtonHoldTimeForPower = 5000

### Custom Colors
bg = 50,65,60

wi=screen.get_width()
he=screen.get_height()
log.debug("Resolution: " + str(wi) + "x" + str(he))
pygame.draw.rect(screen,bg,[0,0,35,64])
pygame.display.update()

def ParseTiming(filePath):
        timingList = []
        f = open(filePath, 'r')
        for line in f:
                timingList.append(int(line))
        f.close()
        log.info("Found " + str(len(timingList)) + " timing values in " + filePath)
        return timingList
        
def LoadFolder(folderPath):
        timingList = [defaultFrameDuration]
        imageList = []
        for child in sorted(folderPath.iterdir()):
                childStr = str(child.resolve())
                log.info("Parsing item: " + childStr)
                if childStr.endswith('Timing.txt'):
                        timingList = ParseTiming(childStr)
                elif childStr.endswith(('.bmp', '.jpeg', 'jpg', '.png')):
                        imageList.append(pygame.image.load(childStr))
        
        log.info("Found " + str(len(imageList)) + " frames in " + str(folderPath.resolve()))
        return (imageList, timingList)

def LoadAnimations():
        Animations.clear()
        animationFolder = Path(animationPath)
        for folder in sorted(animationFolder.iterdir()):
                log.info("Loading folder: " + str(folder.resolve()))
                if folder.is_dir():
                        Animations.append(LoadFolder(folder))
        log.info("Found " + str(len(Animations)) + " animations total")

def ButtonPressed(channel):
    log.debug("Button has been pressed!")

GPIO.setup(gpioChannel, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#GPIO.add_event_detect(gpioChannel, GPIO.BOTH, callback=ButtonPressed, bouncetime=1000)

LoadAnimations()
firstFrame = Animations[CurrentAnimation][0][CurrentFrame]
screen.blit(firstFrame,(0,0))
pygame.display.update()
pygame.display.flip()
LastFrameChange = current_milli_time()

###Render Loop
while True:
        currentTime = current_milli_time()
        gpioDown = not GPIO.input(gpioChannel)
        if gpioDown:
                if ButtonIsDown:
                        totalTimeDown = currentTime - ButtonFirstWentDown
                        if totalTimeDown > ButtonHoldTimeForPower:
                                break
                else:
                        ButtonIsDown = True
                        ButtonFirstWentDown = currentTime
        else:
                if ButtonIsDown:
                        CurrentAnimation = CurrentAnimation+1
                        if CurrentAnimation >= len(Animations):
                                CurrentAnimation = 0
                ButtonIsDown = False
        
        animation = Animations[CurrentAnimation]
        frames = animation[0]
        frameTimes = animation[1]
        frameTime = defaultFrameDuration
        if CurrentFrame < len(frameTimes):
                frameTime = frameTimes[CurrentFrame]
        elif len(frameTimes) > 0:
                frameTime = frameTimes[-1]
        timeSinceLastFrame = currentTime - LastFrameChange
        if timeSinceLastFrame > frameTime:
                LastFrameChange = currentTime
                CurrentFrame = CurrentFrame + 1
                if CurrentFrame >= len(frames):
                        CurrentFrame = 0
                frame = frames[CurrentFrame]
                screen.blit(frame,(0,0))
                pygame.display.flip()
        time.sleep(MSPerFrame)
print("cleanup")
GPIO.cleanup()
quit()
