# SensorTex

### Learning:
    python learn.py -d path_to_folders_with_images 

### Classifying:
    python classify.py -c path_to_folders_with_images/codebook.file -m path_to_folders_with_images/trainingdata.svm.model images_you_want_to_classify

Example run for classifying:

python classify_gui.py -c Training01codebook.file -m Training01trainingdata.svm.model Test_Training01/p3.png

python classify_gui.py -c Training02codebook.file -m Training02trainingdata.svm.model Test_Training02/p4.png


### Prerequisites:

To install the necessary libraries run following code from working directory:

    # installing libsvm
    wget -O libsvm.tar.gz http://www.csie.ntu.edu.tw/~cjlin/cgi-bin/libsvm.cgi?+http://www.csie.ntu.edu.tw/~cjlin/libsvm+tar.gz
    tar -xzf libsvm.tar.gz
    mkdir libsvm
    cp -r libsvm-*/* libsvm/
    rm -r libsvm-*/
    cd libsvm
    make
    cp tools/grid.py ../grid.py
    cd ..
    
    # installing sift
    wget http://www.cs.ubc.ca/~lowe/keypoints/siftDemoV4.zip
    unzip siftDemoV4.zip
    cp sift*/sift sift
    

#### Notes
If you get an `IOError: SIFT executable not found` error, try `sudo apt-get install libc6-i386`. `sift` is a 32Bit executable and you need to install additional libraries to make it run on 64Bit systems.
    
### Install these Python libraries:

To install the necessary libraries run following code from working directory:

    # Numpy, Scipy, and Matplotlib
    sudo apt-get install python-numpy python-scipy python-matplotlib
    
    # Python Imaging Library:
    sudo apt-get install python-imaging imagemagick
