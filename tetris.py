import pygame as pg

BLOCK_SIZE = 20
FALL_TIME = 0.1

def clamp(n, min_n, max_n):
    return min(max(n, min_n), max_n)

class Block(object):
    def __init__(self, pos : pg.Vector2, color : pg.Color):
        self.pos = pos
        self.color = color

    def move(self, x_offset, y_offset):
        pos = pg.Vector2(0, 0)
        pos.x = clamp(self.pos.x + x_offset, 0, 9)
        pos.y = self.pos.y + y_offset
        if pos.y < len(field.grid_pos[0]) and field.is_empty(pos):
            self.pos = pos
            return True
        else:
            return False

    def draw(self):
        rect = pg.Rect(field.grid_pos[int(self.pos.x)][int(self.pos.y)], (BLOCK_SIZE, BLOCK_SIZE))
        pg.draw.rect(screen, self.color, rect)

class Field(object):
    def __init__(self, x, y):
        self.grid_pos = [[pg.Vector2(x * BLOCK_SIZE, y * BLOCK_SIZE) for y in range(y)] for x in range(x)]
        self.grid  = [[None for y in range(y)] for x in range(x)]

    def is_empty(self, pos :pg.Vector2):
        return self.grid[int(pos.x)][int(pos.y)] is None

    def place(self, block :Block):
        self.grid[int(block.pos.x)][int(block.pos.y)] = block

    def draw(self):
        for column in self.grid:
            for cell in column:
                if not (cell is None):
                    cell.draw()


screen = pg.display.set_mode((200, 400))
clock = pg.time.Clock()

field = Field(10, 20)
block = Block(pg.Vector2(1, 1), pg.Color(255, 0, 0))
dt = 0
movement_direction = 0
running = True

fall_timer = FALL_TIME
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_d or event.key == pg.K_RIGHT:
                movement_direction = min(movement_direction + 1, 1)
            elif event.key == pg.K_a or event.key == pg.K_LEFT:
                movement_direction = max(movement_direction - 1, -1)
    #clear
    screen.fill("black")
    
    #rendering
    fall_timer -= dt
    if fall_timer <= 0:
        if not block.move(0, 1):
            field.place(block)
            block = Block(pg.Vector2(0,0), pg.Color(255, 0, 0))

        fall_timer = FALL_TIME

    block.move(movement_direction, 0)
    movement_direction = 0

    block.draw()
    field.draw()

    #show frame
    pg.display.flip()
    
    #limit fps
    dt = clock.tick(60) / 1000

pg.quit()
