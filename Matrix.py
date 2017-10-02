from Block import Block
import numpy as np


class Matrix:
    def __init__(self, width, height, depth):
        self.width = width
        self.height = height
        self.depth = depth

        self.x0 = -(width/2)
        self.y0 = -(height/2)
        self.z0 = -(depth/2)

        self.xf = width / 2
        self.yf = height / 2
        self.zf = depth / 2

        self.blocks = np.ndarray((width, height, depth), Block)

        id = 0

        for x in range(0, width):
            for y in range(0, height):
                for z in range(0, depth):
                    self.blocks[x, y, z] = Block(x + self.x0, y + self.y0, z + self.z0, id)
                    id += 1

        self.blocks[0, 0, self.depth - 1].select()

    def paint(self):
        for x in range(0, self.width):
            for y in range(0, self.height):
                for z in range(0, self.depth):
                    self.blocks[x, y, z].paint()

    def showGrid(self, show):
        for x in range(0, self.width):
            for y in range(0, self.height):
                for z in range(0, self.depth):
                    self.blocks[x, y, z].show_grid = show

    def paintForPick(self):
        for x in range(0, self.width):
            for y in range(0, self.height):
                for z in range(0, self.depth):
                    self.blocks[x, y, z].paintForPick()