from ui_func import *

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.user = None
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.ui.tableWidget.horizontalHeader().setVisible(True)
        UIFunctions.removeTitleBar(self, True)
        UIFunctions.labelTitle(self, 'STUDY - Дистанционное обучение')
        self.ui.label_credits.setText('Создано в целях обучения для обучения')
        startSize = QSize(1000, 720)
        self.resize(startSize)
        self.setMinimumSize(startSize)
        self.ui.btn_toggle_menu.clicked.connect(lambda: UIFunctions.toggleMenu(self, 220, True))
        self.ui.btn_login.clicked.connect(self.buttons)
        self.ui.btn_profile_resetPass.clicked.connect(self.profileBut)
        self.ui.btn_profile_exit.clicked.connect(self.profileBut)

        self.ui.stackedWidget.setMinimumWidth(20)
        UIFunctions.addNewMenu(self, 'Главная', 'btn_home', 'url(:/16x16/icons/16x16/cil-home.png)', True)
        UIFunctions.addNewMenu(self, 'Профиль', 'btn_profile', 'url(:/16x16/icons/16x16/cil-user.png)', False)

        UIFunctions.selectStandardMenu(self, 'btn_home')
        UIFunctions.labelDescription(self, 'Требуется авторизация')
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_login)
        UIFunctions.labelPage(self, 'Вход')
        self.ui.frame_toggle.hide()
        self.ui.frame_left_menu.hide()

        def moveWindow(event):
            if UIFunctions.returStatus(self) == 1:
                UIFunctions.maximize_restore(self)
            if event.buttons() == Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.dragPos)
                self.dragPos = event.globalPos()
                event.accept()
        self.ui.frame_label_top_btns.mouseMoveEvent = moveWindow

        UIFunctions.uiDefinitions(self)
        self.firstLaunch = False
        self.ui.edit_login.setText('Даниил Смирнов')
        self.ui.edit_pass.setText('admin')
        DataBase.createDb(self)
        self.show()
        self.ui.btn_login.click()

    def buttons(self):
        btn = self.sender()
        if btn.objectName() == 'btn_login' and (self.ui.edit_login.text() and self.ui.edit_pass.text()):
            try:
                fname = self.ui.edit_login.text().split(' ')[0]
                lname = self.ui.edit_login.text().split(' ')[1]
                if self.firstLaunch:
                    cur.execute("INSERT INTO users VALUES(?, ?, ?, ?, ?, ?, ?);",
                                ('1', fname, lname, md5(self.ui.edit_pass.text()), ARR_ROLES[0], 'None', 'None'))
                    conn.commit()
                cur.execute("SELECT * FROM users WHERE fname=? AND lname=? AND pass=?;",
                            (fname, lname, md5(self.ui.edit_pass.text())))
                self.user = cur.fetchone()
                if self.user is not None:
                    self.user = array(self.user)
                    self.ui.stackedWidget.setCurrentWidget(self.ui.page_admin)  # REPAIR
                    UIFunctions.labelPage(self, 'Главная')
                    UIFunctions.labelDescription(self, 'Добро пожаловать, {} {} - {}'.format(
                        self.user[1], self.user[2], self.user[4]))
                    self.ui.edit_profile_name.setText('{} {}'.format(self.user[1], self.user[2]))
                    self.ui.edit_profile_role.setText(self.user[4])
                    self.ui.frame_toggle.show()
                    self.ui.frame_left_menu.show()
                    if self.user[4] == ARR_ROLES[0]:
                        UIFunctions.addNewMenu(self, 'Админ', 'btn_admin',
                                               'url(:/16x16/icons/16x16/cil-user-follow)', True)
                        AdminFunctions.tableCreate(self)
                        AdminFunctions.createButton(self)
                else:
                    self.ui.label_login_err.setText('Пользователь не найден или пароль не верный.')
                self.ui.edit_pass.clear()
            except IndexError:
                self.ui.label_login_err.setText('Пользователь не найден или пароль не верный.')
        elif btn.objectName() == 'btn_login' and not self.ui.edit_login.text():
            self.ui.label_login_err.setText('Введите имя пользователя.')
        elif btn.objectName() == 'btn_login' and not self.ui.edit_pass.text():
            self.ui.label_login_err.setText('Введите пароль.')

        if btn.objectName() == 'btn_admin':
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_admin)
            UIFunctions.resetStyle(self, 'btn_admin')
            UIFunctions.labelPage(self, 'Админ')
            btn.setStyleSheet(UIFunctions.selectMenu(self, btn.styleSheet()))

        if btn.objectName() == 'btn_home':
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_home)
            UIFunctions.resetStyle(self, 'btn_home')
            UIFunctions.labelPage(self, 'Главная')
            btn.setStyleSheet(UIFunctions.selectMenu(self, btn.styleSheet()))

        if btn.objectName() == 'btn_profile':
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_profile)
            UIFunctions.resetStyle(self, 'btn_profile')
            UIFunctions.labelPage(self, 'Профиль')
            btn.setStyleSheet(UIFunctions.selectMenu(self, btn.styleSheet()))

    def profileBut(self):
        btn = self.sender()
        if btn.objectName() == 'btn_profile_resetPass':
            passw = self.ui.edit_profile_pass.text()
            newPassw = self.ui.edit_profile_newPass.text()
            if md5(passw) == self.user[3] and passw != newPassw and (passw and newPassw):
                cur.execute("UPDATE users SET pass=? WHERE id=?", (md5(newPassw), self.user[0]))
                conn.commit()

        if btn.objectName() == 'btn_profile_exit':
            UIFunctions.labelDescription(self, 'Требуется авторизация')
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_login)
            UIFunctions.labelPage(self, 'Вход')
            self.ui.frame_toggle.hide()
            self.ui.frame_left_menu.hide()

    def adminBut(self):
        btn = self.sender()
        if btn.objectName() == 'btn_users_addUser':
            pass

        if btn.objectName() == 'btn_users_showTable':
            if btn.text() == 'Увеличить таблицу...':
                self.ui.grid_5.hide()
                btn.setText('Уменьшить таблицу...')
            else:
                self.ui.grid_5.show()
                btn.setText('Увеличить таблицу...')

    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
