# -*- coding:utf-8 -*-
__author__ = "liaokong"
__time__ = "2018/10/29 14:27"

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from Utils import *


class Message(QDialog):
    def __init__(self, parent=None):
        super(Message, self).__init__(parent)

        self.setStyle(QStyleFactory.create("plastique"))

        window_opacity(self)

        self.main_layout = QVBoxLayout(self)

        self.frame = QFrame()
        self.frame_layout = QHBoxLayout()
        self.frame_layout.setSpacing(25)
        self.frame_layout.setContentsMargins(15, 15, 15, 15)
        self.frame.setLayout(self.frame_layout)

        self.btn = QPushButton("x")
        self.btn.clicked.connect(self.close)

        self.label = QLabel()

        self.frame_layout.addWidget(self.label)
        self.frame_layout.addWidget(self.btn)

        self.main_layout.addWidget(self.frame)

    def info(self, msg):
        self.setStyleSheet("""
                QFrame{
                    color: black;
                    background-color: #7cd1ef;
                    border-radius: 5px;
                }

                QPushButton {
                    border: 0px solid rgba(255, 255, 255, 0);
                    font-size: 18px;
                    font-family: "Microsoft YaHei";
                    color: rgba(255, 255, 255, 255);
                    padding-bottom: 5px;
                }

                QPushButton:pressed {
                    color: #6cbddc;
                }

                QLabel{
                    color: #31708f;
                    font-weight: 700;
                    font-size: 14px;
                    font-family: "Microsoft YaHei";
                }
                """)

        self.label.setText(msg)

    def success(self, msg):
        self.setStyleSheet("""
                QFrame{
                    color: black;
                    background-color: #b9df90;
                    border-radius: 5px;
                }

                QPushButton {
                    border: 0px solid rgba(255, 255, 255, 0);
                    font-size: 17px;
                    font-family: "Microsoft YaHei";
                    color: rgba(255, 255, 255, 255);
                    padding-bottom: 5px;
                }

                QPushButton:pressed {
                    color: #a0c97f;
                }

                QLabel{
                    color: #3c763d;
                    font-weight: 700;
                    font-size: 14px;
                    font-family: "Microsoft YaHei";
                }
                """)

        self.label.setText(msg)

    def warning(self, msg):
        self.setStyleSheet("""
                QFrame{
                    color: black;
                    background-color: #ffdd87;
                    border-radius: 5px;
                }

                QPushButton {
                    border: 0px solid rgba(255, 255, 255, 0);
                    font-size: 18px;
                    font-family: "Microsoft YaHei";
                    color: rgba(255, 255, 255, 255);
                    padding-bottom: 5px;
                }

                QPushButton:pressed {
                    color: #e8c677;
                }

                QLabel{
                    color: #8a6d3b;
                    font-weight: 700;
                    font-size: 14px;
                    font-family: "Microsoft YaHei";
                }
                """)

        self.label.setText(msg)

    def error(self, msg):
        self.setStyleSheet("""
                QFrame{
                    color: black;
                    background-color: #f2838f;
                    border-radius: 5px;
                }

                QPushButton {
                    border: 0px solid rgba(255, 255, 255, 0);
                    font-size: 18px;
                    font-family: "Microsoft YaHei";
                    color: rgba(255, 255, 255, 255);
                    padding-bottom: 5px;
                }

                QPushButton:pressed {
                    color: #c16872;
                }

                QLabel{
                    color: #b44e4f;
                    font-weight: 700;
                    font-size: 14px;
                    font-family: "Microsoft YaHei";
                }
                """)

        self.label.setText(msg)

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


