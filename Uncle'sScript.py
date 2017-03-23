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
animationPath = 'Uncle'sShaders'
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
LastFrameChange = current_milli_time
FPS = 30.0
MSPerFrame = 1000.0/FPS
### Custom Colors
bg = 50,65,60

wi=screen.get_width()
he=screen.get_height()
log.debug("Resolution: " + str(wi) + "x" + str(he))
pygame.draw.rect(screen,bg,[0,0,35,64])
pygame.display.update()

def ParseTiming(filePath)
	timingList = []
	f = open(filePath, 'r')
	for line in f:
		timingList.append(int(line))
	f.close()
	log.info("Found " + len(timingList) + " timing values in " + filePath)
	return timingList
	
def LoadFolder(folderPath)
	timingList = [defaultFrameDuration]
	imageList = []
	for child in folderPath.iter_dir()
		childStr = str(child.resolve())
		if childStr == 'Timing.txt':
			timingList = ParseTiming(childStr)
		elif childStr.endswith(('.bmp', '.jpeg', 'jpg', '.png'))
			imageList.append(pygame.image.load(childStr))
	
	log.info("Found " + len(imageList) + " frames in " + filePath)
	return (imageList, timingList)

def LoadAnimations()
	Animations.clear()
	animationFolder = Path(animationPath)
	for folder in animationFolder.iter_dir():
		Animations.append(LoadFolder(folder))
	log.info("Found " + len(Animations) + " animations total")

def ButtonPressed(channel):
    log.debug("Button has been pressed!")

GPIO.setup(gpioChannel, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(gpioChannel, GPIO.BOTH, callback=ButtonPressed, bouncetime=1000)

LoadAnimations()

###Render Loop
while True:
	gpioDetected = GPIO.input(gpioChannel)
	animation = Animations[CurrentAnimation]
	frames = animation[0]
	frameTimes = animation[1]
	frameTime = defaultFrameDuration
	if CurrentFrame < len(frameTimes):
		frameTime = frameTimes[CurrentFrame]
	elif len(frameTimes) > 0:
		frameTime = frameTimes[-1]
	
	currentTime = current_milli_time
	if currentTime - LastFrameChange > frameTime:
		LastFrameChange = currentTime
		CurrentFrame = CurrentFrame + 1
		if CurrentFrame >= len(frames):
			CurrentFrame = 0
		frame = frames[CurrentFrame]
		screen.blit(frame,(wi,he))
		pygame.display.update()
	time.sleep(MSPerFrame)