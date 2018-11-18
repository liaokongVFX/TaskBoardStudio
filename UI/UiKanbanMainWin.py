# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\work\kanban\UI\KanbanMainWin.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1150, 500)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.head_frame = QtWidgets.QFrame(Dialog)
        self.head_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.head_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.head_frame.setObjectName("head_frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.head_frame)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.title_label = QtWidgets.QLabel(self.head_frame)
        self.title_label.setObjectName("title_label")
        self.horizontalLayout.addWidget(self.title_label)
        spacerItem = QtWidgets.QSpacerItem(905, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.min_btn = QtWidgets.QPushButton(self.head_frame)
        self.min_btn.setText("")
        self.min_btn.setObjectName("min_btn")
        self.horizontalLayout.addWidget(self.min_btn)
        self.max_btn = QtWidgets.QPushButton(self.head_frame)
        self.max_btn.setText("")
        self.max_btn.setObjectName("max_btn")
        self.horizontalLayout.addWidget(self.max_btn)
        self.close_btn = QtWidgets.QPushButton(self.head_frame)
        self.close_btn.setText("")
        self.close_btn.setObjectName("close_btn")
        self.horizontalLayout.addWidget(self.close_btn)
        self.verticalLayout.addWidget(self.head_frame)
        self.scrollArea = QtWidgets.QScrollArea(Dialog)
        self.scrollArea.setAutoFillBackground(True)
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 1130, 437))
        self.scrollAreaWidgetContents.setStyleSheet("")
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.main_layout = QtWidgets.QHBoxLayout(self.scrollAreaWidgetContents)
        self.main_layout.setContentsMargins(8, 18, 8, 8)
        self.main_layout.setSpacing(15)
        self.main_layout.setObjectName("main_layout")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.title_label.setText(_translate("Dialog", "Tasks Board Studio"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