class AskMessage(QDialog):
    status = False

    def __init__(self, title, text, parent=None):
        super(AskMessage, self).__init__(parent)

        self.setStyle(QStyleFactory.create("plastique"))

        window_opacity(self)

        self.setMinimumWidth(275)

        self.setStyleSheet(get_style(self.__class__.__name__))

        main_v_layout = QVBoxLayout(self)
        main_v_layout.setSpacing(0)

        header_frame = QFrame()
        header_frame.setObjectName("header_frame")
        header_h_layout = QHBoxLayout(header_frame)

        header_label = QLabel(title)
        header_label.setObjectName("header_label")
        spacer_item1 = QSpacerItem(50, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        close_btn = QPushButton("x")
        close_btn.setObjectName("close_btn")
        close_btn.clicked.connect(self.close)

        header_h_layout.addWidget(header_label)
        header_h_layout.addItem(spacer_item1)
        header_h_layout.addWidget(close_btn)

        body_frame = QFrame()
        body_frame.setObjectName("body_frame")
        body_v_layout = QVBoxLayout(body_frame)

        text_label = QLabel(text)
        text_label.setObjectName("text_label")

        body_btn_h_layout = QHBoxLayout()
        body_btn_h_layout.setContentsMargins(0, 0, 8, 0)

        spacer_item2 = QSpacerItem(50, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        yes_btn = QPushButton("确定")
        yes_btn.setObjectName("yes_btn")
        yes_btn.clicked.connect(self.yes_btn_clicked)
        no_btn = QPushButton("取消")
        no_btn.setObjectName("no_btn")
        no_btn.clicked.connect(self.close)

        body_btn_h_layout.addItem(spacer_item2)
        body_btn_h_layout.addWidget(yes_btn)
        body_btn_h_layout.addWidget(no_btn)

        body_v_layout.addWidget(text_label)
        body_v_layout.addLayout(body_btn_h_layout)

        main_v_layout.addWidget(header_frame)
        main_v_layout.addWidget(body_frame)

    def yes_btn_clicked(self):
        self.status = True
        self.close()

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


class InputMessage(QDialog):
    input_text = ""

    def __init__(self, title, text, parent=None):
        super(InputMessage, self).__init__(parent)

        self.text = text

        window_opacity(self)

        self.setStyleSheet(get_style(self.__class__.__name__))
        self.setMinimumWidth(250)

        main_v_layout = QVBoxLayout(self)
        main_v_layout.setSpacing(0)

        header_frame = QFrame()
        header_frame.setObjectName("header_frame")
        header_h_layout = QHBoxLayout(header_frame)

        header_label = QLabel(title)
        header_label.setObjectName("header_label")
        spacer_item1 = QSpacerItem(50, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        close_btn = QPushButton("x")
        close_btn.setObjectName("close_btn")
        close_btn.clicked.connect(self.close)

        header_h_layout.addWidget(header_label)
        header_h_layout.addItem(spacer_item1)
        header_h_layout.addWidget(close_btn)

        body_frame = QFrame()
        body_frame.setObjectName("body_frame")
        body_v_layout = QVBoxLayout(body_frame)

        self.input_line_edit = QLineEdit()
        self.input_line_edit.setPlaceholderText(self.text)

        btn_h_layout = QHBoxLayout()

        spacer_item2 = QSpacerItem(50, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        finish_btn = QPushButton("确定")
        finish_btn.setObjectName("finish_btn")
        finish_btn.clicked.connect(self.finish_btn_clicked)

        btn_h_layout.addItem(spacer_item2)
        btn_h_layout.addWidget(finish_btn)

        body_v_layout.addWidget(self.input_line_edit)
        body_v_layout.addLayout(btn_h_layout)

        main_v_layout.addWidget(header_frame)
        main_v_layout.addWidget(body_frame)

    def finish_btn_clicked(self):
        if self.input_line_edit.text():
            self.input_text = self.input_line_edit.text()
            self.close()
        else:
            message(self.text, "error")

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


def message(msg, msg_type="info"):
    """
    msg_type:['success','info','warning','error']
    """
    m = Message()
    if msg_type == "info":
        m.info(msg)
    elif msg_type == "success":
        m.success(msg)
    elif msg_type == "warning":
        m.warning(msg)
    elif msg_type == "error":
        m.error(msg)
    else:
        raise ValueError

    m.exec_()


def ask_message(msg, title="提示"):
    am = AskMessage(title, msg)
    am.exec_()

    return am.status


def input_message(msg, title="提示"):
    im = InputMessage(title, msg)
    im.exec_()

    return im.input_text


if __name__ == '__main__':
    app = QApplication([])

    print(input_message("请设置分类名称"))

    app.exec_()
