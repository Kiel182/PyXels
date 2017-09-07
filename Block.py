
import OpenGL.GL as gl
import OpenGL.GLU as glu
from PyQt5.QtGui import QColor

class Block:
    trolltechGreen = QColor.fromCmykF(0.40, 0.0, 1.0, 0.0)
    trolltechPurple = QColor.fromCmykF(0.39, 0.39, 0.0, 0.0)

    def __init__(self):
        self.x0 = 0.0
        self.y0 = 0.0
        self.z0 = 0.0

        self.vertices = (
            (self.x0 + 1, self.y0,     self.z0),
            (self.x0 + 1, self.y0 + 1, self.z0),
            (self.x0,     self.y0 + 1, self.z0),
            (self.x0,     self.y0,     self.z0),
            (self.x0 + 1, self.y0,     self.z0 + 1),
            (self.x0 + 1, self.y0 + 1, self.z0 + 1),
            (self.x0,     self.y0,     self.z0 + 1),
            (self.x0,     self.y0 + 1, self.z0 + 1)
        )

        self.edges = (
            (0, 1),
            (0, 3),
            (0, 4),
            (2, 1),
            (2, 3),
            (2, 7),
            (6, 3),
            (6, 4),
            (6, 7),
            (5, 1),
            (5, 4),
            (5, 7)
        )

        self.surfaces = (
            (0, 1, 2, 3),
            (3, 2, 7, 6),
            (6, 7, 5, 4),
            (4, 5, 1, 0),
            (1, 5, 7, 2),
            (4, 0, 3, 6)
        )

        self.isActive = False

    def __init__(self, x, y, z):
        self.x0 = x
        self.y0 = y
        self.z0 = z

        self.vertices = (
            (self.x0 + 1, self.y0,     self.z0),
            (self.x0 + 1, self.y0 + 1, self.z0),
            (self.x0,     self.y0 + 1, self.z0),
            (self.x0,     self.y0,     self.z0),
            (self.x0 + 1, self.y0,     self.z0 + 1),
            (self.x0 + 1, self.y0 + 1, self.z0 + 1),
            (self.x0,     self.y0,     self.z0 + 1),
            (self.x0,     self.y0 + 1, self.z0 + 1)
        )

        self.edges = (
            (0, 1),
            (0, 3),
            (0, 4),
            (2, 1),
            (2, 3),
            (2, 7),
            (6, 3),
            (6, 4),
            (6, 7),
            (5, 1),
            (5, 4),
            (5, 7)
        )

        self.surfaces = (
            (0, 1, 2, 3),
            (3, 2, 7, 6),
            (6, 7, 5, 4),
            (4, 5, 1, 0),
            (1, 5, 7, 2),
            (4, 0, 3, 6)
        )

        self.isActive = False

    def paint(self):
        gl.glBegin(gl.GL_LINES)
        self.setColor(self.trolltechPurple)
        for edge in self.edges:
            for vertex in edge:
                gl.glVertex3fv(self.vertices[vertex])

        gl.glEnd()

        if self.isActive:
            gl.glBegin(gl.GL_QUADS)
            self.setColor(self.trolltechGreen)
            for surface in self.surfaces:
                for vertex in surface:
                    gl.glVertex3fv(self.vertices[vertex])

            gl.glEnd()

    def setColor(self, c):
        gl.glColor4f(c.redF(), c.greenF(), c.blueF(), c.alphaF())