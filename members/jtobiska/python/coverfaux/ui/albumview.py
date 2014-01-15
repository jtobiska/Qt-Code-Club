# =============================================================================
# coverfaux.ui.albumview
# =============================================================================
"""Defines a widget for viewing album artwork."""

__author__ = "Joey Tobiska"

# =============================================================================
# IMPORTS
# =============================================================================

# Standard imports
from PySide import QtGui, QtCore

# Qt-Code-Club imports
from analbumcover import AnAlbum

# =============================================================================
# CLASSES
# =============================================================================

class Pixmap(QtCore.QObject):

    def __init__(self, graphicsItem, parent=None):
        super(Pixmap, self).__init__(parent)
        self._graphicsItem = graphicsItem

    @property
    def graphicsItem(self):
        return self._graphicsItem

    @QtCore.Property(float)
    def opacity(self):
        return self._graphicsItem.opacity()

    @opacity.setter
    def _opacity(self, opacity):
        self._graphicsItem.setOpacity(opacity)

# =============================================================================

class AlbumsWidget(QtGui.QFrame):

    _ALBUMS = (
        ("Weezer", "Blue"),
        ("Weezer", "Green"),
        ("Imagine Dragons", "Night Visions"),
        ("Green Day", "Dookie"),
        ("Green Day", "American Idiot"),
        ("Green Day", "Insomniac"),
        ("Jimmy Eat World", "Bleed American"),
        ("Jimmy Eat World", "Clarity"),
    )

    def __init__(self, parent=None):
        super(AlbumsWidget, self).__init__(parent)
        self._art = None
        self._currentArtIndex = -1
        self._scene = QtGui.QGraphicsScene(self)
        self._view = QtGui.QGraphicsView(self._scene, self)
        self._view.setSceneRect(0, 0, 500, 500)
        pixmapItem = QtGui.QGraphicsPixmapItem()
        self._pixmapWrapper = Pixmap(pixmapItem)
        self._textItem = QtGui.QGraphicsTextItem()
        self._scene.addItem(pixmapItem)
        self._scene.addItem(self._textItem)
        pixmapItem.setPos(0, 0)
        self._textItem.setPos(0, 0)
        self._view.setRenderHints(QtGui.QPainter.Antialiasing)
        self._mainLayout = QtGui.QVBoxLayout()
        self._mainLayout.addWidget(self._view)
        self.setLayout(self._mainLayout)
        self.nextArt()

    def nextArt(self):
        if self._currentArtIndex < len(self._ALBUMS) - 1:
            self._currentArtIndex += 1
        else:
            self._currentArtIndex = 0
        albumInfo = self._ALBUMS[self._currentArtIndex]
        album = AnAlbum(albumInfo[0], albumInfo[1], fetch=False)
        album.fetchMetadata()        
        self._art = album.arts[-1]
        self._art.downloadComplete.connect(self.showImage)
        self._art.downloadProgress.connect(self.showProgress)
        self._art.download(blocking=False)

    def showImage(self):
        pixmap = QtGui.QPixmap(self._art.image.scaled(500, 500, QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.SmoothTransformation))
        self._pixmapWrapper.graphicsItem.setPixmap(pixmap)
        anim = QtCore.QPropertyAnimation(self)
        anim.setPropertyName("opacity")
        anim.setTargetObject(self._pixmapWrapper)
        anim.setDuration(750)
        anim.setStartValue(0.0)
        anim.setEndValue(1.0)
        anim.setEasingCurve(QtCore.QEasingCurve.InOutBack)
        anim.start()
        self.startTimer(3000)

    def showProgress(self, received, total):
        self._textItem.setPlainText("{0}/{1}".format(received, total))

    def timerEvent(self, event):
        self.killTimer(event.timerId())
        self.nextArt()


# =============================================================================
