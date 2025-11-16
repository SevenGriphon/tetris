import pygame as pg
import random

from contourpy.typecheck import check_lines
from soupsieve.util import lower

BLOCK_SIZE = 20
FALL_TIME = 0.25

def clamp(n, min_n, max_n):
    return min(max(n, min_n), max_n)

class Shape(object):
    def __init__(self, shape_map, color, shape_pos):
        left, top = shape_map[0] - shape_pos
        for block in shape_map[1:]:
            left = min(left, block[0])
            top = min(top, block[1])
        left_top_coner = pg.Vector2(left, top)
        self.blocks = []
        self.core_block = None
        for pos in shape_map:
            # color_ = pg.Color(255, 0, 0) if pos[0]==0==pos[1] else color
            block = Block(shape_pos - left_top_coner + pg.Vector2(pos[0], pos[1]), color)
            if pos[0]==0==pos[1]:
                self.core_block = block
            self.blocks.append(block)


    def move(self, x_offset, y_offset):
        shape_can_move = True
        for block in self.blocks:
            shape_can_move = shape_can_move and block.can_move(x_offset, y_offset)
        if shape_can_move:
            for block in self.blocks:
                block.move(x_offset, y_offset)

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
            block_pos = block.pos-self.core_block.pos
            block_new_pos = pg.Vector2(block_pos.y, -block_pos.x)
            block_offset = block_new_pos - block_pos
            if not block.can_move(block_offset.x, block_offset.y):
                can_rotate = False
                break

        if can_rotate:
            for block in self.blocks:
                block_pos = block.pos - self.core_block.pos
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
        self.check_lines()

    def check_lines(self):
        for y in range(len(self.grid[0])):
            is_full = True
            for x in range(len(self.grid)):
                if self.grid[x][y] is None:
                    is_full = False
                    break
            if is_full:
                for x in range(len(self.grid)):
                    self.grid[x][y] = None
                self.lower_lines(y)

    def lower_lines(self, start_from):
        for y in range(start_from, 0, -1):
            for x in range(len(self.grid)):
                self.grid[x][y] = self.grid[x][y-1]
                if not self.grid[x][y] is None:
                    self.grid[x][y].pos = pg.Vector2(x, y)



    def draw(self):
        for column in self.grid:
            for cell in column:
                if not (cell is None):
                    cell.draw()


shapes = [
    {"shape_map": [(0,-1), (0,0), (0, 1), (0, 2)], "color": pg.Color(0, 255, 255)}, #I
    {"shape_map": [(0,-1), (0,0), (0, 1), (1, 1)], "color": pg.Color(0, 0, 255)}, #L
    {"shape_map": [(0,-1), (0,0), (0, 1), (-1, 1)], "color": pg.Color(255, 112, 0)}, #J
    {"shape_map": [(0,0), (-1,1), (0, 1), (1, 1)], "color": pg.Color(255, 0, 255)}, #T
    {"shape_map": [(0,0), (0,1), (1, 0), (1, 1)], "color": pg.Color(255, 255, 0)}, #O
    {"shape_map": [(1,-1), (0,-1), (0, 0), (-1, 0)], "color": pg.Color(0, 255, 0)}, #S
    {"shape_map": [(-1,-1), (0,-1), (0, 0), (1, 0)], "color": pg.Color(255, 0, 0)}, #Z
]
def get_random_shape():
    i = random.randint(0, len(shapes)-1)
    return Shape(shapes[i]["shape_map"], shapes[i]["color"], pg.Vector2(0, 0))

screen = pg.display.set_mode((200, 400))
clock = pg.time.Clock()

field = Field(10, 20)
shape = get_random_shape()

dt = 0
movement_direction = 0
drop = False

fall_timer = FALL_TIME
running = True
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
            elif event.key == pg.K_s or event.key == pg.K_DOWN:
                drop = True
    #clear
    screen.fill("black")
    
    #rendering
    fall_timer -= dt
    if fall_timer <= 0:
        if not shape.move(0, 1):
            shape.place()
            shape = get_random_shape()

        fall_timer = FALL_TIME

    shape.move(movement_direction, 0)
    movement_direction = 0
    if drop:
        while shape.move(0, 1):
            pass
        drop = False

    shape.draw()
    field.draw()

    #show frame
    pg.display.flip()
    
    #limit fps
    dt = clock.tick(60) / 1000

pg.quit()
