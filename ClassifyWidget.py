# -*- coding:utf-8 -*-
__author__ = "liaokong"
__time__ = "2018/10/25 14:03"

from functools import partial

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from UI.UiClassifyWidget import Ui_classify_widget

from Utils import *
from Config import *
from Message import ask_message

from AddTaskWin import AddTaskWin


class ClassifyWidget(QWidget, Ui_classify_widget):
    def __init__(self, classify_name, parent=None):
        super(ClassifyWidget, self).__init__(parent)
        self.setupUi(self)

        self.setMinimumWidth(250)

        self.setStyleSheet(get_style(self.__class__.__name__))

        self.classify_name = classify_name

        self.classify_name_label.setText(self.classify_name)
        self.init_menu_bar()
        self.init_tasks_list()

        self.add_task_btn.clicked.connect(self.add_task_btn_clicked)

    def init_menu_bar(self):
        menu_bar = QMenuBar()
        menu_bar.setMaximumWidth(30)
        menu_bar.setMaximumHeight(22)

        pop_menu = QMenu(menu_bar)
        add_task_menu_item = pop_menu.addAction("添加任务")
        add_task_menu_item.triggered.connect(self.add_task_btn_clicked)

        move_menu = QMenu(pop_menu)
        move_menu.setTitle("移动到")
        for name in eval(read_ini("Classify", "classify_list")):
            if name != self.classify_name:
                move_task_menu_item = move_menu.addAction(name)
                move_task_menu_item.triggered.connect(
                    partial(self.move_task_menu_item_triggered, self.classify_name, name))

        pop_menu.addAction(move_menu.menuAction())

        remove_classify_menu_item = pop_menu.addAction("删除当前分类")
        remove_classify_menu_item.triggered.connect(self.remove_classify_menu_item_triggered)

        pop_menu.setTitle(" ")
        menu_bar.addAction(pop_menu.menuAction())

        self.more_layout.addWidget(menu_bar)

    def init_tasks_list(self):
        if self.tasks_name_list_layout.count():
            for i in reversed(range(self.tasks_name_list_layout.count())):
                self.tasks_name_list_layout.takeAt(i).widget().setParent(None)

        task_data_list = db_command("SELECT * FROM TasksData WHERE Classify = '%s'" % self.classify_name)
        if task_data_list:
            for data in task_data_list:
                self.tasks_name_list_layout.addWidget(TaskItem(data[1], data[2], data[3], data[4], data[5], data[6]))

    def add_task_btn_clicked(self):
        atw = AddTaskWin(self.classify_name_label.text())
        atw.exec_()

        if atw.changed:
            self.init_tasks_list()

    def remove_classify_menu_item_triggered(self):
        ask = ask_message("是否要删除当前分类: %s \n(当前分类下的任务也将会被删除)" % self.classify_name)
        if ask:
            if db_command("SELECT * FROM TasksData WHERE Classify = '%s'" % self.classify_name):
                db_command(
                    "DELETE FROM TasksData WHERE Classify = '%s'" % self.classify_name)

            classify_list = eval(read_ini("Classify", "classify_list"))
            classify_list.remove(self.classify_name)
            fix_ini("Classify", "classify_list", classify_list)

            self.close()

    def move_task_menu_item_triggered(self, org_classify, to_classify):
        classify_list = eval(read_ini("Classify", "classify_list"))

        org_index = classify_list.index(to_classify)
        classify_list.remove(org_classify)
        classify_list.insert(org_index, org_classify)

        fix_ini("Classify", "classify_list", classify_list)

        self.parent().parent().parent().parent().refresh_classify()


