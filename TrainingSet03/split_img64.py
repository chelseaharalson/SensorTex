from PIL import Image
import sys
import os
import glob
import numpy as np
from scipy.stats import mode
from classify_subwindows import classify
from progressbar import ProgressBar, Percentage, Bar, RotatingMarker, ETA, FileTransferSpeed
import threading

mci = []
maxProb = []
timer = 5

answer = None
def windowSize():
    global answer
    answer = raw_input("(Ex: For 64 x 64, enter 64.)\n")

def splitImage(args):
	print "---------------------"
	#print "Spliting up the image..."
	CURSOR_UP_ONE = '\x1b[1A'
	ERASE_LINE = '\x1b[2K'

	# get test image
	im = Image.open(args.input_images[0])
	xsize, ysize = im.size
	
	subWindowSize = 64, 64

	print "You have 5 seconds to select a sub-window size for " + sys.argv[5] + "."
	t = threading.Thread(target=windowSize)
	t.daemon = True
	t.start()
	t.join(5)
	if answer is None:
		print 
		print 'Timed out! Sub-window size will be set to 64 x 64.'
	else:
		if answer.isdigit():
			subWindowSize = int(answer), int(answer)
			print 'Sub-window size will be set to ' + answer + ' x ' + answer + '.'
		else:
			print 'Invalid input! Sub-window size will be set to 64 x 64.'
	
	overlapWindows = 4, 4
	halfWindowSize = (subWindowSize[0]/2, subWindowSize[1]/2)
	stepSize = (subWindowSize[0]/overlapWindows[0], subWindowSize[1]/overlapWindows[1])
	xcover = xsize-halfWindowSize[0]
	ycover = ysize-halfWindowSize[1]
	mciPixels = np.empty((overlapWindows[0], overlapWindows[1], xsize, ysize))
	mciPixels[:,:,:,:] = -1
	materialVote = 0
	hist = np.zeros(4)
	total = 0
	maxMaterials = 4
	mci = np.zeros((xsize, ysize))	#mci = np.empty((xsize, ysize))
	#mci[:,:] = 0
	maxProb = np.empty((xsize, ysize))	#maxProb = np.empty((xsize, ysize))
	#maxProb[:,:] = 0
	tempArray = np.zeros((ysize/stepSize[1],xsize/stepSize[0]))
	tempArray[:,:] = -1


	# clear out subwindows folder
	files = glob.glob('subwindows/*')
	for f in files:
		os.remove(f)

	# Windowing Progress Bar
	limit = len(range(halfWindowSize[0], xsize-halfWindowSize[0], stepSize[0])) * len(range(halfWindowSize[1], ysize-halfWindowSize[1], stepSize[1])) * 10
	window_widgets = ['Windowing: ', Percentage(), ' ', Bar(marker=RotatingMarker()), ' ', ETA(), ' ', FileTransferSpeed()]
	window_pbar = ProgressBar(widgets=window_widgets, maxval=limit).start()
	i = 0

	# iterate through subwindows
	for xcenter in range(halfWindowSize[0], xsize-halfWindowSize[0], stepSize[0]):
		for ycenter in range(halfWindowSize[1], ysize-halfWindowSize[1], stepSize[1]):				
			box = (xcenter-halfWindowSize[0], ycenter-halfWindowSize[1], xcenter+halfWindowSize[0], ycenter+halfWindowSize[1])
			subwindow = subImage(box, im)
			#subwindow.show()
			subwindowfname = "subwindows/subwindow_" + str(xcenter) + "_" + str(ycenter) + ".png"
			#subwindow.save(subwindowfname)
			#print "Subwindow file name: " + subwindowfname
			#print "---------------------"
			#sys.stdout = open(os.devnull, "w")
			tempMID = classify(subwindowfname, subwindow, args)
			#print str(tempMID)
			x = xcenter/stepSize[0]-2
			y = ycenter/stepSize[1]-2
			#print "x: " + str(x)
			#print "y: " + str(y)
			tempArray[y][x] = tempMID/40
			xIndex = (x) % overlapWindows[0]
			yIndex = (y) % overlapWindows[1]
			#print "xindex: " + str(xIndex) + "   yindex: " + str(yIndex)
			mciPixels[xIndex, yIndex, (xcenter-halfWindowSize[0]):(xcenter+halfWindowSize[0]), (ycenter-halfWindowSize[1]):(ycenter+halfWindowSize[1])] = tempMID
			#sys.stdout = sys.__stdout__
			#window_pbar.update(10*i+1)
			i = i + 1

	window_pbar.finish()

	# Material Vote Progress Bar
	limit = xsize * ysize
	mvote_widgets = ['Material Vote: ', Percentage(), ' ', Bar(marker=RotatingMarker()), ' ', ETA(), ' ', FileTransferSpeed()]
	mvote_pbar = ProgressBar(widgets=mvote_widgets, maxval=limit).start()

	for x in range(0, xsize):
		for y in range(0, ysize):
			mvote_pbar.update(x*ysize + y)				
			for z in range(0, len(hist)):
				hist[z] = 0
			# Tally material IDs
			for i in range(1, overlapWindows[0]):
				for j in range(1, overlapWindows[1]):
					materialVote = mciPixels[i,j,x,y]
					if(materialVote == -1):		# not classified
						continue
					total = total + 1
					hist[materialVote/40] = hist[materialVote/40] + 1
					
			maxID = 0
			materialVote = hist[0]

			for k in range (1, maxMaterials):
				if(hist[k] > materialVote):
					maxID = k
					materialVote = hist[k]

			mci[x,y] = maxID * 40

			maxProb[x,y] = materialVote/total
			#print "MaxProb at " +str(x)+ ", "+str(y) + " for " + str(mci[x,y]) +" : " + str(maxProb[x,y])

	mvote_pbar.finish()
	im = Image.open(sys.argv[5])
	#im.show()
	print "TEMP ARRAY: "
	print(tempArray[1:28,1:18])
	generateMCI(mci)
	temp = np.ravel(mci)
	temp = np.unique(temp)
	f = open('material_IDs.dat', 'r')
	l = f.readline()
	num, name = l.split("-")
	num1 = int(num)
	name1 = name.rstrip("\n")
	l = f.readline()
	num, name = l.split("-")
	num2 = int(num)
	name2 = name.rstrip("\n")
	l = f.readline()
	num, name = l.split("-")
	num3 = int(num)
	name3 = name.rstrip("\n")
	l = f.readline()
	num, name = l.split("-")
	num4 = int(num)
	name4 = name.rstrip("\n")
	output = ""
	for i in temp:
		if i == num1:
			output = output + name1 + ' '
		if i == num2:
			output = output + name2 + ' '
		if i == num3:
			output = output + name3 + ' '
		if i == num4:
			output = output + name4 + ' '
	print sys.argv[5] + '   Classification: ' + output
	return sys.argv[5] + '   Classification: ' + output		

def subImage(box, im):
	region = im.crop(box)
	return region

def generateMCI(mciMap):
	newImage = Image.new('RGBA', (mciMap.shape))
	pixels = newImage.load() # create the pixel map
	for i in range(0, newImage.size[0]):    # for every pixel:
	    for j in range(0, newImage.size[1]):
		pixels[i,j] = (int(mciMap[i,j]), int(mciMap[i,j]), int(mciMap[i,j]), 255) # set the color accordingly
	#newImage.show()
	#pix_val = list(newImage.getdata())
	#print pix_val

	for infile in sys.argv[5:]:
		fname1 = os.path.splitext(infile)[0] + "_mci"

	newImage.save(fname1, "tiff")

	return pixels
