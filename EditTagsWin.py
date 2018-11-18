# -*- coding:utf-8 -*-
__author__ = "liaokong"
__time__ = "2018/11/2 18:33"

from functools import partial

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from Utils import *
from Config import *
from Message import *


class EditTagsWin(QDialog):
    def __init__(self, parent=None):
        super(EditTagsWin, self).__init__(parent)

        self.setStyleSheet(get_style(self.__class__.__name__))
        window_opacity(self)

        main_v_layout = QVBoxLayout(self)
        main_v_layout.setSpacing(0)

        header_frame = QFrame()
        header_frame.setObjectName("header_frame")
        header_h_layout = QHBoxLayout(header_frame)

        header_label = QLabel("编辑标签")
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

        btn_h_layout = QHBoxLayout()
        btn_h_layout.setSpacing(0)

        spacer_item2 = QSpacerItem(50, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        minus_btn = QPushButton()
        minus_btn.setObjectName("minus_btn")
        minus_btn.clicked.connect(self.minus_btn_clicked)
        add_btn = QPushButton()
        add_btn.setObjectName("add_btn")
        add_btn.clicked.connect(self.add_btn_clicked)

        btn_h_layout.addItem(spacer_item2)
        btn_h_layout.addWidget(minus_btn)
        btn_h_layout.addWidget(add_btn)

        self.tags_list_widget = QListWidget()
        self.tags_list_widget.itemDoubleClicked.connect(self.tags_list_widget_item_double_clicked)

        body_v_layout.addLayout(btn_h_layout)
        body_v_layout.addWidget(self.tags_list_widget)

        main_v_layout.addWidget(header_frame)
        main_v_layout.addWidget(body_frame)

        self.init_tags_list()

    def init_tags_list(self):
        self.tags_list_widget.clear()

        tag_data_list = read_json(tags_config_path)
        for tag in tag_data_list:
            item = QListWidgetItem(tag.get("tag_name"))
            item.setBackground(QColor(tag.get("color")))

            self.tags_list_widget.addItem(item)

    def minus_btn_clicked(self):
        try:
            tag_name = self.tags_list_widget.currentItem().text()
        except:
            message("请先选择要删除的标签","error")
            return

        ask = ask_message("是否要删除标签: %s\n(请先将有该标签的任务取消该标签)" % tag_name)
        if ask:
            tags_data_list = read_json(tags_config_path)
            if tags_data_list:
                tags_data_list.pop(self.tags_list_widget.currentRow())
                write_json(tags_data_list, tags_config_path)

                self.init_tags_list()

    def add_btn_clicked(self):
        tew = TagEditWin()
        tew.exec_()

        self.init_tags_list()

    def tags_list_widget_item_double_clicked(self):
        tew = TagEditWin(self.tags_list_widget.currentItem().text())
        tew.exec_()

        self.init_tags_list()

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


class TagEditWin(QDialog):
    def __init__(self, tag_name="", parent=None):
        super(TagEditWin, self).__init__(parent)

        self.setStyleSheet(get_style("EditTagsWin"))
        window_opacity(self)

        self.tags_list = read_json(tags_config_path)
        if tag_name:
            for tag in self.tags_list:
                if tag.get("tag_name") == tag_name:
                    color_str = tag.get("color")
                    break

        main_v_layout = QVBoxLayout(self)
        main_v_layout.setSpacing(0)

        header_frame = QFrame()
        header_frame.setObjectName("header_frame")
        header_h_layout = QHBoxLayout(header_frame)

        header_label = QLabel("编辑标签")
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
        body_v_layout.setSpacing(15)

        color_h_layout = QHBoxLayout()
        color_h_layout.setSpacing(0)

        if tag_name:
            self.color_name_label = QLabel(color_str)
            self.color_name_label.setStyleSheet(
                'QLabel{background-color: %s;font-size:14px;font-family: "Microsoft YaHei";}' % color_str)
        else:
            self.color_name_label = QLabel("请选择标签颜色")
        self.color_name_label.setObjectName("color_name_label")
        color_sel_btn = QPushButton()
        color_sel_btn.setObjectName("color_sel_btn")
        color_sel_btn.clicked.connect(self.color_sel_btn_clicked)

        color_h_layout.addWidget(self.color_name_label)
        color_h_layout.addWidget(color_sel_btn)

        tag_h_layout = QHBoxLayout()
        tag_h_layout.setSpacing(2)
        tag_h_layout.setContentsMargins(0, 8, 0, 0)

        self.tag_name_line = QLineEdit()
        self.tag_name_line.setPlaceholderText("请设置Tag名称")
        if tag_name:
            self.tag_name_line.setText(tag_name)
            add_tag_btn = QPushButton("修改")
        else:
            add_tag_btn = QPushButton("添加")
        add_tag_btn.setObjectName("add_tag_btn")
        add_tag_btn.clicked.connect(partial(self.add_tag_btn_clicked, tag_name))

        tag_h_layout.addWidget(self.tag_name_line)
        tag_h_layout.addWidget(add_tag_btn)

        body_v_layout.addLayout(tag_h_layout)
        body_v_layout.addLayout(color_h_layout)

        main_v_layout.addWidget(header_frame)
        main_v_layout.addWidget(body_frame)

    def add_tag_btn_clicked(self, tag_name):
        if not self.tag_name_line.text() or "#" not in self.color_name_label.text():
            message("请设置标签名字和颜色", "error")
            return

        color_dict = {"tag_name": str(self.tag_name_line.text()), "color": str(self.color_name_label.text())}
        if tag_name:
            for index, item in enumerate(self.tags_list):
                if item.get("tag_name") == str(self.tag_name_line.text()) or item.get("color") == str(
                        self.color_name_label.text()):
                    self.tags_list.insert(index, color_dict)
                    self.tags_list.pop(index + 1)
                    write_json(self.tags_list, tags_config_path)

                    message("已成功修改标签: %s" % str(self.tag_name_line.text()), "success")
                    self.close()
                    return

        self.tags_list.append(color_dict)
        write_json(self.tags_list, tags_config_path)

        message("已成功添加标签: %s" % str(self.tag_name_line.text()), "success")
        self.close()

    def color_sel_btn_clicked(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.color_name_label.setStyleSheet(
                'QLabel{background-color: %s;font-size:14px;font-family: "Microsoft YaHei";}' % color.name())
            self.color_name_label.setText(color.name())

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

    etw = EditTagsWin()
    etw.exec_()

    # tew = TagEditWin("紧急")
    # tew.show()

    app.exec_()
