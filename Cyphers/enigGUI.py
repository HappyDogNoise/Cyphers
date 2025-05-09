
from tkinter import *
from Cyphers import Enigma
import pyperclip

class Plugs:

    def __init__(self, xPos, yPos, letter):
        """creates the plug classes and assignes their limits"""

        #size of the plugs with [x, y]
        self.plugSize = [10, 5]

        #top left position of each plug
        self.Positions = [xPos, yPos]

        #bottom right pos
        self.limits = [self.Positions[0] + self.plugSize[0], self.Positions[1] + self.plugSize[1]]

        self.letter = letter



class enigmaGUI:
    """Tkinter class for the GUI"""

    def __init__(self, master: Tk):
        """initializes the class with back ground and sets up all atributes"""

        #the background colour for the whole machine
        self.background = "#ac7339"

        self.message = []
        self.rowlen = 0

        #gets the window
        self.master = master

        try:
            for widgets in self.master.winfo_children():
                widgets.destroy()

        except:
            pass

        #makes the whole page full screen
        self.master.geometry(str(master.winfo_screenwidth())+"x"+str(master.winfo_screenheight()) + "+0+0")

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

        #a list of all pairs in the plugboard
        self.listOfPairs = []
        
        self.mainPage()
        
        master.mainloop()

    def resize(self, a):
        """resizes all attributes according to the window size"""
        pass

    def clearMessage(self):
        """clears the message screen"""
        self.message = []
        self.rowlen = 0
        self.messageLabel.config(text=self.message)

    def mainPage(self):
        """creates the main paige"""

        #clears the screen
        for widgets in self.master.winfo_children():
            widgets.destroy()

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
        yRel = 0.1
        for i in range(3):
            xREL = 1 - ((i * 0.25) + 0.25)
            self.ButtonReg.append(Button(self.master, text = self.getRotLet(i), command = lambda i = i:self.pushOne(i), height = 3, width = 5,bg = self.background))
            self.ButtonReg[i].place(rely = yRel, relx = xREL, anchor = CENTER)

            self.stringVarRegi.append(StringVar())
            self.stringVarRegi[i].set(self.vList[i])

            self.rotorReg.append(OptionMenu(self.master, self.stringVarRegi[i], *self.vList,command = lambda a, i = i:self.selectPair(i,a)))
            self.rotorReg[i].place(rely = yRel + 0.05, relx = xREL, anchor = CENTER)

        #updates the interrupt register
        self.master.update_idletasks()

        #shows the typed message
        self.messageLabel = Label(self.master, bg=self.background, text="".join(self.message))
        self.messageLabel.place(rely=0.8, relx=0.7, anchor=N)
        self.clrMessage = Button(self.master,bg = self.background,text="clear message",command=self.clearMessage)
        self.clrMessage.place(rely=0.8, relx=0.25, anchor=CENTER)#initiallizes the list for the keyboard
        self.copyBtn = Button(self.master, bg=self.background,text = "COPY\nMSG", command=self.copyMessage)
        self.copyBtn.place(rely = 0.8, relx = 0.9, anchor=CENTER)

        #shows the plugboard
        self.plugboard = Button(self.master,bg=self.background,text="v\nv\nv",command=self.setupPlugBoard)
        self.plugboard.place(rely=1-yRel, relx=0.5, anchor=CENTER)

    def copyMessage(self):
        """Copy the message to clipboard"""
        pyperclip.copy("".join(self.message))

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

        canvasWidth = 1500
        canvasHeight = 500
        self.Canvas = Canvas(self.master, bd=0, highlightthickness=0, relief='ridge', bg = self.background, width = canvasWidth, height = canvasHeight)
        self.Canvas.place(relx = 0.5, rely = 0.5, anchor = CENTER)

        #creates the button to return to the main page
        self.returnButton = Button(self.master, text="^\n^\n^", command = self.mainPage, bg = self.background)
        self.returnButton.place(relx = 0.5, rely=0.05, anchor = CENTER)

        self.labelList = []
        self.dragPoint = []

        #create letters and drag spots/plugs
        count = 0
        for i in range(3):

            rowRange = 10 - i
            if i == 2:
                rowRange = 7

            for j in range(rowRange):

                self.labelList.append(Label(self.Canvas, text = self.letters[count], bg = self.background, width = int(self.Canvas.winfo_width()/3), font = ("Ariel",16)))
                self.dragPoint.append(Label(self.Canvas,text="(  • {} •  )".format(self.letters[count]), bg = "#a2683f", font = ("Ariel",16), width=7))
                xPos = (j + 0.5) * (canvasWidth / rowRange)
                yPos = (2 * i) * canvasHeight/10 + 15
                self.labelList[count].place(x = xPos, y = yPos, anchor = CENTER)
                self.dragPoint[count].place(x = xPos, y = yPos + 50, anchor = CENTER)
                self.dragPoint[count].bind("<Button-1>", lambda event, b = count: self.startDrag(event, b))
                self.dragPoint[count].bind("<B1-Motion>", lambda event, b = count: self.doDrag(event, b))
                self.dragPoint[count].bind("<ButtonRelease-1>", lambda event, b = count: self.endDrag(event, b))
                
                count += 1
        self.master.update()
        self.updatePairs()

    def startDrag(self, event, count):
        """Starts the drag event and animation with image and stuff"""
        # Update the dragPoint label
        self.dragPoint[count].config(text='PLUG')
        
        # Create drag label (PLUG) only if it doesn't exist
        if not hasattr(self, 'plugs') or self.plugs is None:
            self.plugs = Label(self.master, bg="yellow", text="PLUG")
        
        # Get local (widget) coordinates instead of screen coordinates
        x = event.x_root - self.master.winfo_rootx()
        y = event.y_root - self.master.winfo_rooty()
        
        self.plugs.place(x=x, y=y)

    def doDrag(self, event, count):
        """Handles the dragging"""
        # Convert global coordinates to widget-local
        x = event.x_root - self.master.winfo_rootx()
        y = event.y_root - self.master.winfo_rooty()
        
        if hasattr(self, 'plugs') and self.plugs is not None:
            self.plugs.place(x=x, y=y)

    def endDrag(self, event, count):
        """Ends the drag event"""

        mouse_x = event.x_root
        mouse_y = event.y_root

        target_index = None

        for i, plug in enumerate(self.dragPoint):
            # Skip if it's the one being dragged
            if i == count:
                continue

            # Get absolute screen coordinates of the plug
            plug_x1 = plug.winfo_rootx()
            plug_y1 = plug.winfo_rooty()
            plug_x2 = plug_x1 + plug.winfo_width()
            plug_y2 = plug_y1 + plug.winfo_height()

            # Check if mouse is within the plug's bounds
            if plug_x1 <= mouse_x <= plug_x2 and plug_y1 <= mouse_y <= plug_y2:
                target_index = i
                break

        if target_index is not None:
            self.NewPair([self.letters[count], self.letters[target_index]])
        else:
            self.NewPair([self.letters[count], self.letters[count]])

        # Remove the floating 'PLUG' label
        if hasattr(self, 'plugs') and self.plugs is not None:
            self.plugs.place_forget()
            self.plugs = None
            
    def NewPair(self, pairs):
        """creates a new pair of numbers in the plugboard"""

        #adds a new plug by getting what was in the menus
        pairs[0] = ord(pairs[0]) - 65
        pairs[1] = ord(pairs[1]) - 65
        self.machine.changePlug(pairs[0], pairs[1])
        self.listOfPairs=self.machine.plugBoard
        self.updatePairs()

    def updatePairs(self):
        """updates the plugboard page and adds in all the wires"""
        for i in self.listOfPairs:
            self.dragPoint[i[0]].config(text="(  • {} •  )".format(self.letters[i[1]]))
        pairs=self.machine.showPlugPairs()
 
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

        if self.rowlen >= 75:
            self.message.append("\n")
            self.rowlen = 0
        
        if event.char == " ":
            self.message.append("/")

        if ord(event.char) == 13:
            self.rowlen = -1
            self.message.append(event.char)

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
            
        self.rowlen += 1
        self.messageLabel.config(text="".join(self.message))
  
    def onRelease(self,event):
        """catches the released key to simulate a light turning on when the key is held"""
        for i in self.keyboard:
            i.config(bg = '#593715')

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

        canvasWidth = 1500
        canvasHeight = 500
        self.Canvas = Canvas(self.master, bd=0, highlightthickness=0, relief='ridge', bg = '#593715', width = canvasWidth, height = canvasHeight)
        self.Canvas.place(relx = 0.5, rely = 0.5, anchor = CENTER)

        #loops 3 lines
        count = 0
        for i in range(3):
            
            rowRange = 10 - i
            if i == 2:
                rowRange = 7

            for j in range(rowRange):
                xPos = (j + 0.5) * (canvasWidth / rowRange)
                yPos = (i + 0.5) * canvasHeight/3
                
                #creates the letters
                self.keyboard.append(Label(self.Canvas, text = self.letters[count],bg = '#593715', font = ("Ariel",16), padx=10,pady=5))
                self.keyboard[count].place(x = xPos, y = yPos, anchor=CENTER)
                count += 1

if __name__ == "__main__":
    root = Tk()
    my_gui = enigmaGUI(root)
