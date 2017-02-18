import datetime
from verify import VerificationException
from PyQt4 import QtCore
from PyQt4.QtCore import pyqtSlot
from PyQt4.QtCore import *
from PyQt4.QtGui import *

import sys
class GUIUtils(object):
    """
    implementation of applications GUI
    """

    def show_error_as_dialogbox(func):
        """
        refreshs the value before executing the function
        """
        def func_wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except Exception as e:
                self._show_exception_dialog(e)

        return func_wrapper

    def _create_label(self, text, x_pos, y_pos):
        """
        creates a single label in GUI
        :param text: label's text
        :return:
        """
        label = QLabel(self._w)
        label.setText(text)
        label.move(x_pos, y_pos)
        label.show()
        return label

    @show_error_as_dialogbox
    def __init__(self, verification_function):
        """
        initializes application's GUI
        """
        # create our window
        app = QApplication(sys.argv)
        self._w = QWidget()
        self._w.setWindowTitle('Mixnet Proofs Verifier')
        self._w.setFixedSize(300, 300)

        self._create_label("Please select encryption keys file and input file", 30,30)

        self._key_label = self._create_label("", 50, 100)
        self._create_btn("Keys File", 50, 70, lambda: self._select_file(self._key_label))

        self._cipher_label = self._create_label("", 50, 160)
        self._create_btn("Mixnet Result File", 50, 130, lambda: self._select_file(self._cipher_label))

        self._result_label = self._create_label("", 50, 230)
        self._create_btn("Verify",50, 200, lambda: self._verify_proofs(verification_function, self._result_label))

        # Show the window and run the app
        self._w.show()
        app.exec_()

    @pyqtSlot()
    @show_error_as_dialogbox
    def _verify_proofs(self, verification_function, label):
        assert self._cipher_label.text() , "Cipher File was not specified"
        assert self._key_label.text() , "Key File was not specified"
        try:
            verification_function(self._cipher_label.text(), self._key_label.text())
            res_str = "Succes!"
            label.setStyleSheet('color: green')
        except VerificationException, e:
            res_str = e.message
            label.setStyleSheet('color: red')
        label.setText(res_str)
        label.hide()
        label.show()

    @pyqtSlot()
    def _select_file(self, label):
        label.setText(QFileDialog.getOpenFileName(self._w, ""))
        label.hide()
        label.show()

    @staticmethod
    def _show_exception_dialog(e):
        """
        decorator for displaying exceptions as message boxes
        :param e: thrown exception
        """
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("An Exception Occurred, Please try again.")

        msg.setInformativeText(e.message)
        msg.setWindowTitle("Error")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        msg.exec_()


    def _create_btn(self, text, position_x, position_y, callback_function):
        """
        creates a single button
        :param text: button's text
        :param callback_function: callback for clicking the button
        """
        # Create a button in the window
        button = QPushButton(text, self._w)
        button.move(position_x, position_y)

        # connect the signals to the slots
        button.clicked.connect(callback_function)
        return button
