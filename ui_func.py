import os
import subprocess
import sys
import hashlib
import sqlite3
from random import choice
from string import ascii_letters, digits
from numpy import array, where, append
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect,
                          QSize, QTime, QUrl, Qt, QEvent, QThread, QSettings)
from PyQt5.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon, QKeySequence,
                         QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)
from PyQt5.QtWidgets import *
from ui_main import Ui_MainWindow
from main import *

GLOBAL_STATE = 0
GLOBAL_TITLE_BAR = True
count = 1
conn = sqlite3.connect('study.db')
cur = conn.cursor()
ARR_ROLES = array(['Системный администратор', 'Администратор учебного процесса', 'Преподаватель', 'Студент'])
ARR_ADMIN = array(['admin', 'admin', 'Даниил', 'Смирнов', ARR_ROLES[0]])
ARR_STUDENTS_GROUPS = array([])

class DataBase(object):
    def createDb(self):
        cur.execute("""CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fname TEXT,
        lname TEXT,
        login TEXT,
        pass TEXT,
        roles TEXT,
        groups TEXT,
        discipline TEXT);""")
        conn.commit()
        cur.execute("SELECT roles FROM users WHERE roles='Системный администратор';")
        if cur.fetchone() is None:
            DataBase.insertUser(self, ARR_ADMIN[0], ARR_ADMIN[1], ARR_ADMIN[2], ARR_ADMIN[3], ARR_ADMIN[4])

    def getUsers(self):
        cur.execute("SELECT * FROM users;")
        return cur.fetchall()

    def insertUser(self, login, passw, fname, lname, role, clas='NONE', group='NONE'):
        cur.execute("INSERT INTO users VALUES(?, ?, ?, ?, ?, ?, ?, ?);",
                    (None, fname, lname, login, md5(passw), role, clas, group))
        conn.commit()

class AdminFunctions(MainWindow):
    def tableCreate(self):
        self.ui.tableWidget.clearContents()
        self.ui.tableWidget.setRowCount(0)
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.ui.tableWidget.horizontalHeader().setVisible(True)
        users = array(DataBase.getUsers(self))
        for i in users:
            self.ui.tableWidget.setRowCount(self.ui.tableWidget.rowCount() + 1)
            self.ui.tableWidget.setItem(self.ui.tableWidget.rowCount() - 1, 0, QTableWidgetItem(i[0]))
            self.ui.tableWidget.setItem(self.ui.tableWidget.rowCount() - 1, 1, QTableWidgetItem(i[1]))
            self.ui.tableWidget.setItem(self.ui.tableWidget.rowCount() - 1, 2, QTableWidgetItem(i[2]))
            self.ui.tableWidget.setItem(self.ui.tableWidget.rowCount() - 1, 3, QTableWidgetItem(i[3]))
            self.ui.tableWidget.setItem(self.ui.tableWidget.rowCount() - 1, 4, QTableWidgetItem(i[4]))
            self.ui.tableWidget.setItem(self.ui.tableWidget.rowCount() - 1, 5, QTableWidgetItem(i[5]))
            self.ui.tableWidget.setItem(self.ui.tableWidget.rowCount() - 1, 6, QTableWidgetItem(i[6]))
            self.ui.tableWidget.setItem(self.ui.tableWidget.rowCount() - 1, 7, QTableWidgetItem(i[7]))

    def createButton(self):
        self.ui.combo_users_role.clear()
        self.ui.combo_users_role.addItem('Выбрать')
        self.ui.combo_users_role.addItems(ARR_ROLES)
        self.ui.btn_users_showTable.clicked.connect(self.adminBut)
        self.ui.btn_users_addUser.clicked.connect(self.adminBut)

class OtherFunctions(object):
    pass

