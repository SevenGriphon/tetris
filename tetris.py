import pygame as pg
from pygame import Vector2

BLOCK_SIZE = 20
FALL_TIME = 0.25

def clamp(n, min_n, max_n):
    return min(max(n, min_n), max_n)

class Shape(object):
    def __init__(self, shape_map, color, shape_pos):
        self.pos = shape_pos
        self.blocks = []
        for pos in shape_map:
            self.blocks.append(Block(shape_pos + pg.Vector2(pos[0], pos[1]), color))

    def move(self, x_offset, y_offset):
        shape_can_move = True
        for block in self.blocks:
            shape_can_move = shape_can_move and block.can_move(x_offset, y_offset)
        if shape_can_move:
            for block in self.blocks:
                block.move(x_offset, y_offset)
            self.pos += pg.Vector2(x_offset, y_offset)

        return shape_can_move

    def draw(self):
        for block in self.blocks:
            block.draw()

    def place(self):
        for block in self.blocks:
            field.place(block)

    def rotate(self):
        can_rotate = True
        for block in self.blocks:
            block_pos = block.pos-self.pos
            block_new_pos = pg.Vector2(block_pos.y, -block_pos.x)
            block_offset = block_new_pos - block_pos
            if not block.can_move(block_offset.x, block_offset.y):
                can_rotate = False
                break

        if can_rotate:
            for block in self.blocks:
                block_pos = block.pos - self.pos
                block_new_pos = pg.Vector2(block_pos.y, -block_pos.x)
                block_offset = block_new_pos - block_pos
                block.move(block_offset.x, block_offset.y)



class Block(object):
    def __init__(self, pos : pg.Vector2, color : pg.Color):
        self.pos = pos
        self.color = color

    def can_move(self, x_offset, y_offset):
        pos = self.pos + pg.Vector2(x_offset, y_offset)
        in_x_bounds = len(field.grid_pos) > pos.x >= 0
        in_y_bounds = 0 <= pos.y < len(field.grid_pos[0])
        if in_x_bounds and in_y_bounds and field.is_empty(pos):
            return True
        else:
            return False

    def move(self, x_offset, y_offset):
        if self.can_move(x_offset, y_offset):
            self.pos += pg.Vector2(x_offset, y_offset)
            return True
        else:
            return False


    def draw(self):
        rect = pg.Rect(field.grid_pos[int(self.pos.x)][int(self.pos.y)], (BLOCK_SIZE, BLOCK_SIZE))
        pg.draw.rect(screen, self.color, rect)

class Field(object):
    def __init__(self, x, y):
        self.grid_pos = [[pg.Vector2(x * BLOCK_SIZE, y * BLOCK_SIZE) for y in range(y)] for x in range(x)]
        self.grid :list[list[Block|None]] = [[None for y in range(y)] for x in range(x)]

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
shape = Shape([(0,0), (0,1), (0, 2), (1, 2)], pg.Color(255, 255, 0), pg.Vector2(0, 0))
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
            elif event.key == pg.K_w or event.key == pg.K_UP:
                shape.rotate()
    #clear
    screen.fill("black")
    
    #rendering
    fall_timer -= dt
    if fall_timer <= 0:
        if not shape.move(0, 1):
            shape.place()
            shape = Shape([(0,0), (0,1), (0, 2), (1, 2)], pg.Color(255, 255, 0), pg.Vector2(0, 0))

        fall_timer = FALL_TIME

    shape.move(movement_direction, 0)
    movement_direction = 0

    shape.draw()
    field.draw()

    #show frame
    pg.display.flip()
    
    #limit fps
    dt = clock.tick(60) / 1000

pg.quit()
