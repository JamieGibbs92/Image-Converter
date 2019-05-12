import PIL.Image
from PIL import ImageTk
from tkinter import filedialog
from tkinter import *
from tkinter import messagebox
import os

##### Classes #####
class Application(Frame):
    def __init__(self,master):
        """An application used to convert images or other image formats"""
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
        self.singleImageBtn = Button(self, text = "Browse for Single Image",
                                     command = lambda : self.getFile("Select Image File to Convert",VALIDFILETYPES),cursor = "hand2")
        self.singleImageBtn.grid(row = 1, column = 0, columnspan = 4)

        self.dirBtn = Button(self, text = "Browse for Directory of Images", command = lambda : self.getDirectory("Select Directory of Images to Convert"), cursor = "hand2")
        self.dirBtn.grid(row = 1, column = 2, columnspan = 4)

        # Create image preview button
        self.previewImageBtn = Button(self, text = "Preview Image", command = self.previewImage, state = DISABLED)
        self.previewImageBtn.grid(row = 1, column = 0)
        
        # Create status label for each button state
        self.imageStatus = Label(self,text = "Not Selected", foreground = "Red", font = "Helvetica 8 bold" )
        self.imageStatus.grid(row = 2, column = 0, columnspan = 4, pady = 5)

        self.directoryStatus = Label(self,text = "Not Selected", foreground = "Red", font = "Helvetica 8 bold")
        self.directoryStatus.grid(row = 2, column = 2, columnspan = 4, pady = 5)
        
        # Create button for selecting save directory for image and directory options
        self.saveDirBtn1 = Button(self, text = "Select Save Directory", state = DISABLED, command = lambda : self.getSaveDirectory("Select Save Directory for Images", "Image"))
        self.saveDirBtn1.grid(row = 3, column = 0, columnspan = 4, pady = 5)
        
        self.saveDirBtn2 = Button(self, text = "Select Save Directory", state = DISABLED, command = lambda : self.getSaveDirectory("Select Save Directory for Images", "Directory"))
        self.saveDirBtn2.grid(row = 3, column = 2, columnspan = 4, pady = 5)

        # Create status labels for each save directory button.
        self.saveDirStatus1 = Label(self,text = "Not Selected", foreground = "Red", font = "Helvetica 8 bold")
        self.saveDirStatus1.grid(row = 4, column = 0, columnspan = 4, pady = 5)
        
        self.saveDirStatus2 = Label(self,text = "Not Selected", foreground = "Red", font = "Helvetica 8 bold")
        self.saveDirStatus2.grid(row = 4, column = 2, columnspan = 4, pady = 5)
        
        # Create label for convertible file types
        Label(self, text = "File type to convert to:", bd = 10
              ).grid(row = 5, column = 0, sticky = W)
        
        # Create radio button options for file types available for conversion
        self.convertFileType = StringVar()
        self.convertFileType.set(None)
        fileTypes = ["JPG","BMP","PNG","ICO"]
        column = 1
        for i in fileTypes:
            Radiobutton(self, text = i, value = "." + i.lower(), variable = self.convertFileType, cursor = "hand2"
                        ).grid(row = 5, column = column, pady = 10)
            column += 1

        # Create Convert button
        self.convertBtn = Button(self, text = "Convert", font = "Helvetica 8 bold", command = self.validateFileTypeSelection, state = DISABLED)
        self.convertBtn.grid(row = 6, column = 0,  columnspan = 8)
                
        # Create results label
        Label(self, text = "Results", font = "Helvetica 8 bold", bd = 10
              ).grid(row = 7, column = 0, sticky = W)

        # Create results text box to display results of conversion, and accompanying scrollbar
        self.scrollbar = Scrollbar(self)
        self.scrollbar.grid(row = 8, column = 8, ipady = 100)
        
        self.results = Text(self, width = 75, height = 15, wrap = WORD, yscrollcommand = self.scrollbar.set)
        self.results.grid(row = 8, column = 0, columnspan = 8)
        self.scrollbar.config(command = self.results.yview)

        # Create reset button for application
        Button(self, text = "Reset",command = self.clearApp, cursor = "hand2"
               ).grid(row = 7, column = 6, sticky = E, pady = 5)
        
    def previewImage(self):
        self.results.insert(END,"\nPreviewing image...")
        # Create secondary window for image preview
        imgPreviewWindow = Toplevel()
        imgPreviewWindow.title("Preview Image")
        imgPreviewWindow.iconbitmap('Image Converter.ico')
        imgPreviewWindow.resizable(width = False, height = False)
        imgPreviewWindow.grab_set()
        # Create canvas widget to house image in new window
        self.canvas = Canvas(imgPreviewWindow)
        self.canvas.pack()
        # Open and convert image to ensure compatible with canvas
        pilImage = PIL.Image.open(self.fileName)
        width = pilImage.width
        height = pilImage.height
        if width > 600 or height > 600:
            width = pilImage.width / 2
            height = pilImage.height / 2
        pilImage = pilImage.resize((int(width), int(height)))
        self.canvas.configure(width = int(width), height = int(height))
        self.photo = ImageTk.PhotoImage(pilImage)
        self.canvas.create_image(0, 0, anchor = NW, image = self.photo)
    
    def clearApp(self):
        """Clears all selections from the program, simulating a "reset" """
        self.results.delete(0.0,END)
        self.convertFileType.set(None)
        self.singleImageBtn.configure(state = ACTIVE, cursor = "hand2")
        self.previewImageBtn.configure(state = DISABLED, cursor = "arrow")
        self.dirBtn.configure(state = ACTIVE, cursor = "hand2")
        self.saveDirBtn1.configure(state = DISABLED, cursor = "arrow")
        self.saveDirBtn2.configure(state = DISABLED, cursor = "arrow")
        self.imageStatus.configure (text = "Not Selected", foreground = "Red", font = "Helvetica 8 bold")
        self.directoryStatus.configure (text = "Not Selected", foreground = "Red", font = "Helvetica 8 bold")
        self.saveDirStatus1.configure (text = "Not Selected", foreground = "Red", font = "Helvetica 8 bold")
        self.saveDirStatus2.configure (text = "Not Selected", foreground = "Red", font = "Helvetica 8 bold")
        self.fileName = None
        self.imageDirectory = None
        self.saveDir = None
        self.convertBtn.configure(state = DISABLED, cursor = "arrow")
        
    def clearText(self):
        """Clears all log information from Results text box"""
        self.results.delete(0.0,END)

    def validateFileTypeSelection(self):
        # Ensure a file type radio button has been selected
        fileType = self.convertFileType.get()
        if fileType != "None":
            if hasattr(app,'fileName'):
                if self.fileName != None:
                    self.convertSingleFile(fileType)
                else:
                    self.convertFileInDir(fileType)
            else:
                self.convertFileInDir(fileType)
        else:
            self.results.insert(END,"\nNo file type selected. Please select one of an option, and try again.")
    
    def getFile(self,dialogTitle, VALIDFILETYPES):
        """Opens the browse file dialog to get a single file from user. Accepts dialog title and browsable file types."""
        self.dirBtn.configure(state = DISABLED, cursor = "arrow")
        self.saveDirBtn2.configure(state = DISABLED)
        self.clearText()
        self.results.insert(END,"Opening file browser...")
        # Open file browser to locate image to convert
        try:
            defaultDirectory = os.path.expanduser('~\\Documents')
            self.fileName = filedialog.askopenfilename(initialdir = defaultDirectory,title = dialogTitle, filetypes = VALIDFILETYPES)
            if not self.fileName:
                self.results.insert(END,"\nCancelling...")
                self.dirBtn.configure(state = ACTIVE, cursor = "hand2")
            else:
                self.imageStatus.configure (text = "Image Selected", foreground = "Green", font = "Helvetica 8 bold")
                self.results.insert(END,"\nImage selected...")
                self.saveDirBtn1.configure(state = ACTIVE, cursor = "hand2")
                self.previewImageBtn.configure(state = ACTIVE, cursor = "hand2")
        except:
            self.results.insert(END,"\nSomething went wrong. Please try again")

    def getDirectory(self,dialogTitle):
        """Opens the browse directory dialog to get a directory. Accepts dialog title."""
        self.singleImageBtn.configure(state = DISABLED, cursor = "arrow")
        self.saveDirBtn1.configure(state = DISABLED)
        self.clearText()
        self.results.insert(END,"Opening directory browser...")
        # Open directory browser
        try:
            defaultDirectory = os.path.expanduser('~\\Desktop')
            self.imageDirectory = filedialog.askdirectory(initialdir = defaultDirectory,title = dialogTitle)
            if not self.imageDirectory:
                self.results.insert(END,"\nCancelling...")
                self.singleImageBtn.configure(state = ACTIVE, cursor = "hand2")
                self.saveDirBtn1.configure(state = ACTIVE, cursor = "hand2")
            else:
                self.directoryStatus.configure (text = "Directory Selected", foreground = "Green", font = "Helvetica 8 bold")
                self.results.insert(END,"\nDirectory of images selected...")
                self.saveDirBtn2.configure(state = ACTIVE, cursor = "hand2")
        except:
            self.results.insert(END,"\nSomething went wrong. Please try again")

    def getSaveDirectory(self,dialogTitle, selection):
        """Opens the browse directory dialog to get save directory. Accepts dialog title."""
        self.results.insert(END,"\nOpening directory browser...")
        # Open directory browser
        try:
            defaultDirectory = os.path.expanduser('~\\Desktop')
            self.saveDir = filedialog.askdirectory(initialdir = defaultDirectory,title = dialogTitle)
            if not self.saveDir:
                self.results.insert(END,"\nCancelling...")
            else:
                if selection == "Image":
                    self.saveDirStatus1.configure (text = "Directory Selected", foreground = "Green", font = "Helvetica 8 bold")
                else:
                    self.saveDirStatus2.configure (text = "Directory Selected", foreground = "Green", font = "Helvetica 8 bold")
                self.results.insert(END,"\nDirectory selected...\n")
                self.convertBtn.configure(state = ACTIVE, cursor = "hand2")
        except:
            self.results.insert(END,"\nSomething went wrong. Please try again")

    def convertSingleFile(self, fileType):
            # Remove file extension from image
            try:
                splitImage = os.path.split(self.fileName)
                splitImage = os.path.splitext(splitImage[1])
                # Assign full predicted image save location
                fullPath = str(self.saveDir) + "/" + splitImage[0] + fileType
                # Check if file already exists
                if os.path.exists(fullPath):
                    result = messagebox.askyesno("Image Converter","That file already exists. Overwrite?")
                    if result == True:
                        # Convert and save image into chosen directory
                        self.results.insert(END,"\nConverting file...\n")
                        self.results.insert(END,fullPath)
                        image = PIL.Image.open(self.fileName)
                        image.save(fullPath)
                        messagebox.showinfo(message = "Files Converted Successfully",title = "Image Converter",)
                    else:
                        self.results.insert(END,"\nSkipping file...")
                else:
                    # Convert and save image into chosen directory
                    self.results.insert(END,"\nConverting file...")
                    self.results.insert(END,fullPath)
                    image = PIL.Image.open(self.fileName)
                    image.save(fullPath)
                    messagebox.showinfo(message = "Files Converted Successfully",title = "Image Converter",)
            except:
                self.results.insert(END,"\nSomething went wrong. Please try again")


    def convertFileInDir(self, fileType):
        try:
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
                                self.results.insert(END,"\nConverting file...\n")
                                self.results.insert(END,fullPath)
                                image = PIL.Image.open(fullPath)
                                image.save(fullSavePath)
                            else:
                                self.results.insert(END,"\nSkipping file...")
                        else:
                            # Convert and save image into chosen directory
                            self.results.insert(END,fullSavePath + "\n")
                            image = PIL.Image.open(fullPath)
                            image.save(fullSavePath)
            messagebox.showinfo(message = "Files Converted Successfully",title = "Image Converter")
        except:
            self.results.insert(END,"\nSomething went wrong. Please try again")


##### Functions #####

def createRootWindow():
    """Creates the main root window"""
    # Create Tk root window
    root = Tk()
    # Define root window options
    root.title("Image Converter")
    root.geometry("640x530")
    # Prevent user from resizing or maximising window
    root.resizable(width=False, height=False)
    # Define window icon
    root.iconbitmap('Image Converter.ico')
    return root
                
##### Global Variables #####

#set valid file types for image browser
VALIDFILETYPES = (("JPG Files","*.jpg"),("BMP Files","*.bmp"),("PNG Files","*.png"),("ICO Files","*.ico"))


##### Main Program #####
root = createRootWindow()
app = Application(root)
root.mainloop()
