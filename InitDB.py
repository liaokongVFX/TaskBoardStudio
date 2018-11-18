# -*- coding:utf-8 -*-
__author__ = "liaokong"
__time__ = "2018/10/29 16:08"

import sqlite3

from Config import db_path

conn = sqlite3.connect(db_path)
c = conn.cursor()
c.execute('''CREATE TABLE TasksData
       (ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Classify   VARCHAR(20)   NOT NULL,
        Title      VARCHAR(100)  NOT NULL,
        Describe   TEXT          NOT NULL,
        Tags       VARCHAR(255)  NOT NULL,
        Remind     VARCHAR(20)   NOT NULL,
        Finish     VARCHAR(1)    NOT NULL
        )''')
c.close()
conn.commit()
conn.close()


