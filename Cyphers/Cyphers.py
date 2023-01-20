import random
from copy import deepcopy

def Morse(message = None, Forward = None):
    """function takes in either morse message or text message and translates it either way"""

    #2D array for the translation
    morseDictionary = [['A', '.-'], ['B', '-...'], ['C', '-.-.'], ['D', '-..'], ['E', '.'], ['F', '..-.'],
    ['G', '--.'], ['H', '....'], ['I', '..'], ['J', '.---'], ['K', '-.-'], ['L', '.-..'],
    ['M', '--'], ['N', '-.'], ['O', '---'], ['P', '.--.'], ['Q', '--.-'], ['R', '.-.'],
    ['S', '...'], ['T', '-'], ['U', '..-'], ['V', '...-'], ['W', '.--'], ['X', '-..-'],
    ['Y', '-.--'], ['Z', '--..']]

    #checks if there is a message input
    if message == None:

        #asks user for an input if no message given
        message = input("input message here:\n        ")

    #sets the message to all upper case
    message = message.upper()
    
    #if no value for Forward is given
    if Forward == None:
        
        #each character is checked for a /
        for i in message:
            
            if i == '/':
                
                #if a / is detected we know its morse to text
                Forward = False

        #otherwise it will be text to morse
        if Forward == None:
                
            Forward = True

    #Text to morse
    if Forward:

        #empty list for the cypher
        cypher = []

        #loop over whole message
        for i in range(len(message)):

            #append the list with the encoded char
            cypher.append(morseDictionary[ord(message[i]) - 65][1])

        #return as a string
        return('/'.join(cypher))

    #morse to english
    else:
        #the message is split with the /s removed
        message = message.split('/')

        #empty list to store th cypher
        cypher = []

        #for each element of the message
        for j in range(len(message)):

            #for each letter of the alphabet
            for i in range(26):

                #if it has found the morse part
                if morseDictionary[i][1] == message[j]:
                    
                    #append the letter to cypher
                    cypher.append(morseDictionary[i][0])

        #return the cypher joined togeather
        return(''.join(cypher))

def Caesar(message = None,Key = None):
    """translates a message using a caesar cypher
    returns the message and the key to translate it back"""
    #get whole message
    if message == None:
        message = input("input messsage:\n          ")
    message = message.upper()

    #get the translate number
    if Key == None:
        Key = input("what letter shall \"a\" be equal to:\n                     ")
        Key = ord(Key.upper()) - 65
        #print("to translate back use key = " + chr((26 - Key) + 65) + "\n\n")

    #creates an empty list to store each character
    cypher = []

    #loops over each part of the message
    for i in message:
        numbered = ord(i) + Key
        if numbered > 90:
            numbered -= 26
        cypher.append(chr(numbered))
    return ''.join(cypher),chr((26 - Key) + 65)

#function for the vernam cypher
def vernam(message = None, Key = None):

    #gets message if none passed in
    if message == None:
        message = input("input message:\n         ")

    #gets key if none passed in
    if Key == None:
        Key = []
        for i in range(random.randint(3,len(message))):
            Key.append(chr(random.randint(0,128)))
        print(Key)
    while len(Key) < len(message):
        Key += Key

    #list to hold encoded text
    encoded = []

    #loops over entire message
    for i in range(len(message)):

        #completes an XOR bitwise calculation on the letters
        encoded.append(chr(ord(message[i]) ^ ord(Key[i])))
    return("".join(encoded))

class Rotor:
    """class for a rotor on the enigma machine"""
    def __init__(self,pairs):
        """initialization method.
        Takes the pairing on the rotor as a 2D list with column 0 beign forward"""

        #checks that the pairs was input as a string
        if type(pairs) == str:

            self.pairs = self.rotorPair(pairs)

        #makes the pairs an attribute
        else:

            self.pairs = pairs

        #initializes the front pointer attribute to 0
        self.frontPointer = 0

    def cycle(self):
        """cycle method to push the rotor round one"""

        #check that the pointer is not at z
        if self.frontPointer < 25:
            #pushes the pointer forward
            self.frontPointer += 1
            return 0
        
        #otherwise it will set it back round to a
        else: 
            self.frontPointer = 0
            return 1

    def rotorPair(self, shuffled):
        """changes a string of rotor pairs (off the wiki) to the needed 2D array"""

        pairs = []

        #loops over each letter
        for i in range(26):

            #2D aray made (only numbers)
            pairs.append([i,ord(shuffled[i])-65])

        #returns the 2D array
        return pairs

    def getPoint(self):
        """gives back the pointer for the front of the rotor"""
        return self.frontPointer
    
    def getLetter(self, inputLetter, Forward):
        """gets the encoded letter.
        Takes in an inputted letter and direction of input as a parameter"""

        #if the signal is goin into the front of the rotor
        if Forward:
            
            #increase the input by the pointer
            inputLetter += self.frontPointer

            #if it is too large
            if inputLetter > 25:
                
                #it is taken back round
                inputLetter -= 26

            #returns the output
            return self.pairs[inputLetter][1]

        #if it is going to the back
        else:

            #goes through the whole array searching for the input
            for i in range(26):

                #if it has found the input
                if inputLetter == self.pairs[i][1]:

                    #it will set the output to be the letter - pointer (because it is the reverse of going forward)
                    out = self.pairs[i][0] - self.frontPointer

                    #checks it is not less than 0
                    if out < 0:
                        
                        #icreases so it is in the alphabet
                        out += 26

                    #returns the output
                    return out

    def changePairing(self,pairing):
        """changes a rotor out for a new one"""

        #resets the pointer to 1st position
        self.frontPointer = 0

        #checks if it was input as a 2D array or just a string
        if type(pairing) == str:

            #changes the string to a 2D array
            pairing = self.rotorPair(pairing)

        #sets the atribute to the new pairing
        self.pairs = pairing

