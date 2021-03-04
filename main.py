from ui_func import *

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        UIFunctions.removeTitleBar(True)
        UIFunctions.labelTitle(self, 'STUDY - Дистанционное обучение')
        UIFunctions.labelDescription(self, 'NONE')
        startSize = QSize(1000, 720)
        self.resize(startSize)
        self.setMinimumSize(startSize)
        self.ui.btn_toggle_menu.clicked.connect(lambda: UIFunctions.toggleMenu(self, 220, True))
        self.ui.btn_login.clicked.connect(self.Button)

        self.ui.stackedWidget.setMinimumWidth(20)
        UIFunctions.addNewMenu(self, 'Главная', 'btn_home', 'url(:/16x16/icons/16x16/cil-home.png)', True)
        UIFunctions.addNewMenu(self, 'Редактировать профиль', 'btn_profile',
                               'url(:/16x16/icons/16x16/cil-equalizer.png)', False)

        UIFunctions.selectStandardMenu(self, 'btn_home')
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_login)
        self.ui.frame_toggle.hide()
        self.ui.frame_left_menu.hide()

        def moveWindow(event):
            if UIFunctions.returStatus() == 1:
                UIFunctions.maximize_restore(self)
            if event.buttons() == Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.dragPos)
                self.dragPos = event.globalPos()
                event.accept()
        self.ui.frame_label_top_btns.mouseMoveEvent = moveWindow

        UIFunctions.uiDefinitions(self)
        self.show()

    def Button(self):
        btn = self.sender()
        if btn.objectName() == 'btn_home':
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_home)
            UIFunctions.resetStyle(self, 'btn_home')
            UIFunctions.labelPage(self, 'Home')
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        if btn.objectName() == 'btn_login' and (self.ui.edit_login.text() and self.ui.edit_pass.text()):
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_home)
            self.ui.frame_toggle.show()
            self.ui.frame_left_menu.show()

        if btn.objectName() == 'btn_profile':
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_profile)
            UIFunctions.resetStyle(self, 'btn_profile')
            UIFunctions.labelPage(self, 'Custom Widgets')
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
