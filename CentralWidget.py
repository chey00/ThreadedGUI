from time import sleep

from PyQt6.QtCore import QTime, QThread, pyqtSlot
from PyQt6.QtWidgets import QWidget, QGridLayout, QPushButton, QLineEdit, QTextEdit, QTextBrowser, QProgressBar

from ThreadedDatabase import ThreadedDatabase


class CentralWidget(QWidget):
    def __init__(self, parent=None):
        super(CentralWidget, self).__init__(parent)

        layout = QGridLayout()

        self.__button_connect = QPushButton("Connect", self)
        self.__button_connect.released.connect(self.__connect)

        self.__button_disconnect = QPushButton("Disconnect", self)
        self.__button_disconnect.released.connect(self.__disconnect)

        self.__lineedit_username = QLineEdit(self)
        self.__lineedit_username.setPlaceholderText("Benutzername")

        self.__lineedit_password = QLineEdit(self)
        self.__lineedit_password.setPlaceholderText("Passwort")
        self.__lineedit_password.setEchoMode(QLineEdit.EchoMode.Password)

        self.__lineedit_ip = QLineEdit(self)
        self.__lineedit_ip.setPlaceholderText("IP")
        self.__lineedit_ip.setInputMask("009.009.009.009")

        self.__lineedit_port = QLineEdit(self)
        self.__lineedit_port.setPlaceholderText("Port")
        self.__lineedit_port.setInputMask("00009")

        self.__textedit = QTextEdit(self)

        self.__textbrowser = QTextBrowser(self)

        self.__progressbar = QProgressBar(self)
        self.__progressbar.setRange(0, 100)

        layout.addWidget(self.__button_connect, 0, 0)
        layout.addWidget(self.__button_disconnect, 0, 1)
        layout.addWidget(self.__lineedit_username, 1, 0)
        layout.addWidget(self.__lineedit_password, 1, 1)
        layout.addWidget(self.__lineedit_ip, 2, 0)
        layout.addWidget(self.__lineedit_port, 2, 1)
        layout.addWidget(self.__textedit, 3, 0, 1, 2)
        layout.addWidget(self.__textbrowser, 4, 0, 1, 2)
        layout.addWidget(self.__progressbar, 5, 0, 1, 2)

        self.setLayout(layout)

        self.__is_connected = False
        self.__toggle__()

    def __toggle__(self):
        if self.__is_connected:
            self.__button_disconnect.setEnabled(True)
            self.__textedit.setEnabled(True)

            self.__button_connect.setEnabled(False)
            self.__lineedit_ip.setEnabled(False)
            self.__lineedit_port.setEnabled(False)
            self.__lineedit_username.setEnabled(False)
            self.__lineedit_password.setEnabled(False)
        else:
            self.__button_disconnect.setEnabled(False)
            self.__textedit.setEnabled(False)

            self.__button_connect.setEnabled(True)
            self.__lineedit_ip.setEnabled(True)
            self.__lineedit_port.setEnabled(True)
            self.__lineedit_username.setEnabled(True)
            self.__lineedit_password.setEnabled(True)

    @pyqtSlot(int)
    def set_value_progressbar(self, value):
        self.__progressbar.setValue(value)

    def __connect(self):
        self.__is_connected = True
        self.__toggle__()
        self.__button_disconnect.setEnabled(False)

        self.__textbrowser.setText("Verbindung zur Datenbank wird aufgebaut.")

        self.__thread = QThread(self)
        self.__thread.finished.connect(self.__thread.deleteLater)

        self.__database = ThreadedDatabase()
        self.__database.finished.connect(self.__database.deleteLater)
        self.__database.finished.connect(self.__thread.quit)
        self.__database.moveToThread(self.__thread)

        self.__database.finished.connect(self.connected)
        self.__database.progress.connect(self.set_value_progressbar)

        self.__thread.started.connect(self.__database.connectToDatebase)
        self.__thread.start()

    @pyqtSlot()
    def connected(self):
        self.__textbrowser.setText("Verbindung zur Datenbank erfolgreich aufgebaut.")

        self.__button_disconnect.setEnabled(True)

    def __disconnect(self):
        self.__is_connected = False
        self.__toggle__()
        self.__button_connect.setEnabled(False)

        self.__textbrowser.setText("Verbindung zur Datenbank wird abgebaut.")

        self.__thread = QThread(self)
        self.__thread.finished.connect(self.__thread.deleteLater)

        self.__database = ThreadedDatabase()
        self.__database.finished.connect(self.__database.deleteLater)
        self.__database.finished.connect(self.__thread.quit)
        self.__database.moveToThread(self.__thread)

        self.__database.finished.connect(self.disconnected)
        self.__database.progress.connect(self.set_value_progressbar)

        self.__thread.started.connect(self.__database.disconnectFromDatebase)
        self.__thread.start()

    @pyqtSlot()
    def disconnected(self):
        self.__textbrowser.setText("Verbindung zur Datenbank erfolgreich abgebaut.")

        self.__button_connect.setEnabled(True)
