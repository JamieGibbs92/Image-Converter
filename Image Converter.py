import PIL.Image
from tkinter import filedialog
from tkinter import *
from tkinter import messagebox
import os
import time

##### Classes #####
class Application(Frame):
    def __init__(self,master):
        super(Application,self).__init__(master)
        self.grid()
        self.createWidgets()

    def createWidgets(self):
        """Creates labels and buttons for use in app"""
        # Create introduction label
        Label(self,
                text = "Welcome to the image converter program.\n  This program allows you to convert a single image or directory of images to the JPG, BMP, PNG or ICO file formats."
              ).grid(columnspan = 8, pady = 5)
        # Create initial option buttons for type of conversion (single image, or directory)
        self.singleImageBtn = Button(self, text = "Browse for Single Image",command = lambda : self.getFile("Select Image File to Convert",VALIDFILETYPES))
        self.singleImageBtn.grid(row = 1, column = 0, columnspan = 4)
        
        self.DirBtn = Button(self, text = "Browse for Directory of Images", command = lambda : self.getDirectory("Select Directory of Images to Convert"))
        self.DirBtn.grid(row = 1, column = 2, columnspan = 4)
        # Create status label for each button state
        self.imageStatus = Label(self,text = "Not Selected", foreground = "Red", font = "Helvetica 8 bold" )
        self.imageStatus.grid(row = 2, column = 0, columnspan = 4, pady = 5)

        self.directoryStatus = Label(self,text = "Not Selected", foreground = "Red", font = "Helvetica 8 bold")
        self.directoryStatus.grid(row = 2, column = 2, columnspan = 4, pady = 5)
        # Create button to select save directory for converted image
        self.saveDirBtn1 = Button(self, text = "Select Save Directory", state = DISABLED, command = lambda : self.getSaveDirectory("Select Save Directory for Images"))
        self.saveDirBtn1.grid(row = 3, column = 0, columnspan = 4, pady = 5)
        
        self.saveDirStatus1 = Label(self,text = "Not Selected", foreground = "Red", font = "Helvetica 8 bold")
        self.saveDirStatus1.grid(row = 4, column = 0, columnspan = 4, pady = 5)

        self.saveDirBtn2 = Button(self, text = "Select Save Directory", state = DISABLED, command = lambda : self.getSaveDirectory("Select Save Directory for Images"))
        self.saveDirBtn2.grid(row = 3, column = 2, columnspan = 4, pady = 5)
        
        self.saveDirStatus2 = Label(self,text = "Not Selected", foreground = "Red", font = "Helvetica 8 bold")
        self.saveDirStatus2.grid(row = 4, column = 2, columnspan = 4, pady = 5)
        
        # Create convert label and radio button options
        Label(self, text = "File type to convert to:", bd = 10
              ).grid(row = 5, column = 0, sticky = W)
        self.convertFileType = StringVar()
        self.convertFileType.set(None)
        fileTypes = ["JPG","BMP","PNG","ICO"]
        column = 1
        for i in fileTypes:
            Radiobutton(self, text = i, value = "." + i.lower(), variable = self.convertFileType
                        ).grid(row = 5, column = column, pady = 10)
            column += 1

        # Create Convert button
        self.convertBtn = Button(self, text = "Convert", font = "Helvetica 8 bold", command = self.validateFileTypeSelection, state = DISABLED)
        self.convertBtn.grid(row = 6, column = 0,  columnspan = 8)
        
        # Create results label, reset button and textbox to display conversion results and other messages
        Label(self, text = "Results", font = "Helvetica 8 bold", bd = 10
              ).grid(row = 7, column = 0, sticky = W)
        Button(self, text = "Reset",command = self.clearApp
               ).grid(row = 7, column = 6, sticky = E, pady = 5)
        self.results = Text(self, width = 75, height = 15, wrap = WORD)
        self.results.grid(row = 8, column = 0, columnspan = 8, padx = 3, pady = 3, sticky = W)

    def clearApp(self):
        """Clears all selections from the program"""
        self.results.delete(0.0,END)
        self.convertFileType.set(None)
        self.singleImageBtn.configure(state = ACTIVE)
        self.DirBtn.configure(state = ACTIVE)
        self.saveDirBtn1.configure(state = DISABLED)
        self.saveDirBtn2.configure(state = DISABLED)
        self.imageStatus.configure (text = "Not Selected", foreground = "Red", font = "Helvetica 8 bold")
        self.directoryStatus.configure (text = "Not Selected", foreground = "Red", font = "Helvetica 8 bold")
        self.saveDirStatus1.configure (text = "Not Selected", foreground = "Red", font = "Helvetica 8 bold")
        self.saveDirStatus2.configure (text = "Not Selected", foreground = "Red", font = "Helvetica 8 bold")
        self.fileName = None
        self.imageDirectory = None
        self.saveDir = None
        self.convertBtn.configure(state = DISABLED)
        
    def clearText(self):
        """Clears all log information from Results text box"""
        self.results.delete(0.0,END)

    def validateFileTypeSelection(self):
        # Ensure a file type radio button has been selected
        fileType = self.convertFileType.get()
        if fileType != "None":
            if self.fileName:
                self.convertSingleFile(fileType)
            elif self.imageDirectory:
                self.convertFileInDir(fileType)
        else:
            self.results.insert(END,"\nNo file type selected. Please select one of an option, and try again.")
    

    def getFile(self,dialogTitle, VALIDFILETYPES):
        """Opens the browse file dialog to get a single file from user. Accepts dialog title and browsable file types."""
        self.DirBtn.configure(state = DISABLED)
        self.saveDirBtn2.configure(state = DISABLED)
        self.clearText()
        self.results.insert(END,"Opening file browser...")
        # Open file browser to locate image to convert
        defaultDirectory = os.path.expanduser('~\\Documents')
        self.fileName = filedialog.askopenfilename(initialdir = defaultDirectory,title = dialogTitle, filetypes = VALIDFILETYPES)
        if not self.fileName:
            self.results.insert(END,"\nCancelling...")
            self.DirBtn.configure(state = ACTIVE)
        else:
            self.imageStatus.configure (text = "Image Selected", foreground = "Green", font = "Helvetica 8 bold")
            self.results.insert(END,"\nImage selected...")
            self.saveDirBtn1.configure(state = ACTIVE)

    def getDirectory(self,dialogTitle):
        """Opens the browse directory dialog to get a directory. Accepts dialog title."""
        self.singleImageBtn.configure(state = DISABLED)
        self.saveDirBtn1.configure(state = DISABLED)
        self.clearText()
        self.results.insert(END,"Opening directory browser...")
        # Open directory browser
        defaultDirectory = os.path.expanduser('~\\Desktop')
        self.imageDirectory = filedialog.askdirectory(initialdir = defaultDirectory,title = dialogTitle)
        if not self.imageDirectory:
            self.results.insert(END,"\nCancelling...")
            self.singleImageBtn.configure(state = ACTIVE)
            self.saveDirBtn1.configure(state = ACTIVE)

    def getSaveDirectory(self,dialogTitle):
        """Opens the browse directory dialog to get save directory. Accepts dialog title."""
        self.results.insert(END,"\nOpening directory browser...")
        # Open directory browser
        defaultDirectory = os.path.expanduser('~\\Desktop')
        self.saveDir = filedialog.askdirectory(initialdir = defaultDirectory,title = dialogTitle)
        if not self.saveDir:
            self.results.insert(END,"\nCancelling...")
        else:
            self.saveDirStatus1.configure (text = "Directory Selected", foreground = "Green", font = "Helvetica 8 bold")
            self.results.insert(END,"\nDirectory selected...")
            self.convertBtn.configure(state = ACTIVE)

    def convertSingleFile(self, fileType):
            # Remove file extension from image
            splitImage = os.path.split(self.fileName)
            splitImage = os.path.splitext(splitImage[1])
            # Assign full predicted image save location
            fullPath = str(self.saveDir) + "/" + splitImage[0] + fileType
            # Check if file already exists
            if os.path.exists(fullPath):
                result = messagebox.askyesno("Image Converter","That file already exists. Overwrite?")
                if result == True:
                    # Convert and save image into chosen directory
                    self.results.insert(END,"\nConverting file...")
                    self.results.insert(END,fullPath)
                    image = PIL.Image.open(self.fileName)
                    image.save(fullPath)
                    messagebox.showinfo(message = "Files Converted Successfully",title = "Image Converter",)
            else:
                # Convert and save image into chosen directory
                self.results.insert(END,"\nConverting file...")
                self.results.insert(END,fullPath)
                image = PIL.Image.open(self.fileName)
                image.save(fullPath)
                messagebox.showinfo(message = "Files Converted Successfully",title = "Image Converter",)

    def convertFileInDir(fileType):
        for imageFile in os.listdir(self.imageDirectory):
                if imageFile.endswith(('.jpg', '.bmp','png','ico')):
                    fullPath = self.imageDirectory + "/" + imageFile
                    splitImage = os.path.split(imageFile)
                    splitImageExt = os.path.splitext(splitImage[1])
                    # Convert and save image into chosen directory
                    fullSavePath = self.saveDir + "/" + splitImageExt[0] + fileType
                    # Check if file already exists
                    if os.path.exists(fullSavePath):
                        result = messagebox.askyesno("Image Converter",splitImageExt[0] + fileType + "\nalready exists. Overwrite?")
                        if result == True:
                            # Convert and save image into chosen directory
                            self.results.insert(END,"\nConverting file...")
                            self.results.insert(END,fullPath)
                            image = PIL.Image.open(fullPath)
                            image.save(fullSavePath)
                        else:
                            self.results.insert(END,"\nSkipping file...")
                            time.sleep(0.5)
                    else:
                        # Convert and save image into chosen directory
                        print (fullSavePath)
                        image = PIL.Image.open(fullPath)
                        image.save(fullSavePath)
        messagebox.showinfo(message = "Files Converted Successfully",title = "Image Converter")

##### Functions #####

def createRootWindow():
    """Creates the main root window"""
    # Create Tk root window
    root = Tk()
    # Define root window options
    root.title("Image Converter")
    root.geometry("620x530")
    # Prevent user from resizing or maximising window
    root.resizable(width=False, height=False)
    # Define window icon
    root.iconbitmap('Image Converter.ico')
    return root
                
##### Global Variables #####

#set valid file types for image browser
VALIDFILETYPES = (("JPG Files","*.jpg"),("BMP Files","*.bmp"),("PNG Files","*.png"),("ICO Files","*.ico"))

# Main
root = createRootWindow()
app = Application(root)
root.mainloop()
