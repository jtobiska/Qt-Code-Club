__author__ = 'mkessler'

import json
import urllib
import urllib2
import tempfile
from PySide import QtGui, QtCore, QtNetwork

_KEY = "6ded3932b3446fd2a3ea0979f4270c02"

class Art(QtCore.QObject):

    downloadComplete = QtCore.Signal()
    downloadProgress = QtCore.Signal(int, int)

    def __init__(self, data=None, fetch=False, parent=None):
        super(Art, self).__init__(parent)
        if data:
            self.url = data['#text']
            self.size = data['size']
            self.image = None
            if fetch:
                self.download()

    def __repr__(self):
        return "<Art(url='{u}', size={s}>".format(u=self.url, s=self.size)

    def download(self, blocking=True):
        if blocking:
            self.image = QtGui.QImage.fromData(urllib2.urlopen(self.url).read())
        else:
            self.image = None
            self._networkManager = QtNetwork.QNetworkAccessManager()
            request = QtNetwork.QNetworkRequest()
            request.setUrl(QtCore.QUrl(self.url))
            self._networkReply = self._networkManager.get(request)
            self._networkReply.finished.connect(self._finishDownload)
            self._networkReply.downloadProgress.connect(self._downloadProgress)

    def _finishDownload(self):
        self.image = QtGui.QImage.fromData(self._networkReply.readAll())
        self.downloadComplete.emit()

    def _downloadProgress(self, received, total):
        self.downloadProgress.emit(received, total)



    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, value):
        self._image = value

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        self._size = value

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        self._url = value


class AnAlbum:
    def __init__(self, artist, album, fetch=False):
        self.artist = artist
        self.album = album
        self.arts = []

        if fetch:
            self.fetchMetadata(fetch=fetch)

    def __repr__(self):
        return "<AnAlbum('{artist}', '{album}')>".format(aritst=self.artist, album=self.album)

    def fetchMetadata(self, fetch=False):
        """Fetch the album cover information and populate the local cache."""
        base = "http://ws.audioscrobbler.com/2.0/?method=album.getinfo"
        request = "{base}&api_key={key}&artist={artist}&album={album}&format=json".format(
            base=base,
            key=_KEY,
            artist=urllib.quote(self.artist),
            album=urllib.quote(self.album),
        )
        response = urllib2.urlopen(request).read()
        rawinfo = json.loads(response)
        for data in rawinfo['album']['image']:
            art = Art(data, fetch=fetch)
            self.arts.append(art)



    @property
    def album(self):
        return self._album

    @album.setter
    def album(self, value):
        self._album = value

    @property
    def artist(self):
        return self._artist

    @artist.setter
    def artist(self, value):
        self._artist = value


class TopArtistsFetcher(QtCore.QObject):

    downloadComplete = QtCore.Signal()
    downloadProgress = QtCore.Signal(int, int)

    def __init__(self):
        self._networkManager = QtNetwork.QNetworkAccessManager()
        self._networkReply = None
        self._results = None

    def _finishDownload(self):
        self._results = json.loads(self._networkReply.readAll())
        self.downloadComplete.emit()
                                                                                            
    def _downloadProgress(self, received, total):
        self.downloadProgress.emit(received, total)
 
    def start(self):
        url = "http://ws.audioscrobbler.com/2.0/?method=chart.getTopArtists&api_key={key}&format=json".format(
            key=_KEY,
        )   
        request = QtNetwork.QNetworkRequest()
        request.setUrl(QtCore.QUrl(url))
        self._networkReply = self._networkManager.get(request)
        self._networkReply.finished.connect(self._finishDownload)
        self._networkReply.downloadProgress.connect(self._downloadProgress)
