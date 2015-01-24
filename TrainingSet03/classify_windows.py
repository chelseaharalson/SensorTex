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

HISTOGRAMS_FILE = 'testdata.svm'
CODEBOOK_FILE = 'codebook.file'
MODEL_FILE = 'trainingdata.svm.model'

def draw_text_with_halo(img, position, text, font, col, halo_col):
    halo = Image.new('RGBA', img.size, (0, 0, 0, 0))
    ImageDraw.Draw(halo).text(position, text, font = font, fill = halo_col)
    blurred_halo = halo.filter(ImageFilter.BLUR)
    ImageDraw.Draw(blurred_halo).text(position, text, font = font, fill = col)
    return Image.composite(img, blurred_halo, ImageChops.invert(blurred_halo))

#Need natural sort to avoid having the list sorted as such:
#['./folder1.txt', './folder10.txt', './folder2.txt', './folder9.txt']
def sorted_nicely(strings):
    "Sort strings the way humans are said to expect."
    return sorted(strings, key=natural_sort_key)

def natural_sort_key(key):
    import re
    return [int(t) if t.isdigit() else t for t in re.split(r'(\d+)', key)]

def newFilename(fname):
	filename = "test_result" + fname + ".png" #default file name
	#if it does find the last count
	if(os.path.exists(filename)):
		result_file = sorted_nicely( glob.glob("./test_result" + fname + "[0-9]*.png"))
		if(len(result_file)==0):
		        filename="test_result" + fname + "1.png"
		else:
		        last_result = result_file[-1]
		        number = re.search( "test_result" + fname + "([0-9]*).png",last_result).group(1)
		        filename="test_result" + fname + "%i.png"%+(int(number)+1)
	return filename


def parse_arguments():
    parser = argparse.ArgumentParser(description='classify images with a visual bag of words model')
    parser.add_argument('-c', help='path to the codebook file', required=False, default=CODEBOOK_FILE)
    parser.add_argument('-m', help='path to the model  file', required=False, default=MODEL_FILE)
    parser.add_argument('input_images', help='images to classify', nargs='+')
    args = parser.parse_args()
    return args


def classify(imgfname, args):
	#print "---------------------"
	#print "## extract Sift features"
	all_files = []
	all_files_labels = {}
	all_features = {}

	args = parse_arguments()
	model_file = args.m
	codebook_file = args.c
	fnames = args.input_images	# list of img file names
	fnames[0] = imgfname		# still working on this, getting strange errors
	all_features = extractSift(fnames)
	for i in fnames:
	    all_files_labels[i] = 0  # label is unknown

	#print "---------------------"
	#print "## loading codebook from " + codebook_file
	with open(codebook_file, 'rb') as f:
   		codebook = load(f)
	#print "---------------------"
	#print "## test data with svm"
	#print libsvm.test(HISTOGRAMS_FILE, model_file)


	result = str(libsvm.test(HISTOGRAMS_FILE, model_file))
	if result == "[0]":
		mID = 0
		resultText = "Not recognized"
		print("Not recognized")
	if result == "[1]":
		mID = 40
		resultText = "Brick"
		print("Brick")
	if result == "[2]":
		mID = 120
		resultText = "Metal"
		print("Metal")
	if result == "[3]":
		mID = 200
		resultText = "Wood"
		print("Wood")

	'''
	im = Image.open(sys.argv[5])
	font = ImageFont.truetype("TrebuchetMSBold.ttf", 25)

	text_col = (0, 255, 0) # bright green
	halo_col = (0, 0, 0)   # black
	i2 = draw_text_with_halo(im, (5, 5), resultText, font, text_col, halo_col)
	i2.show()

	fname1 = ""
	fname2 = "_mci"

	filename1 = newFilename(fname1)
	filename2 = newFilename(fname2)

	i2.save(filename1)

	pixels = i2.load() # create the pixel map

	# generate mci map
	for i in range(i2.size[0]):    # for every pixel:
	    for j in range(i2.size[1]):
		pixels[i,j] = (mID, mID, mID, 255) # set the colour accordingly

	i2.show()
	i2.save(filename2)
	'''

	return mID

#classify()
