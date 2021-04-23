import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication, QRubberBand
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot, QTimer, QRect, QPoint, QSize, Qt
from PyQt5.QtGui import *
import pyperclip
from voskMicroTest import Recognizer

# TODO add screenshot text recognition
# TODO add better class for representation of recognizer
# TODO add changing of recognizer language
# TODO add launching programs by voice
# TODO add menu with the ui for lang changing
# TODO fix all this bad code
# TODO add space repetition?
# TODO add MindmapReading Support?


class App(QMainWindow):

    def __init__(self):
        super(App, self).__init__()
        self.sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        self.sizePolicy.setHorizontalStretch(0)
        self.sizePolicy.setVerticalStretch(0)
        self.setWindowFlags(
            QtCore.Qt.Dialog | QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowShadeButtonHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground,
                          QtCore.Qt.WA_ShowWithoutActivating)
        self.initUI()
        QtCore.QLocale.setDefault(QtCore.QLocale(
            QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.rubberBand = QRubberBand(QRubberBand.Rectangle, self)
        self.origin = QPoint()

    def initUI(self):
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.outputLabel = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.outputLabel.setFont(font)
        self.outputLabel.setWordWrap(True)
        self.outputLabel.setObjectName("outputLabel")
        self.outputLabel.setText("test text")
        self.setCentralWidget(self.centralwidget)
        # Set timer for updating dialog position near the cursor
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.updatePos)
        timer.start(100)
        self.shortcut_close = QtWidgets.QShortcut(
            QtGui.QKeySequence('Ctrl+K'), self)
        self.shortcut_close.activated.connect(lambda: app.quit())
        self.shortcut_rec = QtWidgets.QShortcut(
            QtGui.QKeySequence('Ctrl+R'), self)
        self.shortcut_rec.activated.connect(lambda: self.runRecognizer())


    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPos)

        self.move(self.x() + delta.x(),
                  self.y() + delta.y())
        self.oldPos = event.globalPos()

    def updatePos(self):
        self.outputLabel.adjustSize()
        self.adjustSize()

    def runRecognizer(self):
        self.threads = []
        self.recognizer = RecognizerThread()
        self.recognizer.trigger.connect(self.updateLabel)
        self.threads.append(self.recognizer)
        self.recognizer.start()

    @ QtCore.pyqtSlot(str)
    def updateLabel(self, string):
        if(string):
            pyperclip.copy(string)
            self.outputLabel.setText(string)


class RecognizerThread(QThread):

    trigger = pyqtSignal(str)
    running = True

    def __init__(self):
        QtCore.QThread.__init__(self)
        global win
        # vosk-model-ru-0.10 vosk-model-en-us-daanzu-20200328
        self.recognizer = Recognizer("vosk-model-ru-0.10")
        print("thread init done")
        self.recognizing = False
        

    @ QtCore.pyqtSlot()
    def run(self):
        print("starting run")
        self.recognizer.setupModel()
        while self.running:
            self.recognizer.runTimedRecognition()
            self.trigger.emit(self.recognizer.answer)
        self.recognizer.stopPyaudio()



class SystemTrayIcon(QtWidgets.QSystemTrayIcon):

    def __init__(self, icon, parent=None):
        QtWidgets.QSystemTrayIcon.__init__(self, icon, parent)
        menu = QtWidgets.QMenu(parent)
        exitAction = menu.addAction("Exit")
        exitAction.triggered.connect(lambda: app.quit())
        self.setContextMenu(menu)


if __name__ == "__main__":

    app = QApplication(sys.argv)
    win = App()
    trayIcon = SystemTrayIcon(QtGui.QIcon("logo.xpm"), win)
    trayIcon.show()
    win.show()
    sys.exit(app.exec())
