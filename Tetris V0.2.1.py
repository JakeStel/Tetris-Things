from tkinter import *
import random
from matrix_rotation import rotate_array as ra


DEBUG = False

#===Main Class===#

class Tetris:
    def __init__(self, master):
        master.title("Tetris")
        self.master = master
        self.grid_width = 10
        self.grid_height = 24
        self.grid = [['' for col in range(self.grid_width)] for row in range(self.grid_height)]
        self.w = 300
        self.h = 720
        self.square_w = self.w//10
        self.canvas = Canvas(game, height = self.h, width = self.w) #bg = 'gray')
        self.canvas.grid(row=0, column = 0)
        self.startLine = self.canvas.create_line(0, self.h/6, self.w, self.h/6, width = 4)
        self.tickrate = 1000
        self.spawning = False
        self.master.after(self.tickrate, self.fps)

        #=Creating the Shapes=#
        self.shapes = {'s':[['','*'],
                            ['*','*'],
                            ['*','']],
                       
                       'z':[['*',''],
                            ['*','*'],
                            ['','*']],
                       
                       'r':[['*','*'],
                            ['*',''],
                            ['*','']],
                       
                       'L':[['*',''],
                            ['*',''],
                            ['*','*']],
                       
                       'o':[['*','*'],
                            ['*','*']],
                       
                       'I':[['*'],
                            ['*'],
                            ['*'],
                            ['*']],
                       
                       'T':[['*','*','*'],
                            ['','*','']]
                       }
                       


        #=KeyBinds=#
        self.master.bind('<Down>', self.move)
        self.master.bind('<Up>', self.rotation)
        self.master.bind('<Left>', self.move)
        self.master.bind('<Right>', self.move)
        

                       

        
#====================FPS Function===================#
    def fps(self):
        if DEBUG:
            print("fps is ticking")
        if not self.spawning:
            self.add_piece()
            self.spawning = not self.spawning
        
        self.move()

        self.master.after(self.tickrate, self.fps)
        


#====================Movement Function====================#
    def move(self, event=None):
        
        if not self.spawning:
            return
        
        
        r = self.active_piece['row']
        c = self.active_piece['col']
        l = len(self.active_piece['shape'])
        w = len(self.active_piece['shape'][0])


        direction = (event and event.keysym) or 'Down'
        if DEBUG:
            print('Keysym:',direction)
        
        
        if direction == 'Down':
            if r+l >= self.grid_height:
                print(r)
                self.bottom()
                return
            rt = r+1
            ct = c
            
        elif direction == 'Left':
            if not c:
                return
            rt = r
            ct = c-1

        elif direction == 'Right':
            if c+w >= self.grid_width:
                return
            rt = r
            ct = c+1

        for row, blocks in zip(range(rt, rt+l),
                               self.active_piece['shape']
                               ):
                
                for column, block in zip(range(ct,ct+w), blocks):
                    if block and self.grid[row][column] == 'x':
                        if direction == 'Down':
                            self.bottom()

                        return

                    

        for row in self.grid:
            row[:] = ['' if cell == '*' else cell for cell in row]
            

        #=Moves Piece Down=#
        if direction == 'Down':
            #self.grid[r][c:c+w] = ['' if p else b for b,p in zip(self.grid[r][c:c+w],self.active_piece['shape'][0])]
            self.active_piece['row'] += 1
            r += 1


            
        #=Moves Piece Left and Right=#    
        else:
            if direction == 'Left':
                #column = c+w
                self.active_piece['col'] -= 1 
                c -= 1
            elif direction == 'Right':
                #column = c-1
                self.active_piece['col'] += 1
                c += 1

           
        for row, blocks in zip(range(r, r+l),
                               self.active_piece['shape']):
            
            for column, block in zip(range(c,c+w),blocks):
                if block:
                    self.grid[row][column] = block

        for id,coords_idx in zip(self.active_piece['piece'], range(len(self.active_piece['coords']))):

            #=Moves Block on Canvas=#
            x1,y1,x2,y2 = self.active_piece['coords'][coords_idx]
            if direction == 'Down':
                y1 += self.square_w
                y2 += self.square_w
            elif direction == 'Left':
                x1 -= self.square_w
                x2 -= self.square_w
            elif direction == 'Right':
                x1 += self.square_w
                x2 += self.square_w
                
            self.active_piece['coords'][coords_idx] = x1,y1,x2,y2
            self.canvas.coords(id, self.active_piece['coords'][coords_idx])



#====================Rotation Function====================#
    def rotation(self, direct):
        pass



    def bottom(self):
        pass #Checks for loss by height
        self.spawning = not self.spawning
        if DEBUG:
            print("Piece has reached the bottom")
            for row in self.grid:
                print(row)

        for row in self.grid:
            row[:] = ['x' if cell == '*' else cell for cell in row]
        

    def add_piece(self):
        if DEBUG:
            print("Creating random piece")
            
        shape = self.shapes[random.choice('szrLoIT')]
        shape = ra(shape, random.choice((0,90,180,270)))
        w = len(shape[0])
        startUp = (10-w)//2
        self.active_piece = {'shape':shape,'piece':[],'row':0, 'col':startUp, 'coords':[]}
        for y,row in enumerate(shape):
            self.grid[y][startUp:startUp+w] = shape[y]
            for x,grid_cell in  enumerate(row, start=startUp):

                #=Takes Coords of each block and appends to list=#
                if grid_cell:
                    self.active_piece['coords'].append((self.square_w*x,
                                                        self.square_w*y,
                                                        self.square_w*(x+1),
                                                        self.square_w*(y+1)))
                    
                    
                    self.active_piece['piece'].append(
                        self.canvas.create_rectangle(self.active_piece['coords'][-1]))

                    
                
        

    def new(self):
        pass

    def loss(self):
        pass

    def remove(self):
        pass


    
    
        
        
        
        
        
        
        
        


game = Tk()
tetris = Tetris(game)
game.mainloop()
