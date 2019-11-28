import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic
import smtplib
import sqlite3
from datetime import datetime


conn = sqlite3.connect('EntryRecords.db')


class MainWindow(QMainWindow,QWidget):
    def __init__(self):
        super().__init__()

        self.InitUi()
        pass
    def InitUi(self):
        uic.loadUi('mainUI.ui', self)
        self.setWindowTitle('Entry Management')
        self.setWindowIcon(QIcon('usermale.png'))

        self.register_new.clicked.connect(self.showForm)
        self.checkOutBut.clicked.connect(self.check_out_clicked)
        self.actionExit_2.triggered.connect(self.exitApp)
        self.statusbar.showMessage("Enable this for your gmail: https://myaccount.google.com/lesssecureapps")



        self.show()
    def exitApp(self):
        self.close()
    def showForm(self):
        self.EMAIL_ADDRESS = str(self.email_edit.text())
        self.PASSWORD = str(self.pass_edit.text())

        if self.EMAIL_ADDRESS =="" or self.PASSWORD =="":
            msg = QMessageBox()
            msg.about(self,"Error","Please Enter Your Gmail Id and password to get started")
            return
        self.x = startForm()

    def check_out_clicked(self):
        self.EMAIL_ADDRESS = str(self.email_edit.text())
        self.PASSWORD = str(self.pass_edit.text())
        if self.EMAIL_ADDRESS =="" or self.PASSWORD =="":
            msg = QMessageBox()
            msg.about(self,"Error","Please Enter Your Gmail Id and password to get started")
            return
        self.y = checkOutWindow()

class checkOutWindow(QDialog):
    def __init__(self):
        super().__init__()

        self.setCOui()
    def setCOui(self):

        uic.loadUi('checkOut.ui',self)
        self.setWindowTitle("Check Out")
        self.setWindowIcon(QIcon('left.png'))
        self.get_max_id()

        self.coButton.clicked.connect(self.checkOutClicked)
        self.show()
    def get_max_id(self):
        self.id = DBobj.get_id()
        self.last_ch_id.setText(str(self.id))

    def checkOutClicked(self):
        details = DBobj.getVisitorDetails(self.id)

        now = datetime.now()
        current_time = str(now.strftime("%H:%M:%S"))
        subject = "Thank you for visiting us!"
        msg = "Your details: \n Name: "+details[0]+"\n Phone :"+details[1]+"\n Checkin time: "+details[2]+"\n Check out time:"+current_time+"\n Host name: "+details[3]
        email = details[4]
        respo = SendMail.send_email(subject,msg,email)


        self.close()


class startForm(QDialog):
    def __init__(self):
        super().__init__()

        self.formUI()
    def formUI(self):

        uic.loadUi('details.ui',self)
        self.setWindowIcon(QIcon('document.png'))
        self.setWindowTitle("Enter the Details")
        self.saveButton.clicked.connect(self.saveClicked)
        self.cancelButton.clicked.connect(self.cancelClicked)

        self.show()


    def saveClicked(self):


        v_name = self.name_edit.text()
        v_phone = self.phone_edit.text()
        v_email = self.email_edit.text()
        h_name = self.name_edit_2.text()
        h_phone = self.phone_edit_2.text()
        h_email = self.email_edit_2.text()
        #print(v_name,v_phone,v_email,h_email,h_name,h_phone)

        DBobj.save_to_db(v_name,v_phone,v_email,h_name,h_phone,h_email)
        self.close()
        self.sendMailToHost(v_name,v_phone,v_email,h_email)
    def cancelClicked(self):
        self.close()


    def sendMailToHost(self,v1,v2,v3,h_email):
        subject = " You have a visitor!"
        msg = "Name : "+v1+"\n"+ "Phone :"+v2+"\nEmail :" +v3
        SendMail.send_email(subject,msg,h_email)







class SendMail:
    def __init__(self):
        pass

    @staticmethod
    def send_email(subject, msg, h_email, self=None):

        try:

            #global EMAIL_ADDRESS,PASSWORD

            EMAIL_ADDRESS = mainWin.EMAIL_ADDRESS
            PASSWORD = mainWin.PASSWORD
            server = smtplib.SMTP('smtp.gmail.com:587')
            server.ehlo()
            server.starttls()
            server.login(EMAIL_ADDRESS, PASSWORD)
            message = 'Subject: {}\n\n{}'.format(subject, msg)
            server.sendmail(EMAIL_ADDRESS, h_email, message)
            server.quit()

            print("Success")
            return 1

        except:
            print('Error, Enter correct details')
            return 0



class DBHandler:
    def __init__(self):
        self.c = conn.cursor()

    def save_to_db(self,v1,v2,v3,h1,h2,h3):

        now = datetime.now()
        current_time = str(now.strftime("%H:%M:%S"))


        cmd = 'select max(id) from visits'
        self.c.execute(cmd)
        max_id = self.c.fetchall()
        max_id = max_id[0]
        max_id = int(max_id[0]) +1


        cmd = "insert into visits values (" + str(max_id) +",'" + v1+"'" +",'" + v2+"'"+",'" + v3+"'"+",'" +current_time +"'"+",'" + " "+"'"+",'" + h1+"'"+",'" + h2+"'"+",'" + h3+"')"
        self.c.execute(cmd)
        # self.c.execute('select * from visits')
        # print(self.c.fetchall())
        conn.commit()


#         conn.execute(''' create table visits(id integer,v_name text,v_phone text,v_email text,c_in text,c_out text,h_name text,
# h_phone text,h_email text)''')
#         print('table created')

    def get_id(self):
        self.c.execute("select max(id) from visits")
        self.id = self.c.fetchall()
        max_id = self.id
        max_id = max_id[0]
        max_id = int(max_id[0])

        return  max_id

    def getVisitorDetails(self,v_id):
            print('please wait..sending mail')
            cmd = "select v_name,v_phone,c_in,h_name,v_email from visits where id like "+str(v_id)
            self.c.execute(cmd)
            x = self.c.fetchall()


            return list(x[0])
DBobj = DBHandler()
smobj=SendMail()
app = QApplication(sys.argv)
mainWin = MainWindow()

sys.exit(app.exec())


