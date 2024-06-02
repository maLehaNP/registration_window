import sys
import json
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QMessageBox
from ui_auth import Ui_Form as Auth_Ui_Form
from ui_reg import Ui_Form as Reg_Ui_Form
from ui_main import Ui_MainWindow

# alph_eng = [chr(i) for i in range(97, 123)] + [chr(i) for i in range(65, 91)]
alph_eng = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
            'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
            'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
# lower = [0, 25], upper = [26, 51]
sp = {'!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/'}


class Auth(QWidget, Auth_Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init_ui()

    def init_ui(self):
        self.setLayout(self.verticalLayout)

        self.sign_btn.clicked.connect(self.buttons)
        self.reg_btn.clicked.connect(self.buttons)

    def buttons(self):
        if self.sender() == self.sign_btn:
            with open('db.json') as db:
                data = json.load(db)
                if self.login.text() in data.keys():
                    if self.password.text() == data[self.login.text()]["password"]:
                        self.main = MainWindow(self.login.text())
                        self.main.show()
                        self.close()
                    else:
                        QMessageBox.warning(self, "Сообщение об ошибке", "Неверный логин или пароль.")
                else:
                    QMessageBox.warning(self, "Сообщение об ошибке", "Неверный логин или пароль.")
        if self.sender() == self.reg_btn:
            self.reg = Reg()
            self.reg.show()
            self.close()


class Reg(QWidget, Reg_Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init_ui()

        self.reg_is_complete = 0
        self.req_stat = [0, 0, 0, 0, 0]
        with open('db.json') as db:
            self.data = json.load(db)

    def init_ui(self):
        self.setLayout(self.verticalLayout)
        # self.password.setEchoMode(QLineEdit.EchoMode.Password)

        self.login.textChanged.connect(self.check_text)
        self.password.textChanged.connect(self.check_text)
        self.pass_rep.textChanged.connect(self.check_text)
        self.email.textChanged.connect(self.check_text)
        self.phone.textChanged.connect(self.check_text)
        self.reg_btn.clicked.connect(self.regist)
        self.cancel.clicked.connect(self.close)

    def check_text(self):
        # Логин
        if self.sender() == self.login:
            # Логин должен состоять не менее чем из 5 символов из набора латинских букв и цифр
            login = self.login.text()
            log_err = []
            if len(login) < 5:
                log_err.append('- Нужно не менее 5 символов')
            if not all((ch.isdigit() or ch in alph_eng) for ch in login):
                log_err.append('- Только латинские буквы и цифры')
            if len(log_err) == 0:
                self.req_stat[0] = 1
                self.login_lbl.setText('Правильный логин')
                self.login_lbl.setStyleSheet("color: rgb(0, 255, 0)")
            else:
                self.req_stat[0] = 0
                self.login_lbl.setText('\n'.join(log_err))
                self.login_lbl.setStyleSheet("color: rgb(255, 0, 0)")

        # Пароль
        if self.sender() == self.password:
            # Пароль должен состоять не менее чем из 8 символов, содержать как минимум одну строчную
            # и одну прописную букву, хотя бы одну цифру и хотя бы один специальный символ
            password = self.password.text()
            pass_err = []
            if len(password) < 8:
                pass_err.append('- Нужно не менее 8 символов')
            if not any(ch in alph_eng[:26] for ch in password):
                pass_err.append('- Нужна одна строчная буква')
            if not any(ch in alph_eng[26:] for ch in password):
                pass_err.append('- Нужна одна прописная буква')
            if not any(ch.isdigit for ch in password):
                pass_err.append('- Нужна одна цифра')
            if not any(ch in sp for ch in password):
                pass_err.append('- Нужен один специальный символ')
            if len(pass_err) == 0:
                self.req_stat[1] = 1
                self.pass_lbl.setText('Правильный пароль')
                self.pass_lbl.setStyleSheet("color: rgb(0, 255, 0)")
            else:
                self.req_stat[1] = 0
                self.pass_lbl.setText('\n'.join(pass_err))
                self.pass_lbl.setStyleSheet("color: rgb(255, 0, 0)")

        # Повтор пароля
        if self.sender() == self.pass_rep:
            rep = self.pass_rep.text()
            if self.password.text() != '' and rep == self.password.text():
                self.req_stat[2] = 1
                self.pass_rep_lbl.setText('Пароль принят')
                self.pass_rep_lbl.setStyleSheet("color: rgb(0, 255, 0)")
            else:
                self.req_stat[2] = 0
                self.pass_rep_lbl.setText('Пароли не совпадают')
                self.pass_rep_lbl.setStyleSheet("color: rgb(255, 0, 0)")

        # Почта
        if self.sender() == self.email:
            email = self.email.text()
            if email.count('@') == 1 and not (email.startswith('@') or email.endswith('@')):
                self.req_stat[3] = 1
                self.email_lbl.setText('Верная почта')
                self.email_lbl.setStyleSheet("color: rgb(0, 255, 0)")
            else:
                self.req_stat[3] = 0
                self.email_lbl.setText('Неверная почта')
                self.email_lbl.setStyleSheet("color: rgb(255, 0, 0)")

        # Телефон
        if self.sender() == self.phone:
            # Телефон вводится в следующем формате: сначала идёт +7 или 8, а затем 10 цифр
            # с любым количеством пробелов между ними и без каких-либо иных символов
            phone = self.phone.text()

            ph_digs = [dig for dig in phone.removeprefix('8').removeprefix('+7').replace(' ', '')]
            if (phone.startswith('+7') or phone.startswith('8')) and len(ph_digs) == 10 and all(
                    dig.isdigit() for dig in ph_digs):
                self.req_stat[4] = 1
                self.phone_lbl.setText('Номер принят')
                self.phone_lbl.setStyleSheet("color: rgb(0, 255, 0)")
            else:
                self.req_stat[4] = 0
                self.phone_lbl.setText('Неправильно введенный номер')
                self.phone_lbl.setStyleSheet("color: rgb(255, 0, 0)")

    def regist(self):
        # if (self.login_lbl.text() == 'Правильный логин') and (self.pass_lbl.text == 'Правильный пароль') and (
        #         self.pass_rep_lbl.text() == 'Пароль принят') and (self.email_lbl.text() == 'Верная почта') and (
        #         self.phone_lbl.text() == 'Номер принят'):
        if self.req_stat == [1, 1, 1, 1, 1]:
            self.data[self.login.text()] = {
                'password': self.password.text(),
                'email': self.email.text(),
                'phone': self.phone.text(),
                'name': self.name.text(),
                'city': self.city.text(),
                'about': self.about.toPlainText()
            }
            with open('db.json', 'w') as db:
                json.dump(self.data, db)
            self.reg_is_complete = 1
            self.main = MainWindow(self.login.text())
            self.main.show()
            self.close()
        else:
            self.password.clear()
            self.pass_rep.clear()

    # действие при закрытии
    def closeEvent(self, event):
        if self.reg_is_complete == 1:
            event.accept()
        else:
            answer = QMessageBox.question(self,
                                          'Выход',
                                          'Хотите прервать регистрацию?'
                                          )
            if answer == QMessageBox.StandardButton.Yes:
                event.accept()
            else:
                event.ignore()


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, login: str):
        super().__init__()
        self.setupUi(self)
        self.init_ui(login)

    def init_ui(self, login):
        self.label.setText(f"Здравствуйте, {login}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Auth()
    ex.show()
    sys.exit(app.exec())
