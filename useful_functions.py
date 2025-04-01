class useful_functions:
    def __init__(self) -> None:
        self.direction = None

    def shiftstring(self, plaintext, direction='forward', shiftby = 1):
       """ Shifts the characters in the given plaintext string by a specified number of positions
       'forward' shifts characters to the right, 'backward' shifts characters to the left"""
       self.direction = direction
       shiftedstring = ''
       for char in plaintext:
            if self.direction == "forward":
                shiftedstring += chr(ord(char)+shiftby)
            elif self.direction == "backward":
                shiftedstring += chr(ord(char)-shiftby)
       return shiftedstring
    
    def returnprimarykey(inputlist,inputsearch):
        for innerlist in inputlist:
            if inputsearch in innerlist:
                return innerlist[0]
        return None