from Block import Block
import numpy as np
from time import sleep

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

        for x in range(0, width):
            for y in range(0, height):
                for z in range(0, depth):
                    self.blocks[x, y, z] = Block(x + self.x0, y + self.y0, z + self.z0)

    def paint(self):
        for x in range(0, self.width):
            for y in range(0, self.height):
                for z in range(0, self.depth):
                    # if z == 1:
                    #     self.blocks[x, y, z].isActive = True
                    self.blocks[x, y, z].paint()