class Enigma:
    """object of the whole machine. includes a refector; 3 rotors; plugboard and outputs coded/decoded letter"""

    def __init__(self, Reflector = None, a = None, b = None, c = None):
        """init method creates the needed atributes
        takes in the Reflector that is a sstring or list along with 3 rotor pairs"""

        #if the parameters supplied show None then it will be given a default one
        if a == None:
            a = self.rotorPair("JGDQOXUSCAMIFRVTPNEWKBLZYH")
        if b == None:
            b = self.rotorPair("NTZPSFBOKMWRCJDIVLAEYUXHGQ")
        if c == None:
            c = self.rotorPair("JVIUBHTCDYAKEQZPOSGXNRMWFL")

        #creates a list to store all the rotors
        self.rotors = [Rotor(a),Rotor(b),Rotor(c)] 

        if Reflector == None:
            Reflector = [[0, 21], [1, 10], [2, 22], [3, 17], [4, 6], [5, 8], [6, 4], [7, 19], [8, 5], [9, 25], [10, 1], [11, 20], [12, 18], [13, 15], [14, 16], [15, 13], [16, 14], [17, 3], [18, 12], [19, 7], [20, 11], [21, 0], [22, 2], [23, 24], [24, 23], [25, 9]]
        #attribute for the reflector, similar to the pairs in the rotors
        self.Reflector = Reflector

        #plugboard set up
        self.plugBoard = []
        self.setupPlugBoard()

    def setupPlugBoard(self):
        """function to be run initially to set the plug board to nothing"""
        for i in range(26):
            self.plugBoard.append([i,i])

    def rotorPair(self, shuffled):
        """changes a string of rotor pairs (off the wiki) to the needed 2D array"""

        pairs = []

        #loops over each letter
        for i in range(26):

            #2D aray made (only numbers)
            pairs.append([i,ord(shuffled[i])-65])

        #returns the 2D array
        return pairs

    def pushRotor(self,i):
        """increases the first rotor by one and the others if needed"""

        self.rotors[i].cycle()
        
        if self.rotors[i].frontPointer == 0 and i != 2:
            
            self.pushRotor(i+1)

    def showPlugPairs(self):
        """shows all the plug board pairs in the machine"""

        #creates a copy so that it may be referenced by value and not reference
        plugBoard = deepcopy(self.plugBoard)
        pairs = []

        for i in range(len(plugBoard)):
            
            #will only show ones that are different
            if plugBoard[i][0] != plugBoard[i][1]:
                pairs.append(plugBoard[i])
        
        return pairs

    def changePlug(self,From,To):
        """changes the plugboard's conections"""

        #checks if both values are the same
        if From == To:
            #sets both values back to the same value
            self.plugBoard[self.plugBoard[From][1]][1] = self.plugBoard[From][1]
            self.plugBoard[From][1] = To

        #checks if you're changing a value that was already changed
        if self.plugBoard[From][1] != self.plugBoard[To][0]:
            #sets the other one back to default
            self.plugBoard[self.plugBoard[From][1]][1] = self.plugBoard[From][1]
        
        #sets the new plugs
        self.plugBoard[From][1] = To
        self.plugBoard[To][1] = From

        
    def pushSpecific(self, sRotor):
        """increases selected rotor by one"""

        self.rotors[sRotor].cycle()

    def showRotors(self):
        """returns a list of the 3 rotors and where they point"""

        return[self.rotors[0].getPoint(),self.rotors[1].getPoint(),self.rotors[2].getPoint()]

    def reflector(self, inputLetter):
        """reflects the inputted letter back into the rotor"""

        return self.Reflector[inputLetter][1]

    def showLetter(self, rot):
        """shows one rotors position"""
        return self.rotors[rot].getPoint()

    def getLetter(self, inputLetter):
        """gets the encoded letter
        takes in the original input letter as an integer"""

        inputLetter = self.plugBoard[inputLetter][1]

        #loops over each rotor
        for i in self.rotors:
            
            #changes input letter to what the rotor says
            inputLetter = i.getLetter(inputLetter,True)

        #reflects in
        inputLetter = self.reflector(inputLetter)

        #goes through each rotor in reverse order
        for i in self.rotors[::-1]:

            inputLetter = i.getLetter(inputLetter,False)
        
        self.pushRotor(0)

        inputLetter = self.plugBoard[inputLetter][1]

        #returns as a letter
        return(inputLetter)

    def changePair(self,i,pair):
        """changes the pair of one of the 3 rotors"""
        self.rotors[i].changePairing(pair)

def hash():
    """hash function thing testing"""

