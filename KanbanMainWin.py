# -*- coding:utf-8 -*-
__author__ = "liaokong"
__time__ = "2018/10/25 11:38"

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from UI.UiKanbanMainWin import Ui_Dialog

from ClassifyWidget import ClassifyWidget

from Utils import *
from Message import input_message


class KanbanMainWin(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super(KanbanMainWin, self).__init__(parent)
        self.setupUi(self)

        self.setStyleSheet(get_style(self.__class__.__name__))

        window_opacity(self)

        self.init_classify_list_panel()

        self.close_btn.clicked.connect(self.close)
        self.min_btn.clicked.connect(self.showMinimized)
        self.max_btn.clicked.connect(self.showMaximized)

    def init_classify_list_panel(self):
        self.resize(1680, 850)

        for classify_name in eval(read_ini("Classify", "classify_list")):
            self.main_layout.addWidget(ClassifyWidget(classify_name))

        btn_layout = QVBoxLayout()
        add_classify_btn = QPushButton("添加一个分类列表...")
        add_classify_btn.setObjectName("add_classify_btn")
        add_classify_btn.setMaximumWidth(200)
        add_classify_btn.setMinimumWidth(185)

        add_classify_btn.clicked.connect(self.add_classify_btn_clicked)

        btn_layout.addWidget(add_classify_btn)
        btn_layout.addItem(QSpacerItem(20, 23, QSizePolicy.Minimum, QSizePolicy.Expanding))
        btn_layout.setContentsMargins(5, 5, 5, 5)

        self.main_layout.addLayout(btn_layout)

    def add_classify_btn_clicked(self):
        classify_name = input_message("请设置分类名称")
        if classify_name:
            classify_list = eval(read_ini("Classify", "classify_list"))
            classify_list.append(classify_name)
            fix_ini("Classify", "classify_list", classify_list)

            self.refresh_classify()

    def refresh_classify(self):
        self.clear_classify_list()
        self.init_classify_list_panel()

    def clear_classify_list(self):
        # 清空widget
        classify_list_layout = self.scrollAreaWidgetContents.findChild(QHBoxLayout)

        if classify_list_layout.count():
            for i in reversed(range(classify_list_layout.count())):
                widget_item = classify_list_layout.takeAt(i)

                if isinstance(widget_item, QWidgetItem):
                    widget_item.widget().setParent(None)
                else:
                    for x in reversed(range(widget_item.count())):
                        btn_widget_item = widget_item.takeAt(x)
                        if isinstance(btn_widget_item, QWidgetItem):
                            btn_widget_item.widget().setParent(None)
                        else:
                            widget_item.removeItem(btn_widget_item)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))

    def mouseMoveEvent(self, event):
        if Qt.LeftButton and self.m_flag:
            self.move(event.globalPos() - self.m_Position)
            event.accept()

    def mouseReleaseEvent(self, event):
        self.m_flag = False
        self.setCursor(QCursor(Qt.ArrowCursor))

if __name__ == '__main__':
    app = QApplication([])

    kmw = KanbanMainWin()
    kmw.show()

    app.exec_()
