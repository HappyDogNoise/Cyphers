
from tkinter import *
from Cyphers import Enigma

class enigmaGUI:
    """Tkinter class for the GUI"""

    def __init__(self, master: Tk):
        """initializes the class with back ground and sets up all atributes"""

        #the background colour for the whole machine
        self.background = "#ac7339"

        #a list of all pairs in the plugboard
        self.listOfPairs = []

        #gets the window
        self.master = master

        #makes the whole page full screen
        self.master.geometry(str(master.winfo_screenwidth())+"x"+str(master.winfo_screenheight()))

        self.master.update_idletasks()

        #gets the light images
        """ self.lightOff = PhotoImage(file=('./Assets/Images/bulb.png'))
        self.lightOn = PhotoImage(file='./Assets/Images/bulbL.png') """

        #gives the window a title and sets the background colour
        master.title("Enigma")
        master.config(bg = self.background)
        
        #binds the keypress interrupts to a method
        master.bind('<KeyPress>', self.onKeyPress)
        master.bind('<KeyRelease>', self.onRelease)
        #master.bind('<Configure>', self.resize)

        #creates an attribute for the alphabet
        self.letters = ['A','B','C','D','E','F','G','H','I','J','K','L','M',
        'N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
        
        #creates an encapsulated enigma class
        self.machine = Enigma()

        #list of the wires
        self.lineList = []

        #dictionary of the enigma rotors and their names taken from https://en.wikipedia.org/wiki/Enigma_rotor_details
        self.rotorDictionary = {'I': "JGDQOXUSCAMIFRVTPNEWKBLZYH","II": "NTZPSFBOKMWRCJDIVLAEYUXHGQ","III": "JVIUBHTCDYAKEQZPOSGXNRMWFL","IV": "ESOVPZJAYQUIRHXLNFTGKDCMWB","V": "VZBRGITYUPSDNHLXAWMJQOFECK","VI": "JPGVOUMFYQBENHZRDKASXLICTW",
            'UKW': 'QYHOGNECVPUZTFDJAXWMKISRBL', 'ETW': 'QWERTZUIOASDFGHJKPYXCVBNML', 'β': 'LEYJVCNIXWPBQMDRTAKZGFUHOS', 'Γ': 'FSOKANUERHMBTIYCWLQPZXVGJD'
        }
        
        self.mainPaige()
        
        master.mainloop()

    def resize(self, a):
        """resizes all attributes according to the window size"""
        print("test", a)
        #self.changeFrameSizes()

    def changeFrameSizes(self):
        """changes the size of the frames"""
        self.master.update_idletasks()
        for i in self.FramePack:
            i.config(width=self.master.winfo_width()/3, height=self.master.winfo_height()/2)

    def clearMessage(self):
        """clears the message screen"""
        self.message = []
        self.messageLabel.config(text=self.message)

    def mainPaige(self):
        """creates the main paige"""

        #clears the screen
        for widgets in self.master.winfo_children():
            widgets.destroy()

        #creates a list of all the frames
        self.FramePack = [Frame(self.master, bg = self.background),
                          Frame(self.master, bg = self.background),
                          Frame(self.master, bg = self.background),
                          Frame(self.master, bg = self.background),
                          Frame(self.master, bg = self.background),
                          Frame(self.master, bg = self.background),
                          Frame(self.master, bg = self.background),
                          Frame(self.master, bg = self.background),
                          Frame(self.master, bg = self.background),
                          ]
        self.changeFrameSizes()

        #places each frame in the correct position of a grid
        for i in range(3):
            
            for f in range(3):
                 
                 self.FramePack[(3*i)+f].grid(column = f, row = i)

        #initiallizes the list for the keyboard
        self.keyboard = []
        
        #runs the keyboard initialization
        self.setKeyboard()    

        #sets the list for the rotor types
        self.vList = ['I','II','III','UKW','ETW','β','Γ']    

        #create the rotor buttons including the drop menu that changes the rotor
        self.ButtonReg = []
        self.stringVarRegi = []
        self.rotorReg = []
        for i in range(3):
            self.ButtonReg.append(Button(self.FramePack[2-i], text = self.getRotLet(i), command = lambda i = i:self.pushOne(i), height = 3, width = 5,bg = self.background))
            self.ButtonReg[i].grid(row = 0, column = 2 - i)

            self.stringVarRegi.append(StringVar())
            self.stringVarRegi[i].set(self.vList[i])

            self.rotorReg.append(OptionMenu(self.FramePack[2 - i], self.stringVarRegi[i], *self.vList,command = lambda a, i = i:self.selectPair(i,a)))
            self.rotorReg[i].grid(row = 1, column = 2 - i)

        #updates the interrupt register
        self.master.update_idletasks()

        #sets the sizes of the rows and columns
        self.master.grid_rowconfigure(0, minsize=250, weight=1)
        self.master.grid_rowconfigure(1, minsize=250, weight=1)
        self.master.grid_rowconfigure(2, minsize=250, weight=1)
        self.master.grid_columnconfigure(0, minsize=450, weight=1)
        self.master.grid_columnconfigure(1, minsize=450, weight=1)
        self.master.grid_columnconfigure(2, minsize=450, weight=1)

        #shows the typed message
        self.messageLabel = Label(self.FramePack[8], bg=self.background)
        self.messageLabel.grid(row=0,column=0)
        self.message = []
        self.clrMessage = Button(self.FramePack[6],bg = self.background,text="clear message",command=self.clearMessage)
        self.clrMessage.grid(row=0,column=0)#initiallizes the list for the keyboard

        #shows the plugboard
        self.plugboard = Button(self.FramePack[7],bg=self.background,text="v\nv\nv",command=self.setupPlugBoard)
        self.plugboard.grid(row=0,column=0)

    def pushEm(self):
        """Cycles the primary rotor"""
        self.machine.pushRotor()
        for i in range(3):
            self.ButtonReg[i].config(text = self.getRotLet(i))
        
    def setupPlugBoard(self):
        """creates the plugboard like the keyboard on the start up"""

        #clears the screen
        for widgets in self.master.winfo_children():
            widgets.destroy()

        #makes new frames
        self.Canvas = Canvas(self.master, bd=0, highlightthickness=0, relief='ridge', bg = self.background, width = 500, height = 200)
        self.Canvas.place(relx = 0.5, rely = 0.66, anchor = CENTER)

        #creates the button to return to the main page
        self.returnButton = Button(self.master, text="^\n^\n^", command = self.mainPaige, bg = self.background)
        self.returnButton.place(relx = 0.5, rely=0.05, anchor = CENTER)

        self.labelList = []
        self.dragPoint = []
        #create letters and drag spots/plugs
        count = 0
        for i in range(3):

            for j in range(10 - (i ** 2)):

                self.labelList.append(Label(self.Canvas, text = self.letters[count], bg = self.background, width = int(self.Canvas.winfo_width()/3), font = ("Ariel",16), padx=30,pady=5))
                self.dragPoint.append(Label(self.Canvas,text="(•   •)", bg = "#a2683f", font = ("Ariel",16), padx=30,pady=5))
                self.labelList[count].grid(row = 2 * i, column = j + i)
                self.dragPoint[count].grid(row = 2 * i + 1, column = j + i)
                #self.labelList[count].place(rely = 2 * i * 0.1, relx = (j + i) * 0.1)
                #self.dragPoint[count].place(rely = (2 * i + 1)*0.1, relx = (j + i) * 0.1)
                self.dragPoint[count].bind("<Button-1>", lambda event, b = count: self.startDrag(event, b))
                self.dragPoint[count].bind("<B1-Motion>", lambda event, b = count: self.doDrag(event, b))
                self.dragPoint[count].bind("<ButtonRelease-1>", lambda event, b = count: self.endDrag(event, b))
                count += 1

        #adds the z
        self.labelList.append(Label(self.Canvas, text = self.letters[count], bg = self.background, width = int(self.Canvas.winfo_width()/3), font = ("Ariel",16), padx=30,pady=5))
        self.dragPoint.append(Label(self.Canvas,text="(•   •)",bg = "#a2683f", font = ("Ariel",16), padx=30,pady=5))
        self.labelList[25].grid(row = 4, column = 8)
        self.dragPoint[25].grid(row = 5, column = 8)
        self.dragPoint[25].bind("<Button-1>", lambda event, b = 25: self.startDrag(event, b))
        self.dragPoint[25].bind("<B1-Motion>", lambda event, b = 25: self.doDrag(event, b))
        self.dragPoint[25].bind("<ButtonRelease-1>", lambda event, b = 25: self.endDrag(event, b))

        self.updatePairs()

    def createLine(self, x1, y1, x2, y2):
        """create the lines for the wires"""
        self.lineList.append(self.Canvas.create_line(x1,y1,x2,y2, width=5))

    def startDrag(self, event, count):
        """starts the drag event and animation with image and stuff"""
        #creates the initial drag image
        self.plugs = (Label(self.master, bg = "yellow", text = "PLUG"))
        self.plugs.place(x = event.x_root, y = event.y_root - 54)
        print(self.dragPoint[count].winfo_rootx() + (self.dragPoint[count].winfo_width() / 2), self.dragPoint[count].winfo_rooty() + (self.dragPoint[count].winfo_height() / 2), self.plugs.winfo_rootx() + (self.plugs.winfo_width() / 2), self.plugs.winfo_rooty() + (self.plugs.winfo_height() / 2))
        self.createLine(self.dragPoint[count].winfo_rootx() + (self.dragPoint[count].winfo_width() / 2), self.dragPoint[count].winfo_rooty() + (self.dragPoint[count].winfo_height() / 2), self.plugs.winfo_rootx() + (self.plugs.winfo_width() / 2), self.plugs.winfo_rooty() + (self.plugs.winfo_height() / 2))

    def doDrag(self, event, count):
        """what is being done in the drag event"""
        #draws the plug where the mouse is
        self.plugs.place(x = event.x_root, y = event.y_root - 54)
        print(self.dragPoint[count].winfo_rootx() + (self.dragPoint[count].winfo_width() / 2), self.dragPoint[count].winfo_rooty() + (self.dragPoint[count].winfo_height() / 2), self.plugs.winfo_rootx() + (self.plugs.winfo_width() / 2), self.plugs.winfo_rooty() + (self.plugs.winfo_height() / 2))
        self.Canvas.coords(self.lineList[-1], self.dragPoint[count].winfo_rootx() + (self.dragPoint[count].winfo_width() / 2), self.dragPoint[count].winfo_rooty() + (self.dragPoint[count].winfo_height() / 2), self.plugs.winfo_rootx() + (self.plugs.winfo_width() / 2), self.plugs.winfo_rooty() + (self.plugs.winfo_height() / 2))

    def endDrag(self, event, count):
        """ends the drag"""
        #checks plug location if that is where it was dropped
        plugPair = [count]
        for i in range(26):
            if self.plugs.winfo_rootx() >= self.dragPoint[i].winfo_rootx() and self.plugs.winfo_rootx() < self.dragPoint[i].winfo_rootx() + self.dragPoint[i].winfo_width():
                if self.plugs.winfo_rooty() >= self.dragPoint[i].winfo_rooty() and self.plugs.winfo_rooty() < self.dragPoint[i].winfo_rooty() + self.dragPoint[i].winfo_height():
                    plugPair.append(i)

        #destroys the plug
        self.plugs.place_forget()

        
        #creates the new pair
        if len(plugPair) == 2:
            self.NewPair(plugPair)

    def NewPair(self, pairs):
        """creates a new pair of numbers in the plugboard"""

        #adds a new plug by getting what was in the menus
        self.machine.changePlug(pairs[0], pairs[1])
        self.listOfPairs=self.machine.showPlugPairs()
        self.updatePairs()

    def updatePairs(self):
        """updates the plugboard page and adds in all the wires"""
        for i in self.listOfPairs:
            self.createLine(self.dragPoint[i[0]].winfo_rootx(), self.dragPoint[i[0]].winfo_rooty(), self.dragPoint[i[1]].winfo_rootx(), self.dragPoint[i[1]].winfo_rooty())
 
    def changeRotor(self,i,pair):
        """changes the given rotor to the given pair"""
        self.machine.changePair(i,pair)

    def selectPair(self,i,selected):
        """lets the user select a new pair for the rotor""" 
        self.changeRotor(i, self.rotorDictionary[selected])
        for i in range(3):
            self.ButtonReg[i].config(text = self.getRotLet(i))
           
    def onKeyPress(self,event):
        """when a key is pressed the encryption is started"""
        #checks if space is pressed
        if event.char == " ":
            self.message.append("/")

        #checks if any key that isnt a letter is typed
        elif ord(event.char.upper()) - 65 < 0 or ord(event.char.upper()) - 65 > 25:
            self.message.append(event.char)

        #gets the letter and shows it on the message
        else:
            letter = self.machine.getLetter(ord(event.char.upper()) - 65)
            self.keyboard[letter].config(bg = 'yellow')
            for i in range(3):
                self.ButtonReg[i].config(text = self.getRotLet(i))
            self.message.append(chr(letter + 65))
        self.messageLabel.config(text=self.message)
  
    def onRelease(self,event):
        """catches the released key to simulate a light turning on when the key is held"""
        for i in self.keyboard:
            i.config(bg = self.background)

    def pushOne(self,i):
        """pushes the rotor and shows it on the screen"""
        self.machine.pushSpecific(i)
        for i in range(3):
            self.ButtonReg[i].config(text = self.getRotLet(i))
 
    def getRotLet(self,i):
        """gets the letter from a rotor"""
        return chr(self.machine.showLetter(i) + 65)
          
    def setKeyboard(self):
        """sets up the Lightboard"""

        #loops 3 lines
        count = 0
        for i in range(3):
            
            #creates each letter
            for f in range(10 - (i ** 2)):
                
                #creates the letters
                self.keyboard.append(Label(self.FramePack[4], text = self.letters[count],bg = self.background, font = ("Ariel",16), padx=10,pady=5))
                self.keyboard[count].grid(row = i, column = f+i)
                count += 1
        self.keyboard.append(Label(self.FramePack[4],text = "Z",bg = self.background, font = ("Ariel",16), padx=10,pady=5))
        self.keyboard[25].grid(row = 2, column = 8)

if __name__ == "__main__":
    root = Tk()
    my_gui = enigmaGUI(root)
