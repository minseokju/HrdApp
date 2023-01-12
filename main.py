import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic, QtWidgets, QtCore
import pymysql
from datetime import datetime
from PyQt5.QtCore import *
import threading

main_form = uic.loadUiType("main.ui")[0]
join_form = uic.loadUiType("join.ui")[0]
login_form = uic.loadUiType("login.ui")[0]
student_form = uic.loadUiType("studentP.ui")[0]
teacher_form = uic.loadUiType("teacherP.ui")[0]


# 메인 위젯
class MainWidget(QWidget, main_form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.moveLogin.clicked.connect(self.move_login)
        self.moveJoin.clicked.connect(self.move_join)

    def move_login(self):
        self.parent().setCurrentIndex(2)

    def move_join(self):
        self.parent().setCurrentIndex(1)


# 회원 가입 위젯
class JoinWidget(QWidget, join_form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.conn = pymysql.connect(host='127.0.0.1', user='root', password='486486', db='hrd')
        self.curs = self.conn.cursor()
        self.joinButton.clicked.connect(self.join)
        self.moveMain.clicked.connect(self.main)

    def join(self):
        grade = ''
        if self.studentCheck.isChecked():
            grade = 'student'
        elif self.teacherCheck.isChecked():
            grade = 'teacher'
        if self.nameLine.text() and self.idLine.text() and self.passLine.text():
            if grade:
                self.curs.execute("insert into hrd.user (name, id, password, grade) values ('%s', '%s', '%s', '%s')" %
                                  (self.nameLine.text(), self.idLine.text(), self.passLine.text(), grade))
                self.conn.commit()
                QMessageBox.information(self, '완료', '회원가입을 완료했습니다')
                self.nameLine.clear()
                self.idLine.clear()
                self.passLine.clear()
                self.parent().setCurrentIndex(0)
            else:
                QMessageBox.information(self, '다시 시도', '본인의 신분을 체크해주세요')
        else:
            QMessageBox.information(self, '다시 시도', '이름, 아이디 혹은 비밀번호를 제대로 입력해주세요')

    def main(self):
        self.parent().setCurrentIndex(0)


# 로그인 위젯
class LoginWidget(QWidget, login_form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.conn = pymysql.connect(host='127.0.0.1', user='root', password='486486', db='hrd')
        self.curs = self.conn.cursor()
        self.loginButton.clicked.connect(self.login)
        self.moveJoin.clicked.connect(self.move_join)

    def login(self):
        self.conn = pymysql.connect(host='127.0.0.1', user='root', password='486486', db='hrd')
        self.curs = self.conn.cursor()
        self.curs.execute("select * from hrd.user")
        users = self.curs.fetchall()
        success = False
        grade = ''
        if self.studentCheck.isChecked():
            grade = 'student'
        elif self.teacherCheck.isChecked():
            grade = 'teacher'
        for u in users:
            if self.idLine.text() == u[1] and self.passLine.text() == u[2] and grade == u[3]:
                self.idLine.clear()
                self.passLine.clear()
                QMessageBox.information(self, '로그인 성공', '%s님의 이름으로\n프로그램을 실행합니다.' % u[0])
                success = True
                # grade값에 따라 다른 화면을 불러오자
                if grade == 'student':
                    self.parent().setCurrentIndex(3)
                    student.userName.setText("%s" % u[0])
                    student.userName_2.setText("%s" % u[0])
                    student.studentName.setText("%s" % u[0])
                    student.user = u[0]
                    student2.userName.setText("%s" % u[0])
                    student2.userName_2.setText("%s" % u[0])
                    student2.studentName.setText("%s" % u[0])
                    student2.user = u[0]
                else:
                    self.parent().setCurrentIndex(4)
                    teacher.userName.setText("%s" % u[0])
                    teacher.teacherName.setText("%s" % u[0])
                    teacher2.userName.setText("%s" % u[0])
                    teacher2.teacherName.setText("%s" % u[0])
                    self.curs.execute("select count(checked) from hrd.messages where checked = 1 and sendto = '%s'" %
                                      u[0])
                    alarm_m = self.curs.fetchall()
                    teacher.messageA.setText(str(alarm_m[0][0]))
                    teacher.user = u[0]
                    teacher2.messageA.setText(str(alarm_m[0][0]))
                    teacher2.user = u[0]
        if not success:
            QMessageBox.information(self, '실패', 'ID나 비밀번호 혹은 신분이 잘못되었습니다.')

    def move_join(self):
        self.parent().setCurrentIndex(1)


class StudentWidget(QWidget, student_form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.studentStack.setCurrentIndex(0)
        self.user = ''
        self.conn = pymysql.connect(host='127.0.0.1', user='root', password='486486', db='hrd')
        self.curs = self.conn.cursor()
        self.now = datetime.now()
        self.todayDate.setText(str(self.now.date()))
        self.logoutButton.clicked.connect(self.log_out)
        self.moveMessage.clicked.connect(self.move_message)
        self.moveCalendar.clicked.connect(self.calendar)
        self.moveChat.clicked.connect(self.move_chat)
        self.mainHome.clicked.connect(self.main_home)
        self.mainHome_2.clicked.connect(self.main_home)
        self.mainHome_3.clicked.connect(self.main_home)
        self.mainHome_4.clicked.connect(self.main_home)
        self.moveAtten.clicked.connect(self.move_atten)
        self.sCalendar.clicked[QtCore.QDate].connect(self.show_task)
        self.studentAddTask.clicked.connect(self.add_task)
        self.attenButton.clicked.connect(self.atten)
        self.outingButton.clicked.connect(self.outing)
        self.sendMessage.clicked.connect(self.messaging)
        self.chat.clicked.connect(self.send_chat)
        self.chatLog.clicked.connect(self.show_chat)

    def log_out(self):
        self.parent().setCurrentIndex(0)

    def move_message(self):
        self.studentStack.setCurrentIndex(1)

    def calendar(self):
        self.studentStack.setCurrentIndex(3)

    def move_chat(self):
        self.studentStack.setCurrentIndex(2)

    def main_home(self):
        self.studentStack.setCurrentIndex(0)

    def move_atten(self):
        self.studentStack.setCurrentIndex(4)

    def show_task(self):
        date = self.sCalendar.selectedDate()
        self.curs.execute("select taskname, task from hrd.tasks where taskdate = '%s'" % date.toString('yyyy-MM-dd'))
        tasks = self.curs.fetchall()
        self.sTasks.clear()
        for task in tasks:
            self.sTasks.append("%s : %s" % task)

    def add_task(self):
        date = self.sCalendar.selectedDate()
        self.curs.execute("insert into hrd.tasks (taskdate, taskname, task) values ('%s', '%s', '%s')" %
                          (date.toString('yyyy-MM-dd'), self.taskName.text(), self.task.text()))
        self.conn.commit()
        self.curs.execute("select taskname, task from hrd.tasks where taskdate = '%s'" % date.toString('yyyy-MM-dd'))
        tasks = self.curs.fetchall()
        self.sTasks.clear()
        for task in tasks:
            self.sTasks.append("%s : %s" % task)

    def atten(self):
        if self.attenButton.text() == '입실':
            self.now = datetime.now()
            self.curs.execute("update hrd.students set intime = '%d : %d' where name = '%s'" %
                              (self.now.hour, self.now.minute, self.user))
            self.conn.commit()
            self.attenTime.setText('%d : %d' % (self.now.hour, self.now.minute))
            self.curs.execute("update hrd.students set outing = '수강중' where name = '%s'" % self.user)
            self.conn.commit()
            self.attenButton.setText("퇴실")
        elif self.attenButton.text() == '퇴실':
            self.curs.execute("update hrd.students set outtime = '%d : %d' where name = '%s'" %
                              (self.now.hour, self.now.minute, self.user))
            self.conn.commit()
            self.backTime.setText('%d : %d' % (self.now.hour, self.now.minute))
            self.curs.execute("update hrd.students set outing = '수강 완료' where name = '%s'" % self.user)
            self.conn.commit()
            self.attenButton.setText("입실")
        else:
            pass
        if self.attenTime.text() != '__ : __' and self.backTime.text() != '__ : __':
            self.attenButton.setText("퇴실 완료")
        else:
            pass

    def outing(self):
        if self.outingButton.text() == '외출':
            self.curs.execute("update hrd.students set outing = '외출 중' where name = '%s'" % self.user)
            self.conn.commit()
            self.outingButton.setText("외출 복귀")
        else:
            self.curs.execute("update hrd.students set outing = '복귀 완료' where name = '%s'" % self.user)
            self.conn.commit()
            self.outingButton.setText("복귀 완료")

    def messaging(self):
        self.curs.execute("insert into hrd.messages (name, sendto, message, checked) values ('%s', '%s', '%s', %d)" %
                          (self.studentName.text(), self.teacherSet.currentText(), self.message.toPlainText(), 1))
        self.conn.commit()
        QMessageBox.information(self, '성공', '%s 교수님에게 메시지를 보냈습니다.' % self.teacherSet.currentText())
        self.curs.execute("select count(checked) from hrd.messages where checked = 1 and sendto = '%s'" %
                          self.teacherSet.currentText())
        alarm_m = self.curs.fetchall()
        teacher.messageA.setText(str(alarm_m[0][0]))
        teacher2.messageA.setText(str(alarm_m[0][0]))

    def send_chat(self):
        self.conn = pymysql.connect(host='127.0.0.1', user='root', password='486486', db='hrd')
        self.curs = self.conn.cursor()
        self.curs.execute("insert into hrd.chats (student, teacher, chat, checked) values ('%s', '%s', '%s : %s', %d)" %
                          (self.studentName.text(), self.teacherSet_2.currentText(),
                           self.studentName.text(), self.chatText.text(), 1))
        self.conn.commit()
        self.show_chat()
        teacher.show_chat()
        teacher2.show_chat()

    def show_chat(self):
        self.chatting.clear()
        self.conn = pymysql.connect(host='127.0.0.1', user='root', password='486486', db='hrd')
        self.curs = self.conn.cursor()
        self.curs.execute("select chat from hrd.chats where student = '%s' and teacher = '%s'" %
                          (self.studentName.text(), self.teacherSet_2.currentText()))
        chats = self.curs.fetchall()
        for chat in chats:
            self.chatting.append(chat[0])


class TeacherWidget(QWidget, teacher_form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.teacherStack.setCurrentIndex(0)
        self.conn = pymysql.connect(host='127.0.0.1', user='root', password='486486', db='hrd')
        self.curs = self.conn.cursor()
        self.user = ''
        self.now = datetime.now()
        self.todayDate.setText(str(self.now.date()))
        self.logoutButton.clicked.connect(self.log_out)
        self.moveCalendar.clicked.connect(self.calendar)
        self.moveMessage.clicked.connect(self.message)
        self.moveChat.clicked.connect(self.move_chat)
        self.mainHome.clicked.connect(self.main_home)
        self.mainHome_2.clicked.connect(self.main_home)
        self.mainHome_3.clicked.connect(self.main_home)
        self.mainHome_4.clicked.connect(self.main_home)
        self.tCalendar.clicked[QtCore.QDate].connect(self.show_task)
        self.teacherAddTask.clicked.connect(self.add_task)
        self.moveAtten.clicked.connect(self.atten)
        self.studentsButton.clicked.connect(self.show_atten)
        self.showMessage.clicked.connect(self.show_message)
        self.chat.clicked.connect(self.send_chat)
        self.chatLog.clicked.connect(self.show_chat)

    def log_out(self):
        self.parent().setCurrentIndex(0)

    def calendar(self):
        self.teacherStack.setCurrentIndex(3)

    def message(self):
        self.teacherStack.setCurrentIndex(1)

    def move_chat(self):
        self.teacherStack.setCurrentIndex(2)

    def main_home(self):
        self.teacherStack.setCurrentIndex(0)

    def atten(self):
        self.teacherStack.setCurrentIndex(4)

    def show_task(self):
        self.conn = pymysql.connect(host='127.0.0.1', user='root', password='486486', db='hrd')
        self.curs = self.conn.cursor()
        date = self.tCalendar.selectedDate()
        self.curs.execute("select taskname, task from hrd.tasks where taskdate = '%s'" % date.toString('yyyy-MM-dd'))
        tasks = self.curs.fetchall()
        self.tTasks.clear()
        for task in tasks:
            self.tTasks.append("%s : %s" % task)

    def add_task(self):
        date = self.tCalendar.selectedDate()
        self.curs.execute("insert into hrd.tasks (taskdate, taskname, task) values ('%s', '%s', '%s')" %
                          (date.toString('yyyy-MM-dd'), self.taskName.text(), self.task.text()))
        self.conn.commit()
        self.curs.execute("select taskname, task from hrd.tasks where taskdate = '%s'" % date.toString('yyyy-MM-dd'))
        tasks = self.curs.fetchall()
        self.tTasks.clear()
        for task in tasks:
            self.tTasks.append("%s : %s" % task)

    def show_atten(self):
        self.conn = pymysql.connect(host='127.0.0.1', user='root', password='486486', db='hrd')
        self.curs = self.conn.cursor()
        self.curs.execute("select * from hrd.students")
        students_t = self.curs.fetchall()
        students_l = []
        for row in students_t:
            students_l.append(list(row))
        for i in range(len(students_l)):
            for j in range(len(students_l[i])):
                self.students.setItem(i, j, QTableWidgetItem(students_l[i][j]))

    def show_message(self):
        self.conn = pymysql.connect(host='127.0.0.1', user='root', password='486486', db='hrd')
        self.curs = self.conn.cursor()
        self.messages.clear()
        self.curs.execute("select name, message from hrd.messages where sendto = '%s' and checked = 1" %
                          self.teacherName.text())
        messages = self.curs.fetchall()
        for m in messages:
            self.messages.append("%s : %s" % (m[0], m[1]))
        self.curs.execute("update hrd.messages set checked = 0 where sendto = '%s'" % self.teacherName.text())
        self.conn.commit()
        self.curs.execute("select count(checked) from hrd.messages where checked = 1 and sendto = '%s'" %
                          self.teacherName.text())
        alarm_m = self.curs.fetchall()
        self.messageA.setText(str(alarm_m[0][0]))

    def send_chat(self):
        self.conn = pymysql.connect(host='127.0.0.1', user='root', password='486486', db='hrd')
        self.curs = self.conn.cursor()
        self.curs.execute("insert into hrd.chats (student, teacher, chat, checked) values ('%s', '%s', '%s : %s', %d)" %
                          (self.studentSet.currentText(), self.teacherName.text(),
                           self.teacherName.text(), self.chatText.text(), 1))
        self.conn.commit()
        self.show_chat()
        student.show_chat()
        student2.show_chat()

    def show_chat(self):
        self.chatting.clear()
        self.conn = pymysql.connect(host='127.0.0.1', user='root', password='486486', db='hrd')
        self.curs = self.conn.cursor()
        self.curs.execute("select chat from hrd.chats where student = '%s' and teacher = '%s'" %
                          (self.studentSet.currentText(), self.teacherName.text()))
        chats = self.curs.fetchall()
        for chat in chats:
            self.chatting.append(chat[0])


# index 0 = 메인, index 1 = 회원가입, index 2 = 로그인
# index 3 = 학생 프로그램, index 4 = 선생 프로그램
if __name__ == "__main__":
    # 이따구로 하면 안되겠지
    app = QApplication(sys.argv)

    stack = QtWidgets.QStackedWidget()
    main = MainWidget()
    join = JoinWidget()
    login = LoginWidget()
    student = StudentWidget()
    teacher = TeacherWidget()

    stack2 = QtWidgets.QStackedWidget()
    main2 = MainWidget()
    join2 = JoinWidget()
    login2 = LoginWidget()
    student2 = StudentWidget()
    teacher2 = TeacherWidget()

    stack.addWidget(main)
    stack.addWidget(join)
    stack.addWidget(login)
    stack.addWidget(student)
    stack.addWidget(teacher)
    stack.setFixedWidth(450)
    stack.setFixedHeight(850)

    stack2.addWidget(main2)
    stack2.addWidget(join2)
    stack2.addWidget(login2)
    stack2.addWidget(student2)
    stack2.addWidget(teacher2)
    stack2.setFixedWidth(450)
    stack2.setFixedHeight(850)

    stack.show()
    stack2.show()

    app.exec_()
