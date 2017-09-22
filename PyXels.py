import sys
import math

from PyQt5.QtCore import pyqtSignal, QPoint, QSize, Qt, pyqtSlot
from PyQt5.Qt import QVector3D, QVector4D
from PyQt5.QtGui import *
from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QVBoxLayout, QOpenGLWidget, QSlider,
                             QWidget, QSizePolicy, QSpinBox, QColorDialog, QCheckBox, QPushButton)

import OpenGL.GL as gl
import OpenGL.GLU as glu

from Matrix import Matrix
import numpy as np


class Window(QWidget):

    def __init__(self):
        super(Window, self).__init__()

        self.glWidget = GLWidget()
        self.glWidget.setMinimumSize(800, 600)
        self.spinHeight = QSpinBox()
        self.spinWidth = QSpinBox()
        self.spinDepth = QSpinBox()
        self.showGrid = QCheckBox()
        self.colorButton = QPushButton()

        self.showGrid.setChecked(True)
        self.showGrid.setText("Show grid")
        self.showGrid.clicked.connect(self.updateGrid)

        self.spinHeight.setPrefix("Height : ")
        self.spinWidth.setPrefix("Width : ")
        self.spinDepth.setPrefix("Depth : ")

        self.spinDepth.setMinimum(1)
        self.spinWidth.setMinimum(1)
        self.spinHeight.setMinimum(1)

        self.spinDepth.setValue(5)
        self.spinWidth.setValue(5)
        self.spinHeight.setValue(5)

        self.spinHeight.valueChanged.connect(self.updateMatrix)
        self.spinWidth.valueChanged.connect(self.updateMatrix)
        self.spinDepth.valueChanged.connect(self.updateMatrix)

        self.colorButton.setText("Pick Color")
        self.colorButton.clicked.connect(self.color_picker)

        mainLayout = QHBoxLayout()
        mainLayout.addWidget(self.glWidget) 
        subLayout = QVBoxLayout()
        subLayout.addWidget(self.showGrid)
        subLayout.addWidget(self.spinHeight)
        subLayout.addWidget(self.spinWidth)
        subLayout.addWidget(self.spinDepth)
        subLayout.addWidget(self.colorButton)
        mainLayout.addLayout(subLayout)
        self.setLayout(mainLayout)

        self.setMinimumSize(800, 600)

        self.setWindowTitle("PyXels")

    @pyqtSlot()
    def color_picker(self):
        color = QColorDialog.getColor()
        self.glWidget.setSelectedColor(color)

    @pyqtSlot()
    def updateMatrix(self):
        self.glWidget.setMatrixSize(self.spinWidth.value(),
                                    self.spinHeight.value(),
                                    self.spinDepth.value())
        self.glWidget.selectedX = 0
        self.glWidget.selectedY = 0
        self.glWidget.selectedZ = 0

    @pyqtSlot()
    def updateGrid(self):
        self.glWidget.matrix.showGrid(self.showGrid.isChecked())
        self.glWidget.updateGL()


