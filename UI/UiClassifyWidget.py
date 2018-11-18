# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\work\kanban\UI\ClassifyWidget.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_classify_widget(object):
    def setupUi(self, classify_widget):
        classify_widget.setObjectName("classify_widget")
        classify_widget.resize(225, 424)
        classify_widget.setMaximumSize(QtCore.QSize(250, 16777215))
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(classify_widget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frame = QtWidgets.QFrame(classify_widget)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout.setContentsMargins(10, 5, 5, 5)
        self.verticalLayout.setSpacing(8)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.classify_name_label = QtWidgets.QLabel(self.frame)
        self.classify_name_label.setObjectName("classify_name_label")
        self.horizontalLayout.addWidget(self.classify_name_label)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.more_layout = QtWidgets.QHBoxLayout()
        self.more_layout.setSpacing(0)
        self.more_layout.setObjectName("more_layout")
        self.horizontalLayout.addLayout(self.more_layout)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.tasks_name_list_layout = QtWidgets.QVBoxLayout()
        self.tasks_name_list_layout.setSpacing(0)
        self.tasks_name_list_layout.setObjectName("tasks_name_list_layout")
        self.verticalLayout.addLayout(self.tasks_name_list_layout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.add_task_btn = QtWidgets.QPushButton(self.frame)
        self.add_task_btn.setMinimumSize(QtCore.QSize(100, 0))
        self.add_task_btn.setObjectName("add_task_btn")
        self.horizontalLayout_2.addWidget(self.add_task_btn)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.verticalLayout_2.addWidget(self.frame)
        spacerItem2 = QtWidgets.QSpacerItem(143, 335, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem2)

        self.retranslateUi(classify_widget)
        QtCore.QMetaObject.connectSlotsByName(classify_widget)

    def retranslateUi(self, classify_widget):
        _translate = QtCore.QCoreApplication.translate
        classify_widget.setWindowTitle(_translate("classify_widget", "Form"))
        self.classify_name_label.setText(_translate("classify_widget", "TextLabel"))
        self.add_task_btn.setText(_translate("classify_widget", "添加一个任务..."))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    classify_widget = QtWidgets.QWidget()
    ui = Ui_classify_widget()
    ui.setupUi(classify_widget)
    classify_widget.show()
    sys.exit(app.exec_())

