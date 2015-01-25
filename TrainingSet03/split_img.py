from PIL import Image
import numpy as np
from scipy.stats import mode

from classify_subwindows import classify

def parse_arguments():
    parser = argparse.ArgumentParser(description='classify images with a visual bag of words model')
    parser.add_argument('-c', help='path to the codebook file', required=False, default=CODEBOOK_FILE)
    parser.add_argument('-m', help='path to the model  file', required=False, default=MODEL_FILE)
    parser.add_argument('input_images', help='images to classify', nargs='+')
    args = parser.parse_args()
    return args

def splitImage(args):
	print "---------------------"
	print "Spliting up the image..."

	# get test image
	im = Image.open(args.input_images[0])
	xsize, ysize = im.size

	subWindowSize = 32, 32
	halfWindowSize = (subWindowSize[0]/2, subWindowSize[1]/2)
	stepSize = (subWindowSize[0]/8, subWindowSize[1]/8)
	xcover = xsize-halfWindowSize[0]
	ycover = ysize-halfWindowSize[1]
	mciPixels = np.empty((xcover, ycover, xsize, ysize))
	mciMode = []

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
			mciPixels[xcenter, ycenter, (xcenter-halfWindowSize[0]):(xcenter+halfWindowSize[0]), (ycenter-halfWindowSize[1]):(ycenter+halfWindowSize[1])] = tempMID
	
	print "Finding mode"
	print "---------------------"
	for row in mciPixels:
		findMode = mode(row, axis=0)
		mciMode.append(findMode[0])
	print(mciMode)


	'''
	data = np.arange(200).reshape((mciPixels))
	with file('arrayOutput.txt', 'w') as outfile:
		for data_slice in data:
			np.savetxt(outfile, data_slice, fmt='%-7.2f')
			outfile.write('# New slice\n')
	'''
	'''
	for x in range(1, xsize):
		for y in range(1, ysize):
			mci[x,y] = mode(mciPixels, axis=0)
			print(mci[x,y])
	'''

def subImage(box, im):
	region = im.crop(box)
	return region
