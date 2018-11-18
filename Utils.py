# -*- coding:utf-8 -*-
__author__ = "liaokong"
__time__ = "2018/10/25 14:24"

import os
import json
import sqlite3
import configparser

from PyQt5.QtCore import *

from Config import db_path, ini_path


def window_opacity(obj):
    obj.setWindowOpacity(0.99)  # 设置窗口透明度
    obj.setAttribute(Qt.WA_TranslucentBackground)  # 设置窗口背景透明
    obj.setWindowFlags(Qt.FramelessWindowHint)


def get_style(class_name):
    style_str = open("%s/CSS/%s.css" % (os.getcwd().replace("\\", "/"), class_name)).read()
    return style_str.replace("%PATH%", os.getcwd().replace("\\", "/"))


def read_json(json_file):
    """
    将json文件转换成list
    :param json_file: json文件路径
    :return: list
    """
    with open(json_file, encoding="utf-8") as json_file:
        json_str = json_file.read()
        json_list = json.loads(json_str)
    return json_list


def write_json(json_list, json_file):
    """
    将list写成json文件
    :param json_list: list
    :param json_file: json路径
    :return: None
    """
    with open(json_file, "w", encoding="utf-8") as json_file:
        json_str = json.dumps(json_list, ensure_ascii=False, indent=2)
        json_file.write(json_str)


def db_command(command):
    """数据库操作函数"""
    conn_db = sqlite3.connect(db_path)
    c = conn_db.cursor()
    c.execute(command)
    data_list = c.fetchall()
    c.close()
    conn_db.commit()
    conn_db.close()

    return data_list


def read_ini(node, name):
    config = configparser.ConfigParser()
    config.read_file(open(ini_path, encoding="utf8"))
    return config.get(node, name)


def fix_ini(node, name, data):
    config = configparser.ConfigParser()
    config.read_file(open(ini_path, encoding="utf8"))
    config.set(node, name, str(data))
    config.write(open(ini_path, "w", encoding="utf8"))


if __name__ == '__main__':
    pass
    # classify_list = eval(read_ini("Classify", "classify_list"))
    # classify_list.append("灵感")
    # fix_ini("Classify", "classify_list", classify_list)