class UIFunctions(object):
    GLOBAL_STATE = 0
    GLOBAL_TITLE_BAR = True

    def maximize_restore(self):
        global GLOBAL_STATE
        status = GLOBAL_STATE
        if status == 0:
            self.showMaximized()
            GLOBAL_STATE = 1
            self.ui.horizontalLayout.setContentsMargins(0, 0, 0, 0)
            self.ui.btn_maximize_restore.setToolTip('Restore')
            self.ui.btn_maximize_restore.setIcon(QtGui.QIcon(u':/16x16/icons/16x16/cil-window-restore.png'))
            self.ui.frame_top_btns.setStyleSheet('background-color: rgb(27, 29, 35)')
            self.ui.frame_size_grip.hide()
        else:
            GLOBAL_STATE = 0
            self.showNormal()
            self.resize(self.width()+1, self.height()+1)
            self.ui.horizontalLayout.setContentsMargins(10, 10, 10, 10)
            self.ui.btn_maximize_restore.setToolTip('Maximize')
            self.ui.btn_maximize_restore.setIcon(QtGui.QIcon(u':/16x16/icons/16x16/cil-window-maximize.png'))
            self.ui.frame_top_btns.setStyleSheet('background-color: rgba(27, 29, 35, 200)')
            self.ui.frame_size_grip.show()

    def returStatus(self):
        return GLOBAL_STATE

    def setStatus(self, status):
        global GLOBAL_STATE
        GLOBAL_STATE = status

    def enableMaximumSize(self, width, height):
        if width != '' and height != '':
            self.setMaximumSize(QSize(width, height))
            self.ui.frame_size_grip.hide()
            self.ui.btn_maximize_restore.hide()

    def toggleMenu(self, maxWidth, enable):
        if enable:
            width = self.ui.frame_left_menu.width()
            maxExtend = maxWidth
            standard = 70
            if width == 70:
                widthExtended = maxExtend
            else:
                widthExtended = standard
            self.animation = QPropertyAnimation(self.ui.frame_left_menu, b'minimumWidth')
            self.animation.setDuration(300)
            self.animation.setStartValue(width)
            self.animation.setEndValue(widthExtended)
            self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animation.start()

    def removeTitleBar(self, status):
        global GLOBAL_TITLE_BAR
        GLOBAL_TITLE_BAR = status

    def labelTitle(self, text):
        self.ui.label_title_bar_top.setText(text)

    def labelDescription(self, text):
        self.ui.label_top_info_1.setText(text)

    def selectMenu(self, getStyle):
        select = getStyle + 'QPushButton { border-right: 7px solid rgb(44, 49, 60); }'
        return select

    def deselectMenu(self, getStyle):
        deselect = getStyle.replace('QPushButton { border-right: 7px solid rgb(44, 49, 60); }', '')
        return deselect

    def selectStandardMenu(self, widget):
        for w in self.ui.frame_left_menu.findChildren(QPushButton):
            if w.objectName() == widget:
                w.setStyleSheet(UIFunctions.selectMenu(self, w.styleSheet()))

    def resetStyle(self, widget):
        for w in self.ui.frame_left_menu.findChildren(QPushButton):
            if w.objectName() != widget:
                w.setStyleSheet(UIFunctions.deselectMenu(self, w.styleSheet()))

    def labelPage(self, text):
        newText = '| ' + text.upper()
        self.ui.label_top_info_2.setText(newText)

    def uiDefinitions(self):
        def dobleClickMaximizeRestore(event):
            if event.type() == QtCore.QEvent.MouseButtonDblClick:
                QtCore.QTimer.singleShot(250, lambda: UIFunctions.maximize_restore(self))

        if GLOBAL_TITLE_BAR:
            self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
            self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
            self.ui.frame_label_top_btns.mouseDoubleClickEvent = dobleClickMaximizeRestore
        else:
            self.ui.horizontalLayout.setContentsMargins(0, 0, 0, 0)
            self.ui.frame_label_top_btns.setContentsMargins(8, 0, 0, 5)
            self.ui.frame_label_top_btns.setMinimumHeight(42)
            self.ui.frame_icon_top_bar.hide()
            self.ui.frame_btns_right.hide()
            self.ui.frame_size_grip.hide()

        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(17)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 150))
        self.ui.frame_main.setGraphicsEffect(self.shadow)
        self.sizegrip = QSizeGrip(self.ui.frame_size_grip)
        self.sizegrip.setStyleSheet('width: 20px; height: 20px; margin 0px; padding: 0px;')
        self.ui.btn_minimize.clicked.connect(lambda: self.showMinimized())
        self.ui.btn_maximize_restore.clicked.connect(lambda: UIFunctions.maximize_restore(self))
        self.ui.btn_close.clicked.connect(lambda: self.close())

def md5(text):
    m = hashlib.md5()
    m.update(text.encode('utf-8'))
    return m.hexdigest()

def randGen():
    end = []
    sym = ascii_letters + digits
    for i in range(12):
        end.append(choice(sym))
    end = ''.join(end)
    return end