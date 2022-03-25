from tkinter import *
from Cyphers import Enigma


class enigmaGUI:
    """Tkinter class for the GUI"""

    def __init__(self, master: object):
        """iniitializes the class with back ground and sets up all atributes"""

        self.background = "#ac7339"

        #gets the window
        self.master = master

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
        self.FramePack = [Frame(master, width = 640, height = 540,bg = self.background),
                          Frame(master, width = 640, height = 540,bg = self.background),
                          Frame(master, width = 640, height = 540,bg = self.background),
                          Frame(master, width = 640, height = 540,bg = self.background),
                          Frame(master, width = 640, height = 540,bg = self.background),
                          Frame(master, width = 640, height = 540,bg = self.background)]
        
        #places each frame in the correct position of a grid
        for i in range(2):
            
            for f in range(3):
                 
                 self.FramePack[(3*i)+f].grid(column = f, row = i)

        #dictionary of the enigma rotors and their names taken from https://en.wikipedia.org/wiki/Enigma_rotor_details
        self.rotorDictionary = {'I': "JGDQOXUSCAMIFRVTPNEWKBLZYH","II": "NTZPSFBOKMWRCJDIVLAEYUXHGQ","III": "JVIUBHTCDYAKEQZPOSGXNRMWFL",
            'UKW': 'QYHOGNECVPUZTFDJAXWMKISRBL', 'ETW': 'QWERTZUIOASDFGHJKPYXCVBNML', 'β': 'LEYJVCNIXWPBQMDRTAKZGFUHOS', 'Γ': 'FSOKANUERHMBTIYCWLQPZXVGJD'
        }
        
        #initiallizes the list for the keyboard
        self.keyboard = []
        
        #runs the keyboard initialization
        self.setKeyboard()    

        self.vList = ['I','II','III','UKW','ETW','β','Γ']    

#         self.ButtonReg = []
#         self.stringVarRegi = []
#         self.rotorReg = []
#         for i in range(3):
#             self.ButtonReg.append(Button(self.FramePack[2-i], text = self.getRotLet(i), command=lambda:self.pushOne(i), height = 3, width = 5,bg = self.background))
#             self.ButtonReg[i].grid(row = 0, column = 2 - i)
# 
#             self.stringVarRegi.append(StringVar())
#             self.stringVarRegi[i].set(self.vList[i])
# 
#             self.rotorReg.append(OptionMenu(self.FramePack[2 - i], self.stringVarRegi[i], *self.vList,command=lambda a:self.selectPair(i,a)))
#             self.rotorReg[i].grid(row = 1, column = 2 - i)

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

        
        master.mainloop()
    
    def pushEm(self):
        """Cycles the primary rotor"""
        self.machine.pushRotor()
        for i in range(3):
            self.ButtonReg[i].config(text = self.getRotLet(i))

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
        letter = self.machine.getLetter(ord(event.char.upper()) - 65)
        self.keyboard[letter].config(bg = 'yellow')
        for i in range(3):
            self.ButtonReg[i].config(text = self.getRotLet(i))

    
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
                self.keyboard.append(Label(self.FramePack[4], text = self.letters[count],bg = self.background))
                self.keyboard[count].grid(row = i, column = f+i)
                count += 1
        self.keyboard.append(Label(self.FramePack[4],text = "Z",bg = self.background))
        self.keyboard[25].grid(row = 2, column = 8)


if __name__ == "__main__":
    root = Tk()
    my_gui = enigmaGUI(root)
