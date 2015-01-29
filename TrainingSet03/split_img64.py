from PIL import Image
import sys
import os
import glob
import numpy as np
from scipy.stats import mode
from classify_subwindows import classify
from classify_single import newFilename

mci = []
maxProb = []

def splitImage(args):
	print "---------------------"
	print "Spliting up the image..."

	# get test image
	im = Image.open(args.input_images[0])
	xsize, ysize = im.size
	
	subWindowSize = 64, 64
	overlapWindows = 4, 4
	halfWindowSize = (subWindowSize[0]/2, subWindowSize[1]/2)
	stepSize = (subWindowSize[0]/overlapWindows[0], subWindowSize[1]/overlapWindows[1])
	xcover = xsize-halfWindowSize[0]
	ycover = ysize-halfWindowSize[1]
	mciPixels = np.empty((overlapWindows[0], overlapWindows[1], xsize, ysize))
	mciPixels[:,:,:,:] = -1
	maximalVote = 0
	hist = np.zeros(4)
	total = 0
	maxMaterials = 4
	mci = np.empty((xsize, ysize))
	mci[:,:] = 0
	maxProb = np.empty((xsize, ysize))
	maxProb[:,:] = 0
	tempArray = np.zeros((ysize/stepSize[1]-4,xsize/stepSize[0]-4))
	print str(ysize/stepSize[1]-2)
	print str(xsize/stepSize[0]-2)

	# clear out subwindows folder
	files = glob.glob('subwindows/*')
	for f in files:
		os.remove(f)

	# iterate through subwindows
	for xcenter in range(halfWindowSize[0], xsize-halfWindowSize[0], stepSize[0]):
		for ycenter in range(halfWindowSize[1], ysize-halfWindowSize[1], stepSize[1]):				
			box = (xcenter-halfWindowSize[0], ycenter-halfWindowSize[1], xcenter+halfWindowSize[0], ycenter+halfWindowSize[1])
			subwindow = subImage(box, im)
			#subwindow.show()
			subwindowfname = "subwindows/subwindow_" + str(xcenter) + "_" + str(ycenter) + ".png"
			subwindow.save(subwindowfname)
			#print "Subwindow file name: " + subwindowfname
			#print "---------------------"
			tempMID = classify(subwindowfname, args)
			#print str(tempMID)
			x = xcenter/stepSize[0]
			y = ycenter/stepSize[1]
			#print "x: " + str(x)
			#print "y: " + str(y)
			tempArray[y-2][x-2] = tempMID/40
			mciPixels[x % overlapWindows[0], y % overlapWindows[1], (xcenter-halfWindowSize[0]):(xcenter+halfWindowSize[0]), (ycenter-halfWindowSize[1]):(ycenter+halfWindowSize[1])] = tempMID

	# find mode
	print "Determining maximal vote"
	print "---------------------"
	for x in range(1, xsize):
		for y in range(1, ysize):
			for i in range(1, overlapWindows[0]):
				for j in range(1, overlapWindows[1]):
					maximalVote = mciPixels[i][j][x][y]
					if(maximalVote == -1):		# not classified
						continue
					total = total + 1
					hist[maximalVote/40] = hist[maximalVote/40] + 1

			maxID = 0
			maximalVote = hist[0]

			for k in range (1, maxMaterials):
				if(hist[k] > maximalVote):
					maxID = k
					maximalVote = hist[k]

			mci[x][y] = maxID * 40
			maxProb[x][y] = maximalVote/total
	im = Image.open(sys.argv[5])
	im.show()
	print "TEMP ARRAY: "
	print(tempArray[1:28,1:18])
	generateMCI(mci)
			

def subImage(box, im):
	region = im.crop(box)
	return region

def generateMCI(mciMap):
	newImage = Image.new('RGB', (mciMap.shape), "black")
	pixels = newImage.load() # create the pixel map
	for i in range(newImage.size[0]):    # for every pixel:
	    for j in range(newImage.size[1]):
		#print(mciMap[i,j])
		pixels[i,j] = (int(mciMap[i,j]), int(mciMap[i,j]), int(mciMap[i,j]), 255) # set the color accordingly
	newImage.show()
	fname = "_mosaic_mci"
	filename = newFilename(fname)
	newImage.save(filename)
	return pixels
