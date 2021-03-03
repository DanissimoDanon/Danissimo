###==IMPORTS==BEGIN==###
import os
import subprocess
import sys
import zipfile
from datetime import datetime
from random import choice, randrange
from string import ascii_letters, ascii_lowercase, digits, punctuation, ascii_uppercase
from mss import mss
from time import time, sleep
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect,
                          QSize, QTime, QUrl, Qt, QEvent, QThread, QSettings)
from PyQt5.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon, QKeySequence,
                         QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)
from PyQt5.QtWidgets import *
from ui_main import Ui_MainWindow
###==IMPORTS==END==###

###==GLOBAL_VAR==BEGIN==###
PATH_TO_FILE = os.path.basename(sys.argv[0])
QSettings.setDefaultFormat(QSettings.NativeFormat)
settings = QSettings('STUDY', 'settings')
###==GLOBAL_VAR==END==###
