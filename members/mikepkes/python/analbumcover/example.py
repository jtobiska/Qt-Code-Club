
import sys
sys.path.append("../")
from PySide import QtGui
from analbumcover import AnAlbum


class Demo(QtGui.QLabel):
    def __init__(self, parent=None):
        super(Demo, self).__init__(parent)

        self.setWindowTitle("Asynchronus")
        self.setFixedSize(100,100)
        self.show()
        self.raise_()

        album = AnAlbum('Weezer', 'Green', fetch=False)
        album.fetchMetadata()
        self._art = album.arts[-1]
        self._art.downloadComplete.connect(self.showImage)
        self._art.download(blocking=False)
    def showImage(self):
        self.setPixmap(QtGui.QPixmap(self._art.image))
        self.setFixedSize(self._art.image.size())

if 1:

    app = QtGui.QApplication(sys.argv)
    w = Demo()
    app.exec_()

if 0:

    app = QtGui.QApplication(sys.argv)
    album = AnAlbum('Weezer', 'Blue', fetch=True)
    art = album.arts[-1]
    w = QtGui.QLabel()
    w.setWindowTitle("Synchronous")
    w.setFixedSize(art.image.size())
    w.setPixmap(QtGui.QPixmap(art.image))
    w.show()
    w.raise_()
    app.exec_()
