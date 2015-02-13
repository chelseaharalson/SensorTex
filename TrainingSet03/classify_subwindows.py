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

def parse_arguments():
    parser = argparse.ArgumentParser(description='classify images with a visual bag of words model')
    parser.add_argument('-c', help='path to the codebook file', required=False, default=CODEBOOK_FILE)
    parser.add_argument('-m', help='path to the model  file', required=False, default=MODEL_FILE)
    parser.add_argument('input_images', help='images to classify', nargs='+')
    args = parser.parse_args()
    return args

# Uncomment @profile if want to do a profile by adding in: -m memory_profiler
#@profile
def classify(imgfname, subwindow, args):
	#print "---------------------"
	#print "## extract Sift features"
	all_files = []
	all_files_labels = {}
	all_features = {}

	args = parse_arguments()
	model_file = args.m
	codebook_file = args.c
	fnames = args.input_images
	fnames[0] = imgfname
	all_features = extractSift(fnames, subwindow)
	for i in fnames:
	    all_files_labels[i] = 0  # label is unknown

	#print "---------------------"
	#print "## loading codebook from " + codebook_file
	with open(codebook_file, 'rb') as f:
	    codebook = load(f)

	#print "---------------------"
	#print "## computing visual word histograms"
	all_word_histgrams = {}
	for imagefname in all_features:
	    word_histgram = computeHistograms(codebook, all_features[imagefname])
	    all_word_histgrams[imagefname] = word_histgram

	#print "---------------------"
	#print "## write the histograms to file to pass it to the svm"
	nclusters = codebook.shape[0]
	writeHistogramsToFile(nclusters,
		              all_files_labels,
		              fnames,
		              all_word_histgrams,
		              HISTOGRAMS_FILE)

	#print "---------------------"
	#print "## test data with svm"
	#print libsvm.test(HISTOGRAMS_FILE, model_file)

	result = str(libsvm.test(HISTOGRAMS_FILE, model_file))
	if result == "[0]":
		mID = 0
		resultText = "Not recognized"
		#print("Not recognized")
	if result == "[1]":
		mID = 40
		resultText = "Brick"
		#print("Brick")
	if result == "[2]":
		mID = 80
		resultText = "Metal"
		#print("Metal")
	if result == "[3]":
		mID = 120
		resultText = "Wood"
		#print("Wood")
	return mID
