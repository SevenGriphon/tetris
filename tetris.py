import pygame as pg

BLOCK_SIZE = 20
FALL_TIME = 0.5

def clamp(n, min_n, max_n):
    return min(max(n, min_n), max_n)

class Block(object):
    def __init__(self, pos : pg.Vector2, color : pg.Color):
        self.pos = pos
        self.color = color

    def move(self, x_offset, y_offset):
        self.pos.x = clamp(self.pos.x + x_offset, 0, 9)
        self.pos.y = clamp(self.pos.y + y_offset, 0, 19)

    def draw(self):
        rect = pg.Rect(grid[int(self.pos.x)][int(self.pos.y)], (BLOCK_SIZE, BLOCK_SIZE))
        pg.draw.rect(screen, self.color, rect)


screen = pg.display.set_mode((200, 400))
clock = pg.time.Clock()

grid = [[pg.Vector2(x * BLOCK_SIZE, y * BLOCK_SIZE) for y in range(20)] for x in range(10)]

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
        if block.pos.y < len(grid[0])-1:
            block.move(0, 1)

        fall_timer = FALL_TIME

    block.move(movement_direction, 0)
    movement_direction = 0

    block.draw()


    #show frame
    pg.display.flip()
    
    #limit fps
    dt = clock.tick(60) / 1000

pg.quit()
