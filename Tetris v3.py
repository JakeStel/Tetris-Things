from tkinter import *
import random
from matrix_rotation import rotate_array as ra
import RPi.GPIO as GPIO


buttons = [18,19,20,21]
GPIO.setmode(GPIO.BCM)
GPIO.setup(buttons, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

DEBUG = False

#==Side Class===#
class Shape:
    def __init__(self, shape, piece, row, column, coords):
        self.shape = shape
        self.piece = piece
        self.row = row
        self.col = column
        self.coords = coords

#===Main Class===#
class Tetris:
    def __init__(self, master):
        master.title("Tetris")
        self.master = master
        self.grid_width = 10
        self.grid_height = 24
        self.grid = [['' for col in range(self.grid_width)] for row in range(self.grid_height)]
        self.field = [[None for column in range(self.grid_width)]for row in range(self.grid_height)]
        self.w = 300
        self.h = 720
        self.square_w = self.w//10
        self.canvas = Canvas(game, height = self.h, width = self.w)
        self.canvas.grid(row=0, column = 0)
        self.startLine = self.canvas.create_line(0, self.h/6, self.w, self.h/6, width = 2)
        self.R_border = self.canvas.create_line(self.w, 0, self.w, self.h, width = 2)
        self.tickrate = 1000
        self.spawning = False
        self.master.after(self.tickrate, self.fps)
        self.active_piece_state = False

        #=Creating the Shapes=#
        self.Pool = ['s','z','r','L','o','I','T']
        self.color = {'s':'green',
                      'z':'red',
                      'r':'orange',
                      'L':'blue',
                      'o':'yellow',
                      'I':'cyan',
                      'T':'purple'}
                      
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
        GPIO.add_event_detect(buttons[0], GPIO.RISING, callback = self.move)
        self.master.bind('<q>', self.rotation)
        GPIO.add_event_detect(buttons[1], GPIO.RISING, callback = self.move)
        self.master.bind('<e>', self.rotation)
        self.master.bind('<Left>', self.move)
        GPIO.add_event_detect(buttons[2], GPIO.RISING, callback = self.move)
        self.master.bind('<Right>', self.move)
        GPIO.add_event_detect(buttons[3], GPIO.RISING, callback = self.move)
        

                       

        
#====================FPS Function===================#
    def fps(self):
        if DEBUG:
            print("fps is ticking")
        if not self.spawning:
            self.add_piece()
            self.spawning = not self.spawning
            
        self.move()
        
        self.master.after(self.tickrate, self.fps)
        
#=====================Direction Function==================#
    def Direction(self, event):
        if DEBUG:
            print('Keysym:',event.keysym)
        if type(event) == int:
            direction = event
            if direction == 18:
                direction = 'Down'
            elif direction == 19:
                direction = 'Left'
            elif direction == 20:
                direction = 'Right'
            
        elif event == None:
            direction = 'Down'
        else:
            direction = (event and event.keysym) or 'Down'
        return direction


#====================Movement Function====================#
    def move(self, event=None):
        
        if not self.spawning:
            return
        
        r = self.active_piece.row
        c = self.active_piece.col
        l = len(self.active_piece.shape)
        w = len(self.active_piece.shape[0])

        direction = self.Direction(event)
        if DEBUG:
            print('Keysym:',direction)
        
        
        if direction == 'Down':
            if r+l >= self.grid_height:
                self.bottom(r+1)
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

        #collision code
        for row, blocks in zip(range(rt, rt+l),
                               self.active_piece.shape
                               ):
                for column, block in zip(range(ct,ct+w), blocks):
                    if block and self.grid[row][column] == 'x':
                        if direction == 'Down':
                            self.bottom(r)
                        return

                    

        for row in self.grid:
            row[:] = ['' if cell == '*' else cell for cell in row]
            

        #=Moves Piece Down=#
        if direction == 'Down':
            self.grid[r][c:c+w] = ['' if p else b for b,p in zip(self.grid[r][c:c+w],self.active_piece.shape[0])]
            self.active_piece.row += 1
            r += 1


            
        #=Moves Piece Left and Right=#    
        else:
            if direction == 'Left':
                #column = c+w
                self.active_piece.col -= 1 
                c -= 1
            elif direction == 'Right':
                #column = c-1
                self.active_piece.col += 1
                c += 1

           
        for row, blocks in zip(range(r, r+l),
                               self.active_piece.shape):
            
            for column, block in zip(range(c,c+w),blocks):
                if block:
                    self.grid[row][column] = block

        for id,coords_idx in zip(self.active_piece.piece, range(len(self.active_piece.coords))):

            #=Moves Block on Canvas=#
            x1,y1,x2,y2 = self.active_piece.coords[coords_idx]
            if direction == 'Down':
                y1 += self.square_w
                y2 += self.square_w
            elif direction == 'Left':
                x1 -= self.square_w
                x2 -= self.square_w
            elif direction == 'Right':
                x1 += self.square_w
                x2 += self.square_w
                
            self.active_piece.coords[coords_idx] = x1,y1,x2,y2
            self.canvas.coords(id, self.active_piece.coords[coords_idx])
        #print(self.active_piece)
#====================Check&Move Function====================#
    def check_and_move(self, r, c):
        pass
        
#====================Rotation Function====================#
    def rotation(self, event=None):
        if not self.active_piece:
            return
        r = self.active_piece.row
        c = self.active_piece.col
        l = len(self.active_piece.shape)
        w = len(self.active_piece.shape[0])
        x = c + w//2 #center for old shape
        y = r + l//2 #center for old shape
        direction = event.keysym
        if direction == 'q':
            direction = 'left'
            shape = ra(self.active_piece.shape, -90)
        elif direction == 'e':
            direction = 'right'
            shape = ra(self.active_piece.shape, 90)

        l = len(shape) #rotated length
        w = len(shape[0]) #rotated width
        rt= y - l//2 #rotated row
        ct= x - w//2  #rotated column
        if w%2:
            if direction == 'right':
                ct += 1
            elif direction == 'left':
                ct -= 1
        if l%2:
            if direction == 'right':
                rt += 1
            elif direction == 'left':
                rt -= 1
            
        for row, blocks in zip(range(rt, rt+l),
                               shape
                               ):
                
                for column, block in zip(range(ct,ct+w), blocks):
                    if block and self.grid[row][column] == 'x':
                        return

        self.active_piece.shape = shape

        x_start = min(coord for tup in self.active_piece.coords for coord in (tup[0], tup[2]))
        y_start = min(coord for tup in self.active_piece.coords for coord in (tup[1], tup[3]))
        squares = iter(range(4)) # iterator of 4 indices
        for row_coord, row in zip(range(y_start, y_start+l*self.square_w+1,self.square_w),
                                shape):
            for col_coord, cell in zip(range(x_start, x_start+w*self.square_w+1,self.square_w),
                                       row):
                if cell:
                    square_idx = next(squares)
                    coord = (col_coord,
                             row_coord,
                             col_coord+self.square_w,
                             row_coord+self.square_w)
                    self.active_piece.coords[square_idx] = coord
                    self.canvas.coords(self.active_piece.piece[square_idx], coord)

        if DEBUG:
            for row in shape:
                print(*(cell or ' ' for cell in row))
            print(direction)
            



    def bottom(self, r):
        #Checks for loss by height
        self.spawning = not self.spawning
        if DEBUG:
            print("Piece has reached the bottom")
            for row in self.grid:
                print(row)
        if r == 0:
            self.loss()
            return

        for row in self.grid:
            row[:] = ['x' if cell == '*' else cell for cell in row]
        for (x1,y1,x2,y2),id in zip(self.active_piece.coords, self.active_piece.piece):
            self.field[y1//self.square_w][x1//self.square_w] = id
        indices = [idx for idx, row in enumerate(self.grid) if all(row)]
        if indices:
            self.remove_line(indices)
        

    def add_piece(self):
        if DEBUG:
            print("Creating random piece")
        if self.Pool == []:
            self.Pool = ['s','z','r','L','o','I','T']

        Chossen = random.choice(self.Pool)
        self.Pool.remove(Chossen)
        shape = self.shapes[Chossen]
        shape = ra(shape, random.choice((0,90,180,270)))
        w = len(shape[0])
        startUp = (10-w)//2
        self.active_piece = Shape(shape,[], 0, startUp, [])
        for y,row in enumerate(shape):
            self.grid[y][startUp:startUp+w] = shape[y]
            for x,grid_cell in  enumerate(row, start=startUp):

                #=Takes Coords of each block and appends to list=#
                if grid_cell:
                    self.active_piece.coords.append((self.square_w*x,
                                                        self.square_w*y,
                                                        self.square_w*(x+1),
                                                        self.square_w*(y+1)))
                    
                    #piece is created
                    self.active_piece.piece.append(
                        self.canvas.create_rectangle(self.active_piece.coords[-1],
                                                     fill=self.color[Chossen], width=2))


    def loss(self):
        pass

    def remove_line(self, indices):
        for idx in indices:
            self.grid.pop(idx)
            self.grid.insert(0, ['' for column in range(self.grid_width)])
        self.Sweep(indices)

    def Sweep(self, indices,current_column=0):
        for row in indices:
            id = self.field[row][current_column]
            self.field[row][current_column] = None
            self.canvas.delete(id)
        if current_column < self.grid_width-1:
            self.master.after(100, self.Sweep, indices, current_column+1)
        else:
            for idx,row in enumerate(self.field):
                offset = sum(r > idx for r in indices)*self.square_w
                for square in row:
                    if square:
                        self.canvas.move(square, 0, offset)
            for row in indices:
                self.field.pop(row)
                self.field.insert(0, [None for x in range(self.grid_width)])
            
                
                
                
        

    

    

game = Tk()
tetris = Tetris(game)
game.mainloop()
