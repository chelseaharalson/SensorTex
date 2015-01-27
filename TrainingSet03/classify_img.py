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

from split_img import splitImage
from classify_single import classifySingle

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


answer = raw_input("Is this image a mosaic? Please type 'y' or 'n' and then press enter. ")
if answer == 'y':
	splitImage(parse_arguments())	#mosaic
elif answer == 'n':
	classifySingle(parse_arguments())	#single image
else:
	print "Please type 'y' or 'n'. "
