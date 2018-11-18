# -*- coding:utf-8 -*-
__author__ = "liaokong"
__time__ = "2018/10/25 17:39"

import time
from functools import partial

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from UI.UiAddTaskWin import Ui_add_task
from EditTagsWin import EditTagsWin

from Utils import *
from Config import *
from Message import message


class AddTaskWin(QDialog, Ui_add_task):
    changed = False

    def __init__(self, classify, title="", describe="", tags="", remind="", finish="0", parent=None):
        super(AddTaskWin, self).__init__(parent)
        self.setupUi(self)

        self.classify_name = classify
        self.finish = finish

        self.tags = tags

        self.init_style()
        self.init_ui_data(title, describe, tags, remind)

        self.close_btn.clicked.connect(self.close)
        self.set_remind_check.stateChanged.connect(self.set_remind_check_state_changed)
        self.calendar_widget.selectionChanged.connect(self.calendar_widget_selection_changed)
        self.date_edit.dateChanged.connect(self.date_edit_date_changed)
        self.add_btn.clicked.connect(self.add_btn_clicked)

    def init_style(self):
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.calendar_widget.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        self.calendar_widget.setHorizontalHeaderFormat(QCalendarWidget.NoHorizontalHeader)
        self.hour_combo.setItemDelegate(QStyledItemDelegate())
        self.minute_combo.setItemDelegate(QStyledItemDelegate())

        self.setStyleSheet(get_style(self.__class__.__name__))

        self.tags_list_widget.setSelectionMode(QAbstractItemView.NoSelection)

        self.tags_list_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tags_list_widget.customContextMenuRequested.connect(self.popup_menu)

    def popup_menu(self):
        menu = QMenu()
        menu.setStyleSheet(get_style("AddTaskWinMenu"))
        edit_tag_menu = menu.addAction(u"编辑标签")
        edit_tag_menu.triggered.connect(partial(self.edit_tag_menu_triggered, self.tags))
        menu.exec_(QCursor.pos())

    def init_ui_data(self, title, describe, tags, remind):
        self.header_label.setText(self.classify_name)

        if title:
            self.task_title_line.setEnabled(False)
            self.add_btn.setText("修改任务")

        self.task_title_line.setText(title)
        self.task_plain.setPlainText(describe)

        tag_data_list = read_json(tags_config_path)
        for tag in tag_data_list:
            item = QListWidgetItem(tag.get("tag_name"))
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Unchecked)
            if tags:
                if tag.get("tag_name") in tags.split(";"):
                    item.setCheckState(Qt.Checked)

            item.setBackground(QColor(tag.get("color")))

            self.tags_list_widget.addItem(item)

        self.hour_combo.addItems([str(x + 1).zfill(2) for x in range(24)])
        self.minute_combo.addItems([str(x).zfill(2) for x in range(60)][::5])

        if remind:
            self.set_remind_check.setCheckState(Qt.Checked)
            day, hour_min = remind.split(" ")
            self.date_edit.setDate(QDate(int(day.split("/")[0]), int(day.split("/")[1]), int(day.split("/")[2])))
            self.date_edit.setEnabled(True)
            self.hour_combo.setCurrentText(hour_min.split(":")[0])
            self.hour_combo.setEnabled(True)
            self.minute_combo.setCurrentText(hour_min.split(":")[1])
            self.minute_combo.setEnabled(True)
            self.calendar_widget.setSelectedDate(self.date_edit.date())
            self.calendar_widget.setEnabled(True)
        else:
            current_day_data = time.localtime(time.time())
            self.date_edit.setDate(QDate(current_day_data[0], current_day_data[1], current_day_data[2]))

    def edit_tag_menu_triggered(self, tags):
        etw = EditTagsWin()
        etw.exec_()

        self.tags_list_widget.clear()
        tag_data_list = read_json(tags_config_path)
        for tag in tag_data_list:
            item = QListWidgetItem(tag.get("tag_name"))
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Unchecked)
            if tags:
                if tag.get("tag_name") in tags.split(";"):
                    item.setCheckState(Qt.Checked)

            item.setBackground(QColor(tag.get("color")))

            self.tags_list_widget.addItem(item)

    def add_btn_clicked(self):
        title = self.task_title_line.text()
        if not title:
            message("请先为这个任务设置标题", "error")
            return

        tags_list_str = ";".join([self.tags_list_widget.item(i).text() for i in range(self.tags_list_widget.count()) if
                                  self.tags_list_widget.item(i).checkState()])

        if self.set_remind_check.isChecked():
            remind_date = "%s %s:%s" % (
                self.date_edit.text(), self.hour_combo.currentText(), self.minute_combo.currentText())
        else:
            remind_date = ""

        if not db_command(
                        "SELECT * FROM TasksData WHERE Classify = '%s' AND Title = '%s'" % (self.classify_name, title)):
            db_command(
                "INSERT INTO TasksData (Classify,Title,Describe,Tags,Remind,Finish) VALUES ('%s','%s','%s','%s','%s','%s')" % (
                    self.classify_name, str(title), str(self.task_plain.toPlainText()), tags_list_str, remind_date,
                    self.finish))

        else:
            db_command(
                "UPDATE TasksData SET Describe = '%s',Tags = '%s',Remind = '%s',Finish = '%s' WHERE Classify = '%s' AND Title = '%s'" % (
                    str(self.task_plain.toPlainText()), tags_list_str, remind_date, self.finish, self.classify_name,
                    str(title)))

        self.changed = True

        if self.task_title_line.isEnabled():
            message("任务: %s  - 添加完成。" % self.task_title_line.text(), "success")
        else:
            message("任务: %s  - 修改完成。" % self.task_title_line.text(), "success")
        self.close()

    def set_remind_check_state_changed(self):
        if self.set_remind_check.isChecked():
            self.date_edit.setEnabled(True)
            self.hour_combo.setEnabled(True)
            self.minute_combo.setEnabled(True)
            self.calendar_widget.setEnabled(True)
        else:
            self.date_edit.setEnabled(False)
            self.hour_combo.setEnabled(False)
            self.minute_combo.setEnabled(False)
            self.calendar_widget.setEnabled(False)

    def calendar_widget_selection_changed(self):
        self.date_edit.setDate(self.calendar_widget.selectedDate())

    def date_edit_date_changed(self):
        self.calendar_widget.setSelectedDate(self.date_edit.date())

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

        atw = AddTaskWin("进行中")
        atw.show()

        app.exec_()
