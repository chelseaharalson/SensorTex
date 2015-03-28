from Tkinter import *
import ttk
import tkFileDialog
from classify_single import *
#from split_img import splitImage
#from classify_single import classifySingle


CODEBOOK_FILE = 'codebook.file'
MODEL_FILE = 'trainingdata.svm.model'
#filename = '/Test_Training03/test000.png'

def parse_arguments():
    parser = argparse.ArgumentParser(description='classify images with a visual bag of words model')
    parser.add_argument('-c', help='path to the codebook file', required=False, default=CODEBOOK_FILE)
    parser.add_argument('-m', help='path to the model  file', required=False, default=MODEL_FILE)
    parser.add_argument('input_images', help='images to classify', nargs='+')
    args = parser.parse_args()
    return args

def execute():
  if textvar.get()=="1":
    print "Mosaic"
    #splitImage(parse_arguments())
  elif textvar.get()=="2":
    print "Single image"

    print filename
    classifySingle(filename)
  else:
    pass
    '''
    def start_processing(self):
        #print "start processing file..."
        try:
            #print self.fileloc.get()
            #print self.adj.get()
            tide = Converter()
            tide.set_input_file(self.fileloc.get())
            tide.set_adjustment(int(self.adj.get()))
            #tide.set_output_file("tide_%d%d%d%d%d%d.txt" % (self.now.year, self.now.month, self.now.day, self.now.hour, self.now.minute, self.now.second))
            tide.set_output_file(self.generate_filename())
            tide.process_file()
            tide.close()
            self.done_processing()
        except:
            #print "Unexpected error",
            tkMessageBox.showerror("Unexpected Error", sys.exc_info())

    def done_processing(self):
        tkMessageBox.showinfo("Successful", "'%s' created from '%s'. Adjustment: %s hour(s)" % (self.generate_filename(), self.filename,self.adj.get()))
        self.start()

    def generate_filename(self):
        return "%s/tide_%d%d%d%d%d%d.txt" % (os.path.dirname(self.fileloc.get()),self.now.year, self.now.month, self.now.day, self.now.hour, self.now.minute, self.now.second)
    '''

def calculate(*args):
    try:
        value = float(feet.get())
        meters.set((0.3048 * value * 10000.0 + 0.5)/10000.0)
    except ValueError:
        pass

def browse_file():
  filename = tkFileDialog.askopenfilename(title="Open image...")
  file_entry.insert(0,filename )
  return filename

def model_file():
  model_filename = tkFileDialog.askopenfilename(title="Specify Model File Location..")
  model_entry.insert(0,model_filename )

def codebook_file():
  codebook_filename = tkFileDialog.askopenfilename(title="Specify Codebook File Location...")
  codebook_entry.insert(0,codebook_filename )

root = Tk()
root.title("Sensor Tex - Material Recognition Software")

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

feet = StringVar()
meters = StringVar()

ttk.Button(mainframe, text="Browse..", command=browse_file).grid(column=4, row=1, sticky=E)
file_entry = ttk.Entry(mainframe, width=30, textvariable=file)
file_entry.grid(column=2, row=1, sticky=(W, E))
filename = browse_file()


ttk.Button(mainframe, text="Browse..", command=model_file).grid(column=4, row=2, sticky=E)
model_entry = ttk.Entry(mainframe, width=30, textvariable=file)
model_entry.grid(column=2, row=2, sticky=(W, E))

ttk.Button(mainframe, text="Browse..", command=codebook_file).grid(column=4, row=3, sticky=E)
codebook_entry = ttk.Entry(mainframe, width=30, textvariable=file)
codebook_entry.grid(column=2, row=3, sticky=(W, E))

ttk.Button(mainframe, text="Run", width=15, command=execute).grid(column=2, row=7)

ttk.Label(mainframe, text="Classify Material and Generate MCI Map").grid(column=2, row=0)
ttk.Label(mainframe, text="Input Image(s)").grid(column=1, row=1, sticky=W)
ttk.Label(mainframe, text="Model File").grid(column=1, row=2, sticky=W)
ttk.Label(mainframe, text="Codebook File").grid(column=1, row=3, sticky=W)
ttk.Label(mainframe, text="Is this image a mosaic? ").grid(column=1, row=5, sticky=N)
MOSAIC = [
    ("Yes", "1"),
    ("No", "2")
]

textvar = StringVar()
textvar.set("1") #Initialize

i = 5
for text, mode in MOSAIC:
    adjustment = Radiobutton(mainframe, text=text, variable=textvar, value=mode)
    adjustment.grid(row=i, column=2, sticky=W)
    i += 1

for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

#feet_entry.focus()
#root.bind('<Return>', calculate)

root.mainloop()
