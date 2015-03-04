import libsvm
import argparse
from cPickle import load
from learn import extractSift, computeHistograms, writeHistogramsToFile
from PIL import Image
import sys
import ImageChops, ImageDraw, ImageFont, ImageFilter
import os
import glob
import re
import sys
import time

from split_img64 import splitImage
from classify_single import classifySingle

HISTOGRAMS_FILE = 'testdata.svm'
CODEBOOK_FILE = 'codebook.file'
MODEL_FILE = 'trainingdata.svm.model'

def parse_arguments():
    parser = argparse.ArgumentParser(description='classify images with a visual bag of words model')
    parser.add_argument('-c', help='path to the codebook file', required=False, default=CODEBOOK_FILE)
    parser.add_argument('-m', help='path to the model  file', required=False, default=MODEL_FILE)
    parser.add_argument('input_images', help='images to classify', nargs='+')
    args = parser.parse_args()
    return args

#print  sys.argv[5]
startTime = time.time()

if  os.path.exists(sys.argv[5]):
	if  os.path.isdir(sys.argv[5]):
		directory = sys.argv[5]
		files = os.listdir(directory)
		answer = raw_input("Are the " + str(len(files)) + " images located in " + directory
+ " considered to be mosaics? Please type 'y' or 'n' and then press enter. ")
		if answer == 'y':
			for i in files:
				sys.argv[5] = os.path.join(directory, i)
				splitImage(parse_arguments())	#mosaic
				os.remove(sys.argv[5] + ".sift")
		elif answer == 'n':
			for i in files:
				sys.argv[5] = os.path.join(directory, i)
				classifySingle(parse_arguments())	#single image
				os.remove(sys.argv[5] + ".sift")
		else:
			print "Please type 'y' or 'n'. "
	else:
		answer = raw_input("Is this image a mosaic? Please type 'y' or 'n' and then press enter. ")
		if answer == 'y':
			splitImage(parse_arguments())	#mosaic
		elif answer == 'n':
			classifySingle(parse_arguments())	#single image
		else:
			print "Please type 'y' or 'n'. "
		os.remove(sys.argv[5] + ".sift")
else:
	print  sys.argv[5] + " is not a valid path. The application will now shut down."

elapsedTime = time.time() - startTime
print "Total run time " + str(elapsedTime) + " sec"

