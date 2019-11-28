from PySide2.QtWidgets import QOpenGLWidget
from PySide2.QtGui import QMouseEvent, QMatrix4x4, QVector3D, QVector4D
from PySide2.QtCore import QObject, QRect, QPoint, QSize, Signal, Slot
from OpenGL import GL as gl
from signals import Signals, DragInfo
from pyD3VBasicPainter import BasicPainter
class GlWin(QOpenGLWidget):
    glPainters = [BasicPainter()]
    mv = QMatrix4x4
    proj = QMatrix4x4
    vport = QRect
    eye = QVector3D(0, 0, 10.0)  # position of the viewer
    poi = QVector3D(0, 0, 0)  # point of interest
    phi = 0.0  # rotation about X
    theta = 0.0  # rotation about Y
    #def __init__(self,  parent=None):
        #pass
        #QOpenGLWidget.__init__(self,parent)
        #QOpenGLFunctions.__init__(self)

    def paintGL(self):
        self.mv = QMatrix4x4()
        self.mv.rotate(self.theta * 57.3, 0.0, 1.0, 0.0) # rotation about Y
        self.mv.rotate(self.phi * 57.3, 1.0, 0.0, 0.0) # rotation about X
        self.mv.translate(-self.eye)

        for p in self.glPainters:
            p.setprogramvalues(self.proj, self.mv, self.mv.normalMatrix(), QVector3D(0, 0, 70))

        for p in self.glPainters:
            p.paintGL()


    def initializeGL(self):
        Signals.get().updateGL.connect(self.updateGL)
        Signals.get().dragging.connect(self.onDrag)

        for p in self.glPainters:
            p.initializeGL()

    def resizeGL(self, w:int, h:int):
#        self.vport.setWidth(w)
#        self.vport.setHeight(h)

        ratio = float(w)/float(h)
        self.proj = QMatrix4x4()
        self.proj.ortho(-10*ratio,10*ratio,-10,10,-10,10)

        for p in self.glPainters:
            p.resizeGL(w,h)

    def addPainter(self, painter):
        self.glPainters.append(painter)

    def mouseMoveEvent(self, event:QMouseEvent):
        self.dragInfo.update(event.pos())
        Signals.get().dragging.emit(self.dragInfo)

    def mouseDoubleClickEvent(self, event:QMouseEvent):
        pass

    def mousePressEvent(self, event:QMouseEvent):
        self.dragInfo = DragInfo(event.pos(), self.geometry(), QMatrix4x4(), QMatrix4x4(), QRect())
        Signals.get().draggingBegin.emit(self.dragInfo)

    def mouseReleaseEvent(self, event:QMouseEvent):
        self.dragInfo.update(event.pos())
        Signals.get().draggingEnd.emit(self.dragInfo)


    @Slot()
    def updateGL(self):
        self.update()

    @Slot()
    def onDrag(self, di:DragInfo):
        d = di.normalizedDelta
        self.phi = d.y() * 3.14
        self.theta = d.x() * 3.14
        self.update()