class TaskItem(QWidget):
    def __init__(self, classify, title, describe, tags, remind, finish, parent=None):
        super(TaskItem, self).__init__(parent)

        self.setWindowOpacity(0.99)  # 设置窗口透明度
        self.setAttribute(Qt.WA_TranslucentBackground)  # 设置窗口背景透明
        self.setWindowFlags(Qt.FramelessWindowHint)

        self.setStyleSheet(get_style(self.__class__.__name__))

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 1, 5, 6)

        self.frame = QFrame()
        self.frame_layout = QVBoxLayout()
        self.frame_layout.setSpacing(0)
        self.frame_layout.setContentsMargins(15, 10, 0, 10)
        self.frame.setLayout(self.frame_layout)
        self.frame.setAcceptDrops(True)

        # 上部分
        self.up_h_layout = QHBoxLayout()
        self.up_h_layout.setSpacing(3)
        self.up_h_layout.setContentsMargins(0, 0, 0, 0)
        tag_json_list = read_json(tags_config_path)

        if tags:
            for tag in tags.split(";"):
                tag_color = [(x.get("color")) for x in tag_json_list if x.get("tag_name") == tag]
                if tag_color:
                    label = QLabel()
                    label.setMaximumHeight(5)
                    label.setMinimumWidth(18)

                    label.setStyleSheet(
                        "QLabel{background-color: %s;""border-radius: 2px;}" % tag_color[0])

                    label.setToolTip("<span style='color:#222;'>%s</span>" % tag)

                    self.up_h_layout.addWidget(label)

        spacer_item_label = QSpacerItem(40, 1, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.up_h_layout.addItem(spacer_item_label)

        # 下部分
        self.down_h_layout = QHBoxLayout()
        self.down_h_layout.setContentsMargins(0, 0, 0, 0)

        self.finish_check = QCheckBox(title)
        if int(finish):
            self.finish_check.setStyleSheet("QCheckBox{color:#aaa;font-weight: 400;text-decoration: line-through;}")
            self.finish_check.setCheckState(Qt.Checked)
        else:
            self.finish_check.setStyleSheet("QCheckBox{color:#333;font-weight: 600;}")
            self.finish_check.setCheckState(Qt.Unchecked)

        if describe:
            self.finish_check.setToolTip("<span style='color:#222;font-size:14px;'>%s</span>" % describe)
        self.finish_check.stateChanged.connect(partial(self.finish_check_state_changed, classify, title))
        spacer_item = QSpacerItem(50, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.menu_bar = QMenuBar()
        self.menu_bar.setMaximumWidth(30)
        self.menu_bar.setMaximumHeight(22)
        pop_menu = QMenu(self.menu_bar)
        edit_menu_item = pop_menu.addAction("编辑")
        edit_menu_item.triggered.connect(
            partial(self.edit_menu_item_triggered, classify, title, describe, tags, remind, finish))

        move_menu = QMenu(pop_menu)
        move_menu.setTitle("移动到")
        for name in eval(read_ini("Classify", "classify_list")):
            if name != classify:
                move_menu_item = move_menu.addAction(name)
                move_menu_item.triggered.connect(
                    partial(self.move_menu_item_triggered, classify, title, name))

        pop_menu.addAction(move_menu.menuAction())

        del_menu_item = pop_menu.addAction("删除")
        del_menu_item.triggered.connect(partial(self.del_menu_item_triggered, classify, title, describe, tags, remind))
        pop_menu.setTitle(" ")
        self.menu_bar.addAction(pop_menu.menuAction())

        self.down_h_layout.addWidget(self.finish_check)
        self.down_h_layout.addItem(spacer_item)
        self.down_h_layout.addWidget(self.menu_bar)

        self.frame_layout.addLayout(self.up_h_layout)
        self.frame_layout.addLayout(self.down_h_layout)

        self.main_layout.addWidget(self.frame)

        effect = QGraphicsDropShadowEffect(self.frame)
        effect.setOffset(3, 2)
        effect.setBlurRadius(10)
        effect.setColor(QColor(0, 0, 0, 52))
        self.frame.setGraphicsEffect(effect)

    def move_menu_item_triggered(self, classify, title, to_classify):
        data = db_command("SELECT * FROM TasksData WHERE Classify = '%s' AND Title = '%s'" % (classify, title))[0]

        if ask_message("是否要将当前任务:  %s \n移动到:  %s 分类下" % (title, to_classify)):
            db_command(
                "DELETE FROM TasksData WHERE Classify = '%s' AND Title = '%s'" % (classify, title))
            self.close()

            if not db_command("SELECT * FROM TasksData WHERE Classify = '%s' AND Title = '%s'" % (to_classify, title)):
                db_command(
                    "INSERT INTO TasksData (Classify,Title,Describe,Tags,Remind,Finish) VALUES ('%s','%s','%s','%s','%s','%s')" % (
                        to_classify, title, data[3], data[4], data[5], data[6]))

            else:
                db_command(
                    "UPDATE TasksData SET Describe = '%s',Tags = '%s',Remind = '%s',Finish = '%s' WHERE Classify = '%s' AND Title = '%s'" % (
                        data[3], data[4], data[5], data[6], to_classify, title))

            for classify_widget in self.parent().parent().parent().children():
                if isinstance(classify_widget, ClassifyWidget):
                    if classify_widget.classify_name == to_classify:
                        classify_widget.init_tasks_list()
                        break

    def edit_menu_item_triggered(self, classify, title, describe, tags, remind, finish):
        atw = AddTaskWin(classify, title, describe, tags, remind, finish)
        atw.exec_()

        self.parent().parent().init_tasks_list()

    def del_menu_item_triggered(self, classify, title, describe, tags, remind):
        if ask_message("是否要删除当前任务:  %s" % title):
            db_command(
                "DELETE FROM TasksData WHERE Classify = '%s' AND Title = '%s' AND Describe = '%s' AND Tags = '%s' AND Remind = '%s'" % (
                    classify, title, describe, tags, remind))
            self.close()

    def finish_check_state_changed(self, classify, title):
        if self.finish_check.isChecked():
            self.finish_check.setStyleSheet("QCheckBox{color:#aaa;font-weight: 400;text-decoration: line-through;}")
            db_command(
                "UPDATE TasksData SET Finish = '%s' WHERE Classify = '%s' AND Title = '%s'" % ("1", classify, title))
        else:
            self.finish_check.setStyleSheet("QCheckBox{color:#333;font-weight: 600;}")
            db_command(
                "UPDATE TasksData SET Finish = '%s' WHERE Classify = '%s' AND Title = '%s'" % ("0", classify, title))


if __name__ == '__main__':
    app = QApplication([])

    cw = ClassifyWidget("进行中")
    cw.show()
    #
    # t = TaskItem()
    # t.show()

    app.exec_()
