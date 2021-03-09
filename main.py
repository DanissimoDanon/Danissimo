from ui_func import *

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        ###==VAR==BEGIN==###
        self.user = None
        ###==VAR==END==###

        ###==UI_START==BEGIN==###
        UIFunctions.labelTitle(self, 'STUDY - Дистанционное обучение')
        self.ui.label_credits.setText('Создано в целях обучения для обучения')
        self.ui.label_version.setText('DEBUG')

        startSize = QSize(1000, 720)
        self.resize(startSize)
        self.setMinimumSize(startSize)
        self.ui.stackedWidget.setMinimumWidth(20)

        UIFunctions.selectStandardMenu(self, 'btn_home_page')
        UIFunctions.labelDescription(self, 'Требуется авторизация')
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_login)
        UIFunctions.labelPage(self, 'Вход')

        UIFunctions.uiDefinitions(self)
        DataBase.createDb(self)
        ###==UI_START==END==###

        ###==CONNECT==BEGIN==###
        self.ui.btn_toggle_menu.clicked.connect(lambda: UIFunctions.toggleMenu(self, 220, True))
        self.ui.btn_home_page.clicked.connect(self.buttons)
        self.ui.btn_profile_page.clicked.connect(self.buttons)
        self.ui.btn_addUsers_page.clicked.connect(self.buttons)
        self.ui.btn_login.clicked.connect(self.buttons)
        self.ui.btn_profile_resetPass.clicked.connect(self.profileBut)
        self.ui.btn_profile_exit.clicked.connect(self.profileBut)
        ###==CONNECT==END==###

        ###==HIDE==BEGIN==###
        self.ui.frame_toggle.hide()
        self.ui.frame_left_menu.hide()
        self.ui.btn_addUsers_page.hide()
        ###==HIDE==END==###

        ###==MOVE_FRAME==BEGIN==###
        UIFunctions.removeTitleBar(self, True)

        def moveWindow(event):
            if UIFunctions.returStatus(self) == 1:
                UIFunctions.maximize_restore(self)
            if event.buttons() == Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.dragPos)
                self.dragPos = event.globalPos()
                event.accept()
        self.ui.frame_label_top_btns.mouseMoveEvent = moveWindow
        ###==MOVE_FRAME==END==###
        self.show()

        ###==DEBUG==BEGIN==###
        self.ui.edit_login.setText('admin')
        self.ui.edit_pass.setText('admin')
        self.ui.btn_login.click()
        ###==DEBUG==END==###
        # DataBase.insertUser(self, login, self.ui.edit_pass.text(), fname, lname, clas, group, role)

    def buttons(self):
        btn = self.sender()
        if btn.objectName() == 'btn_login' and (self.ui.edit_login.text() and self.ui.edit_pass.text()):
            cur.execute("SELECT * FROM users WHERE login=? AND pass=?;",
                        (self.ui.edit_login.text(), md5(self.ui.edit_pass.text())))
            self.user = cur.fetchone()
            if self.user is not None:
                self.user = array(self.user)
                self.ui.stackedWidget.setCurrentWidget(self.ui.page_admin)  # ЗАМЕНИТЬ page_admin на page_login
                UIFunctions.labelPage(self, 'Главная')
                UIFunctions.labelDescription(self, 'Добро пожаловать, {} {} - {}'.format(
                    self.user[1], self.user[2], self.user[5]))
                self.ui.edit_profile_name.setText('{} {}'.format(self.user[1], self.user[2]))
                self.ui.edit_profile_role.setText(self.user[5])
                self.ui.frame_toggle.show()
                self.ui.frame_left_menu.show()
                if self.user[5] == ARR_ROLES[0]:
                    self.ui.btn_addUsers_page.show()
                    AdminFunctions.tableCreate(self)
                    AdminFunctions.createButton(self)
            else:
                self.ui.label_login_err.setText('Пользователь не найден или пароль не верный.')
            self.ui.edit_pass.clear()
        elif btn.objectName() == 'btn_login' and not self.ui.edit_login.text():
            self.ui.label_login_err.setText('Введите имя пользователя.')
        elif btn.objectName() == 'btn_login' and not self.ui.edit_pass.text():
            self.ui.label_login_err.setText('Введите пароль.')

        if btn.objectName() == 'btn_addUsers_page':
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_admin)
            UIFunctions.resetStyle(self, 'btn_addUsers')
            UIFunctions.labelPage(self, 'Доб. пользователя')
            btn.setStyleSheet(UIFunctions.selectMenu(self, btn.styleSheet()))

        if btn.objectName() == 'btn_home_page':
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_home)
            UIFunctions.resetStyle(self, 'btn_home_page')
            UIFunctions.labelPage(self, 'Главная')
            btn.setStyleSheet(UIFunctions.selectMenu(self, btn.styleSheet()))

        if btn.objectName() == 'btn_profile_page':
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_profile)
            UIFunctions.resetStyle(self, 'btn_profile_page')
            UIFunctions.labelPage(self, 'Профиль')
            btn.setStyleSheet(UIFunctions.selectMenu(self, btn.styleSheet()))

    def profileBut(self):
        btn = self.sender()
        if btn.objectName() == 'btn_profile_resetPass':
            passw = self.ui.edit_profile_pass.text()
            newPassw = self.ui.edit_profile_newPass.text()
            if md5(passw) == self.user[4] and passw != newPassw and (passw and newPassw):
                cur.execute("UPDATE users SET pass=? WHERE id=?", (md5(newPassw), self.user[0]))
                conn.commit()

        if btn.objectName() == 'btn_profile_exit':
            UIFunctions.labelDescription(self, 'Требуется авторизация')
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_login)
            UIFunctions.labelPage(self, 'Вход')
            self.ui.frame_toggle.hide()
            self.ui.frame_left_menu.hide()
            self.ui.btn_addUsers_page.hide()

    def adminBut(self):
        btn = self.sender()
        if btn.objectName() == 'btn_users_addUser' and self.ui.edit_users_name.text():
            try:
                self.ui.label_users_err.clear()
                fname = self.ui.edit_users_name.text().split(' ')[0]
                lname = self.ui.edit_users_name.text().split(' ')[1]
                login = randGen()
                passw = randGen()
                print(self.ui.combo_users_role.itemText(self.ui.combo_users_role.currentIndex()))
                if self.ui.combo_users_role.currentIndex():
                    pass
                else:
                    self.ui.label_users_err.setText('Имя указано не верно, пример (Иван Иванов).')
                # DataBase.insertUser(self, login, passw, fname, lname,
                #                     self.ui.combo_users_role.itemText(self.ui.combo_users_role.currentIndex()),
                #                     )
            except IndexError:
                self.ui.label_users_err.setText('Имя указано не верно, пример (Иван Иванов).')
        elif btn.objectName() == 'btn_users_addUser' and not self.ui.edit_users_name.text():
            self.ui.label_users_err.setText('Имя не может быть пустым.')

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