class GLWidget(QOpenGLWidget):
    xRotationChanged = pyqtSignal(int)
    yRotationChanged = pyqtSignal(int)
    zRotationChanged = pyqtSignal(int)

    def __init__(self, parent=None):
        super(GLWidget, self).__init__(parent)

        self.setFocusPolicy(Qt.StrongFocus)

        self.object = 0
        self.xRot = 0
        self.yRot = 0
        self.zRot = 0
        self.translateX = 0.0
        self.translateY = 0.0
        self.zoom = -15.0
        self.ctlPressed = False

        self.matrix = Matrix(5, 5, 5)

        self.lastPos = QPoint()

        self.selectedX = 0
        self.selectedY = 0
        self.selectedZ = 4

        self.trolltechGreen = QColor.fromCmykF(0.40, 0.0, 1.0, 0.0)
        self.trolltechPurple = QColor.fromCmykF(0.39, 0.39, 0.0, 0.0)
        self.Black = QColor.fromCmykF(0.0, 0.0, 0.0, 0.0, 0.0)

    def getOpenglInfo(self):
        info = """
            Vendor: {0}
            Renderer: {1}
            OpenGL Version: {2}
            Shader Version: {3}
        """.format(
            gl.glGetString(gl.GL_VENDOR),
            gl.glGetString(gl.GL_RENDERER),
            gl.glGetString(gl.GL_VERSION),
            gl.glGetString(gl.GL_SHADING_LANGUAGE_VERSION)
        )

        return info

    def minimumSizeHint(self):
        return QSize(50, 50)

    def sizeHint(self):
        return QSize(800, 600)

    def setXRotation(self, angle):
        angle = self.normalizeAngle(angle)
        if angle != self.xRot:
            self.xRot = angle
            self.xRotationChanged.emit(angle)
            self.update()

    def setYRotation(self, angle):
        angle = self.normalizeAngle(angle)
        if angle != self.yRot:
            self.yRot = angle
            self.yRotationChanged.emit(angle)
            self.update()

    def setZRotation(self, angle):
        angle = self.normalizeAngle(angle)
        if angle != self.zRot:
            self.zRot = angle
            self.zRotationChanged.emit(angle)
            self.update()

    def initializeGL(self):
        print(self.getOpenglInfo())

        self.setClearColor(self.trolltechPurple.darker())
        self.object = self.makeObject()
        gl.glShadeModel(gl.GL_FLAT)
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glEnable(gl.GL_CULL_FACE)

    def paintGL(self):
        gl.glClear(
            gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        gl.glLoadIdentity()
        gl.glTranslatef(self.translateX, self.translateY, self.zoom)
        gl.glRotated(self.xRot / 16.0, 1.0, 0.0, 0.0)
        gl.glRotated(self.yRot / 16.0, 0.0, 1.0, 0.0)
        gl.glRotated(self.zRot / 16.0, 0.0, 0.0, 1.0)
        gl.glCallList(self.object)

    def resizeGL(self, width, height):
        side = min(width, height)
        if side < 0:
            return

        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        glu.gluPerspective(45, width/height, 0.1, 250.0)
        gl.glMatrixMode(gl.GL_MODELVIEW)

    def mousePressEvent(self, event):
        self.lastPos = event.pos()

        if event.buttons() & Qt.MiddleButton:
            self.resetView()
            # self.matrix.paintForPick()
            self.updateGL()



    def mouseMoveEvent(self, event):
        dx = event.x() - self.lastPos.x()
        dy = event.y() - self.lastPos.y()

        if not self.ctlPressed:
            if event.buttons() & Qt.LeftButton:
                self.setXRotation(self.xRot + 8 * dy)
                self.setYRotation(self.yRot + 8 * dx)
            elif event.buttons() & Qt.RightButton:
                self.setXRotation(self.xRot + 8 * dy)
                self.setZRotation(self.zRot + 8 * dx)

            self.lastPos = event.pos()
        else:
            if event.buttons() & Qt.LeftButton:
                self.translateX = dx / 100
                self.translateY = - dy / 100

                self.update()

    def wheelEvent(self, event):

        numdegrees = event.angleDelta() / 8
        numdegrees = numdegrees / 15

        if -200 <= self.zoom + numdegrees.y() <= 0:
            self.zoom += numdegrees.y()

        self.update()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Shift:
            self.ctlPressed = True
        elif event.key() == Qt.Key_Left and self.selectedX > 0:
            self.matrix.blocks[self.selectedX, self.selectedY, self.selectedZ].select()
            self.selectedX -= 1
            self.matrix.blocks[self.selectedX, self.selectedY, self.selectedZ].select()
            self.updateGL()
        elif event.key() == Qt.Key_Right and self.selectedX < self.matrix.width - 1:
            self.matrix.blocks[self.selectedX, self.selectedY, self.selectedZ].select()
            self.selectedX += 1
            self.matrix.blocks[self.selectedX, self.selectedY, self.selectedZ].select()
            self.updateGL()
        elif event.key() == Qt.Key_Minus and self.selectedY > 0:
            self.matrix.blocks[self.selectedX, self.selectedY, self.selectedZ].select()
            self.selectedY -= 1
            self.matrix.blocks[self.selectedX, self.selectedY, self.selectedZ].select()
            self.updateGL()
        elif event.key() == Qt.Key_Plus and self.selectedY < self.matrix.height - 1:
            self.matrix.blocks[self.selectedX, self.selectedY, self.selectedZ].select()
            self.selectedY += 1
            self.matrix.blocks[self.selectedX, self.selectedY, self.selectedZ].select()
            self.updateGL()
        elif event.key() == Qt.Key_Up and self.selectedZ > 0:
            self.matrix.blocks[self.selectedX, self.selectedY, self.selectedZ].select()
            self.selectedZ -= 1
            self.matrix.blocks[self.selectedX, self.selectedY, self.selectedZ].select()
            self.updateGL()
        elif event.key() == Qt.Key_Down and self.selectedZ < self.matrix.depth - 1:
            self.matrix.blocks[self.selectedX, self.selectedY, self.selectedZ].select()
            self.selectedZ += 1
            self.matrix.blocks[self.selectedX, self.selectedY, self.selectedZ].select()
            self.updateGL()
        elif event.key() == Qt.Key_F5:
            self.matrix.blocks[self.selectedX, self.selectedY, self.selectedZ].activate()
            self.updateGL()

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Shift:
            self.ctlPressed = False

    def makeObject(self):
        genList = gl.glGenLists(1)
        gl.glNewList(genList, gl.GL_COMPILE)

        # self.matrix.paintForPick()
        self.matrix.paint()

        gl.glEndList()

        return genList

    def normalizeAngle(self, angle):
        while angle < 0:
            angle += 360 * 16
        while angle > 360 * 16:
            angle -= 360 * 16

        return angle

    def setClearColor(self, c):
        gl.glClearColor(c.redF(), c.greenF(), c.blueF(), c.alphaF())

    def setColor(self, c):
        gl.glColor4f(c.redF(), c.greenF(), c.blueF(), c.alphaF())

    def setMatrixSize(self, x, y, z):
        self.matrix = Matrix(x, y, z)
        self.updateGL()

    def resetView(self):
        self.xRot = 0
        self.yRot = 0
        self.zRot = 0
        self.translateX = 0.0
        self.translateY = 0.0
        self.zoom = -15.0

        self.updateGL()

    def updateGL(self):
        self.object = self.makeObject()
        self.paintGL()
        self.update()

    def testRayOBBIntersection(self, ray_origin, ray_direction, aabb_min, aabb_max,
                               ModelMatrix, intersection_distance):
        tMin = 0.0
        tMax = 100000.0

        OBBposition_worldspace = np.atleast_3d()

        return False

    def setSelectedColor(self, color):
        self.matrix.blocks[self.selectedX, self.selectedY, self.selectedZ].color = color
        print("color set")


if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())