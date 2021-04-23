#################################################################
# Name:Connor Gwatney
# Date:04-19-2021
# Description: Tetris
#################################################################
from tkinter import *

#main view grid to align pices
class MainGrid(Frame):
    def __init__(self,container):
        Frame.__init__(self,container, bg="black")
        #method
        self.setupGrid()

    def setupGrid(self):
        self.display = Label(self, text="", anchor = E, bg="black",height =2, width=15)
        self.display.grid(row=2,column=0, columnspan = 1, sticky = E+W+N+S)
        self.display.pack()
        
        #create each grid pice in a for loop
        #commit them to the grid
        for j in range(24):
            for i in range(10):
                img = PhotoImage(file="Tetris parts/grid1.gif")
                L = Label(image = img,bg="black")
                L.image = img
                L.grid(row=j,column = i)
        
#Grid used to house the pieces
class BlockGrid(Frame):
    def __init__(self,container):
        Frame.__init__(self,container, bg="black")
        #method
        self.setupGrid()

    def setupGrid(self):
        self.display = Label(self, text="", anchor = E, bg="black",height =2, width=15)
        self.display.grid(row=2,column=0, columnspan = 1, sticky = E+W+N+S)

    def Put(self,R,C,Name):
        img = PhotoImage(file="Tetris parts/Square1.gif")
        L = Label(image = img,bg="black")
        L.image = img
        L.grid(row= R,column = C)

class brick():
    def __init__(self,R,C):
        self.R = R
        self.C = C
    def Place(self):
        BlockGrid.Put(self,self.R,self.C,line)
            
        
class pieces:
    def __init__(self,R,C):
        self.R = R
        self.C = C
        self.B1 = brick(self.R,self.C)
        self.B2 = brick(self.R,self.C+1)
        self.B3 = brick(self.R+1,self.C)
        self.B4 = brick(self.R+1,self.C+1)

    def Spawn(self):
        self.B1.Place()
        self.B2.Place()
        self.B3.Place()
        self.B4.Place()

        

class line(pieces):
    def __init__(self,R,C):
        pieces.__init__(self,R,C)
        self.B1 = brick(self.R,self.C)
        self.B2 = brick(self.R,self.C+1)
        self.B3 = brick(self.R,self.C+2)
        self.B4 = brick(self.R,self.C+3)
          
##############################
# the main part of the program
##############################
# create the window
window = Tk()
window.title("Tetris")
# set the window title

# generate the GUI
g1 = MainGrid(window)
g2 = BlockGrid(window)
P1 = pieces(0,0)
P1.Spawn()
P2 = line(4,0)
P2.Spawn()

        



# display the GUI and wait for user interaction
#window.mainloop()
