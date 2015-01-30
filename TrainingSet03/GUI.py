from Tkinter import *
import tkFileDialog, tkMessageBox
import datetime, os
from split_img import splitImage
from classify_single import classifySingle

class App:

    def __init__(self, master):
        self.master = master
        self.start()

    def start(self):
        self.master.title("Sensor Tex - Material Recognition Software")
        
        self.now = datetime.datetime.now()
        label01 = "Classify Material and Generate MCI Map"
        Label(self.master, text=label01).grid(row=0, column=1, sticky=W)
        
        Label(self.master, text="Input File: ").grid(row=1)
        self.fileloc = Entry(self.master)
        self.fileloc["width"] = 60
        self.fileloc.focus_set()
        self.fileloc.grid(row=1, column=1)
        
        self.open_file = Button(self.master, text="Browse...", command=self.browse_file)
        self.open_file.grid(row=1, column=2)
        
        Label(self.master, text="Is this image a mosaic? ").grid(row=3, sticky=N)
        MOSAIC = [
            ("Yes", "1"),
            ("No", "2")
        ]
        
        self.textvar = StringVar()
        self.textvar.set("1") #Initialize
        
        i = 3
        for text, mode in MOSAIC:
            self.adjustment = Radiobutton(self.master, text=text, variable=self.textvar, value=mode)
            self.adjustment.grid(row=i, column=1, sticky=W)
            i += 1
        
        self.submit = Button(self.master, text="EXECUTE", command=self.execute, fg="red")
        self.submit.grid(row=8, column=2, sticky=E)
        
    def browse_file(self):
        self.filename = tkFileDialog.askopenfilename(title="Open image...")
        self.fileloc.insert(0,self.filename ) #set the location to fileloc var

    def execute(self):
	if self.textvar.get()=="1":
		print "Mosaic"
		#splitImage(parse_arguments())
	elif self.textvar.get()=="2":
		print "Single image"
		#classifySingle(parse_arguments())
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
        
root = Tk()
app = App(root)
root.mainloop()
