import pygame
import random
import sys
pygame.init()

width = 500
height = 500

rows = 25
cols = 20

black = 0,0,0
white = 255, 0, 0

class snake():
    body = []
    turns = {}

    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)

    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dX, tail.dY

        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0]-1,tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0]+1,tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0],tail.pos[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0],tail.pos[1]+1)))

        self.body[-1].dX = dx
        self.body[-1].dY = dy

        def draw(self, surface):
            for i,c in enumerate(self.body):
                if i == 0:
                    c.draw(surface, True)
            else:
                c.draw(surface) 
    
    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed()

            for key in keys:
                if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                    self.dX = -1
                    self.dY = 0
                    self.turns[self.head.pos[:]] = [self.dX,self.dY]
                elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                    self.dX = 1
                    self.dY = 0
                    self.turns[self.head.pos[:]] = [self.dX,self.dY]
                elif keys[pygame.K_UP] or keys[pygame.K_w]:
                    self.dY = -1
                    self.dX = 0
                    self.turns[self.head.pos[:]] = [self.dX,self.dY]
                elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                    self.dY = 1
                    self.dX = 0
                    self.turns[self.head.pos[:]] = [self.dX,self.dY]
        
        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body)-1:
                    self.turns.pop(p)
            else:
                c.move(c.dX,c.dY)

    def draw(self, surface):
        for i,c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)

    def reset(self,pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dX = 0
        self.dY = 1


class cube():
    rows = 25
    width = 500

    def __init__(self, start_pos, dX=1, dY=0, color=(255,0,0)):
        self.pos = start_pos
        self.dX = dX
        self.dY = dY
        self.color = color

    def draw(self, surface, eyes=False):
        dis = self.width // self.rows

        i = self.pos[0]
        j = self.pos[1]

        pygame.draw.rect(surface, self.color, (i*dis+1,j*dis+1,dis-2,dis-2))
    
        if eyes:
            centre = dis//2
            radius = 3
            circleMiddle = (i*dis+centre-radius,j*dis+8)
            circleMiddle2 = (i*dis + dis -radius*2, j*dis+8)
            pygame.draw.circle(surface, (255,255,255), circleMiddle, radius)
            pygame.draw.circle(surface, (255,255,255), circleMiddle2, radius)

    def move(self, dX, dY):
        self.dX = dX
        self.dY = dY
        self.pos = (self.pos[0] + self.dX, self.pos[1] + self.dY)

def cRandomSnack(rows, item):
    positions = item.body

    while True:
        x = random.randrange(1,rows-1)
        y = random.randrange(1,rows-1)
        if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0:
               continue
        else:
               break

    return (x,y)

def reDraw():
    global scr
    scr.fill((0,0,0))
    s.draw(scr)
    snack.draw(scr)
    pygame.display.update()
    pass


def main(): 

    global s, snack, scr
    scr = pygame.display.set_mode((width,height))
    s = snake(white,(10,10))
    s.addCube()
    snack = cube(cRandomSnack(rows,s), color = (0,255,0))

    clock = pygame.time.Clock()

    while True: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
    
        pygame.time.delay(50)
        clock.tick(10)
        s.move()
        startPos = s.head

        if s.body[0].pos == snack.pos:
            s.addCube()
            snack = cube(cRandomSnack(rows,s), color=(0,255,0))

        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z:z.pos,s.body[x+1:])):
                print("Score:", len(s.body))
                s.reset((10,10))
                break
            
            if s.body[x].pos[0] >= 25 or s.body[x].pos[0] <= -2:
                s.reset((10,10))
                break 
            if s.body[x].pos[1] >= 25 or s.body[x].pos[1] <= -2:
                s.reset((10,10))
                break
            
                    
        reDraw()
        
main()