
from tkinter import *
from Cyphers import Enigma
import os


class enigmaGUI:
    """Tkinter class for the GUI"""

    def __init__(self, master: Enigma):
        """iniitializes the class with back ground and sets up all atributes"""

        self.background = "#ac7339"

        self.listOfPairs = []

        #gets the window
        self.master = master

        #gets the light images
        """ self.lightOff = PhotoImage(file=('./Assets/Images/bulb.png'))
        self.lightOn = PhotoImage(file='./Assets/Images/bulbL.png') """

        #gives the window a title
        master.title("Enigma")
        #master.geometry("1920x1080")
        master.config(bg = self.background)
        
        #binds the keypress interrupt to a method
        master.bind('<KeyPress>', self.onKeyPress)
        master.bind('<KeyRelease>', self.onRelease)
        
        #creates an attribute for the alphabet
        self.letters = ['A','B','C','D','E','F','G','H','I','J','K','L','M',
        'N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
        
        #creates an encapsulated enigma class
        self.machine = Enigma()
        
        
        #creates a list of all the frames
        self.FramePack = [Frame(master, bg = self.background),
                          Frame(master, bg = self.background),
                          Frame(master, bg = self.background),
                          Frame(master, bg = self.background),
                          Frame(master, bg = self.background),
                          Frame(master, bg = self.background),
                          Frame(master, bg = self.background),
                          Frame(master, bg = self.background),
                          Frame(master, bg = self.background),
                          ]
        
        #places each frame in the correct position of a grid
        for i in range(3):
            
            for f in range(3):
                 
                 self.FramePack[(3*i)+f].grid(column = f, row = i)

        #dictionary of the enigma rotors and their names taken from https://en.wikipedia.org/wiki/Enigma_rotor_details
        self.rotorDictionary = {'I': "JGDQOXUSCAMIFRVTPNEWKBLZYH","II": "NTZPSFBOKMWRCJDIVLAEYUXHGQ","III": "JVIUBHTCDYAKEQZPOSGXNRMWFL","IV": "ESOVPZJAYQUIRHXLNFTGKDCMWB","V": "VZBRGITYUPSDNHLXAWMJQOFECK","VI": "JPGVOUMFYQBENHZRDKASXLICTW",
            'UKW': 'QYHOGNECVPUZTFDJAXWMKISRBL', 'ETW': 'QWERTZUIOASDFGHJKPYXCVBNML', 'β': 'LEYJVCNIXWPBQMDRTAKZGFUHOS', 'Γ': 'FSOKANUERHMBTIYCWLQPZXVGJD'
        }
        
        self.mainPaige()
        
        master.mainloop()

    def clearMessage(self):
        """clears the message screen"""
        self.message = []
        self.messageLabel.config(text=self.message)

    def mainPaige(self):
        """creates the main paige"""

        #clears the screen
        for i in self.FramePack:
            for widget in i.winfo_children():
                widget.destroy()

        #initiallizes the list for the keyboard
        self.keyboard = []
        
        #runs the keyboard initialization
        self.setKeyboard()    

        self.vList = ['I','II','III','UKW','ETW','β','Γ']    

        # self.ButtonReg = []
        # self.stringVarRegi = []
        # self.rotorReg = []
        # for i in range(3):
        #     self.ButtonReg.append(Button(self.FramePack[2-i], text = self.getRotLet(i), command=lambda:self.pushOne(i), height = 3, width = 5,bg = self.background))
        #     self.ButtonReg[i].grid(row = 0, column = 2 - i)

        #     self.stringVarRegi.append(StringVar())
        #     self.stringVarRegi[i].set(self.vList[i])

        #     self.rotorReg.append(OptionMenu(self.FramePack[2 - i], self.stringVarRegi[i], *self.vList,command=lambda a:self.selectPair(i,a)))
        #     self.rotorReg[i].grid(row = 1, column = 2 - i)

        #sets the buttons for the rotation
        self.ButtonReg = [Button(self.FramePack[2], text = self.getRotLet(0), command=lambda:self.pushOne(0), height = 3, width = 5,bg = self.background),
                          Button(self.FramePack[1], text = self.getRotLet(1), command=lambda:self.pushOne(1), height = 3, width = 5,bg = self.background),
                          Button(self.FramePack[0], text = self.getRotLet(2), command=lambda:self.pushOne(2), height = 3, width = 5,bg = self.background)]
        self.ButtonReg[0].grid(row=0,column=2)
        self.ButtonReg[1].grid(row=0,column=1)
        self.ButtonReg[2].grid(row=0,column=0)

        self.stringVarRegi = [StringVar(),StringVar(),StringVar()]
        self.stringVarRegi[0].set(self.vList[0])
        self.stringVarRegi[1].set(self.vList[1])
        self.stringVarRegi[2].set(self.vList[2])
        #creates list for the changing of the rotors
        self.rotorReg = [OptionMenu(self.FramePack[2], self.stringVarRegi[0], *self.vList,command=lambda a:self.selectPair(0,a)),
                        OptionMenu(self.FramePack[1], self.stringVarRegi[1], *self.vList,command=lambda a:self.selectPair(1,a)),
                        OptionMenu(self.FramePack[0], self.stringVarRegi[2], *self.vList,command=lambda a:self.selectPair(2,a))]
        self.rotorReg[0].grid(row=1,column=2)
        self.rotorReg[1].grid(row=1,column=1)
        self.rotorReg[2].grid(row=1,column=0)

        #sets the sizes of the rows and columns
        self.master.grid_rowconfigure(0, minsize=250, weight=1)
        self.master.grid_rowconfigure(1, minsize=250, weight=1)
        self.master.grid_rowconfigure(2, minsize=250, weight=1)
        self.master.grid_columnconfigure(0, minsize=450, weight=1)
        self.master.grid_columnconfigure(1, minsize=450, weight=1)
        self.master.grid_columnconfigure(2, minsize=450, weight=1)

        #shows the typed message
        self.messageLabel = Label(self.FramePack[7], bg=self.background)
        self.messageLabel.grid(row=0,column=0)
        self.message = []
        self.clrMessage = Button(self.FramePack[6],bg = self.background,text="clear message",command=self.clearMessage)
        self.clrMessage.grid(row=0,column=0)#initiallizes the list for the keyboard
        self.keyboard = []
        
        #runs the keyboard initialization
        self.setKeyboard()    

        self.vList = ['I','II','III','IV','V','VI','UKW','ETW','β','Γ']    

        # self.ButtonReg = []
        # self.stringVarRegi = []
        # self.rotorReg = []
        # for i in range(3):
        #     self.ButtonReg.append(Button(self.FramePack[2-i], text = self.getRotLet(i), command=lambda:self.pushOne(i), height = 3, width = 5,bg = self.background))
        #     self.ButtonReg[i].grid(row = 0, column = 2 - i)

        #     self.stringVarRegi.append(StringVar())
        #     self.stringVarRegi[i].set(self.vList[i])

        #     self.rotorReg.append(OptionMenu(self.FramePack[2 - i], self.stringVarRegi[i], *self.vList,command=lambda a:self.selectPair(i,a)))
        #     self.rotorReg[i].grid(row = 1, column = 2 - i)

        #sets the buttons for the rotation
        self.ButtonReg = [Button(self.FramePack[2], text = self.getRotLet(0), command=lambda:self.pushOne(0), height = 3, width = 5,bg = self.background),
                          Button(self.FramePack[1], text = self.getRotLet(1), command=lambda:self.pushOne(1), height = 3, width = 5,bg = self.background),
                          Button(self.FramePack[0], text = self.getRotLet(2), command=lambda:self.pushOne(2), height = 3, width = 5,bg = self.background)]
        self.ButtonReg[0].grid(row=0,column=2)
        self.ButtonReg[1].grid(row=0,column=1)
        self.ButtonReg[2].grid(row=0,column=0)

        self.stringVarRegi = [StringVar(),StringVar(),StringVar()]
        self.stringVarRegi[0].set(self.vList[0])
        self.stringVarRegi[1].set(self.vList[1])
        self.stringVarRegi[2].set(self.vList[2])
        #creates list for the changing of the rotors
        self.rotorReg = [OptionMenu(self.FramePack[2], self.stringVarRegi[0], *self.vList,command=lambda a:self.selectPair(0,a)),
                        OptionMenu(self.FramePack[1], self.stringVarRegi[1], *self.vList,command=lambda a:self.selectPair(1,a)),
                        OptionMenu(self.FramePack[0], self.stringVarRegi[2], *self.vList,command=lambda a:self.selectPair(2,a))]
        self.rotorReg[0].grid(row=1,column=2)
        self.rotorReg[1].grid(row=1,column=1)
        self.rotorReg[2].grid(row=1,column=0)

        #sets the sizes of the rows and columns
        self.master.grid_rowconfigure(0, minsize=250, weight=1)
        self.master.grid_rowconfigure(1, minsize=250, weight=1)
        self.master.grid_rowconfigure(2, minsize=250, weight=1)
        self.master.grid_columnconfigure(0, minsize=450, weight=1)
        self.master.grid_columnconfigure(1, minsize=450, weight=1)
        self.master.grid_columnconfigure(2, minsize=450, weight=1)

        #shows the typed message
        self.messageLabel = Label(self.FramePack[7], bg=self.background)
        self.messageLabel.grid(row=0,column=0)
        self.message = []
        self.clrMessage = Button(self.FramePack[6],bg = self.background,text="clear message",command=self.clearMessage)
        self.clrMessage.grid(row=0,column=0)

        #shows the plugboard
        self.plugboard = Button(self.FramePack[8],bg=self.background,text="plugboard",command=self.setupPlugBoard)
        self.plugboard.grid(row=0,column=0)

    def pushEm(self):
        """Cycles the primary rotor"""
        self.machine.pushRotor()
        for i in range(3):
            self.ButtonReg[i].config(text = self.getRotLet(i))
        
    def setupPlugBoard(self):
        """creates the plugboard like the keyboard on the start up"""
        for i in self.FramePack:
            for widget in i.winfo_children():
                widget.destroy()

        #button to return to the main paige of the enigma
        button = Button(self.FramePack[0], text = "return",command=self.mainPaige)
        button.grid(row=0,column=0)

        #button to create new pair
        newPair = Button(self.FramePack[0], text = "new ", command = self.NewPair)
        newPair.grid(row=1,column=0)

        #shows all the pairs
        self.pairsList = Label(self.FramePack[1], text = self.listOfPairs)
        self.pairsList.grid(row=0,column=0)

        #creates the 2 option menus that create the new pairs
        self.alphabet1 = StringVar(self.master)
        self.alphabet1.set("new pair 1")
        self.alphabet2 = StringVar(self.master)
        self.alphabet2.set("new pair 2")
        pair1 = OptionMenu(self.FramePack[3],self.alphabet1,*self.letters)
        pair2 = OptionMenu(self.FramePack[5],self.alphabet2,*self.letters)
        pair1.grid(row=0,column=0)
        pair2.grid(row=0,column=0)

    def NewPair(self):
        """creates a new pair of numbers in the plugboard"""

        #stops users accidentally creating a pair with the initial conditions of the menus
        if self.alphabet1.get() != "new pair 1" and self.alphabet2 != "new pair 2":

            #adds a new plug by hetting what was in the menus
            self.machine.changePlug(ord(self.alphabet1.get()) - 65,ord(self.alphabet2.get()) - 65)
            self.listOfPairs=self.machine.showPlugPairs()

            #changes the pairs into letters
            for i in range(len(self.listOfPairs)):
                self.listOfPairs[i][0] = chr(int(self.listOfPairs[i][0] + 65))
                self.listOfPairs[i][1] = chr(int(self.listOfPairs[i][1] + 65))

            #shows on the window
            self.pairsList.config(text = self.listOfPairs)
   
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
            self.messageLabel.config(text = self.message)

        #checks if any key that isnt a letter is typed
        elif ord(event.char.upper()) - 65 < 0 or ord(event.char.upper()) - 65 > 25:
            self.message.append(event.char)
            self.messageLabel.config(text=self.message)

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
