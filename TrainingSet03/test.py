import os
import glob

files = glob.glob('subwindows/*')
for f in files:
	os.remove(f)