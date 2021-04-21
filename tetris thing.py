

#################################################################
# Name:Jake Stelly
# Date:02-01-2021
# Description: Calculatrise
#################################################################
from tkinter import *
import time

#main view grid to align pices
class MainGrid(Frame):
    def __init__(self,container):
        Frame.__init__(self,container, bg="black")
        #method
        self.setupGrid()

    def setupGrid(self):
        self.display = Label(self, text="", anchor = E, bg="black",height =2, width=15)
        self.display.grid(row=2,column=0, columnspan = 1, sticky = E+W+N+S)
        
        #create each grid pice in a for loop
        #commit them to the grid
        for j in range(10):
            for i in range(24):
                img = PhotoImage(file="Tetris parts/grid.gif")
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
        Name.grid(row= R,column = C)

class brick():
    def __init__(self,R,C):
        self.R = R
        self.C = C
    def Place(self,Name):
        BlockGrid.Put(self,self.R,self.C,Name)
            
        
class pieces:
    def __init__(self,R,C,Name):
        self.R = R
        self.C = C
        self.img = PhotoImage(file="Tetris parts/Square.gif")
        #Block 1
        self.B1 = brick(self.R,self.C)
        self.B1N = Label(image = self.img, bg = "black")
        #Block 2
        self.B2 = brick(self.R,self.C+1)
        self.B2N = Label(image = self.img, bg = "black")
        #Block 3
        self.B3 = brick(self.R+1,self.C)
        self.B3N = Label(image = self.img, bg = "black")
        #Block 4
        self.B4 = brick(self.R+1,self.C+1)
        self.B4N = Label(image = self.img, bg = "black")

    def Spawn(self):
        self.B1.Place(self.B1N)
        self.B2.Place(self.B2N)
        self.B3.Place(self.B3N)
        self.B4.Place(self.B4N)

    def Down(self):
        while self.C != 22:
            C = self.C + 1
            BlockGrid.Put(self,self.R,C,self.B1N)
            BlockGrid.Put(self,self.R,C+1,self.B2N)
            BlockGrid.Put(self,self.R+1,C,self.B3N)
            BlockGrid.Put(self,self.R+1,C+1,self.B4N)
            self.C =  C
        

class line(pieces):
    def __init__(self,R,C,Name):
        pieces.__init__(self,R,C,Name)
        self.img = PhotoImage(file="Tetris parts/Square.gif")
        self.B2 = brick(self.R,self.C)
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
P1 = pieces(0,0,"Square")
P1.Spawn()
##P2 = line(4,0,"Line")
##P2.Spawn()
DownButton = Button(command=lambda: P1.Down())
DownButton.grid(row=10,column=25)
        



# display the GUI and wait for user interaction
#window.mainloop()
