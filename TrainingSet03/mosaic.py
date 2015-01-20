#import image_slicer
#image_slicer.slice('test_result10.png', 14)

from PIL import Image
import numpy as np
from scipy.stats import mode

def splitImage(filepath):
	im = Image.open(filepath)
	xsize, ysize = im.size
	#print im.size
	tempWindowSize = 32, 32
	halfWindowSize = (tempWindowSize[0]/2, tempWindowSize[1]/2)
	cover = 4
	stepSize = (tempWindowSize[0]/6, tempWindowSize[1]/6)
	mciPixels = np.empty((cover, cover, xsize, ysize))
	for xcenter in range(halfWindowSize[0], xsize-halfWindowSize[0]):
		for ycenter in range(halfWindowSize[1], ysize-halfWindowSize[1]):
			box = (xcenter-halfWindowSize[0], xcenter+halfWindowSize[0], ycenter-halfWindowSize[1], ycenter+halfWindowSize[1])
			windowWidth = subImage(box, im)
			#classify(windowWidth)
			#tempMCI = classify(windowWidth)
			#mciPixels[xcenter, ycenter, (xcenter-halfWindowSize[0]) - (xcenter+halfWindowSize[0]), (ycenter-halfWindowSize[1]) - (ycenter+halfWindowSize[1])] = tempMCI

	#for x in range(1, xsize):
		#for y in range(1, ysize):
			#mci[x,y] = mode(mciPixels, axis=0)


def subImage(box, im):
	region = im.crop(box)
	region.show()
	return region
		

print "---------------------"
splitImage("test.bmp")
