from time import sleep

from PyQt6.QtCore import QObject, pyqtSignal


class ThreadedDatabase(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)

    def connectToDatebase(self):
        for i in range(101):
            self.progress.emit(i)

            sleep(0.05)

        self.finished.emit()

    def disconnectFromDatebase(self):
        for i in range(101):
            self.progress.emit(i)

            sleep(0.02)

        self.finished.emit()
