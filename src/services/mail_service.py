import smtplib
import mandrill
from smtplib import SMTPException


class MailService(object):

    MANDRILL_KEY = 'zbtMhO3YBEppH8OzqB528A'

    def __init__(self):
        self.client = mandrill.Mandrill(MailService.MANDRILL_KEY)

    def sendAccessRequestEmail(self, username, note, login_link):

        sender = 'projectreldi@gmail.com'
        receivers = ['projectreldi@gmail.com']

        if note != "":
            note = "The following note has been left by the user: {0}".format(note)

        message = """From: Project ReLDI <projectreldi@gmail.com>
MIME-Version: 1.0
Content-type: text/plain
To: <{0}>
Subject: New ReLDI user

A new user with the username *{0}* has requested access.
Click the link to log in and review the user details: {2}

{1}""".format(username, note, login_link)

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.ehlo()
            server.starttls()
            server.login('projectreldi@gmail.com', 'linguistics1020')
            server.sendmail(sender, receivers, message)
            server.close()
        except SMTPException:
            print "Error: unable to send email"

    def sendUserActivatedEmail(self, username, email, login_url):

        sender = 'projectreldi@gmail.com'
        receivers = [email]

        message = """From: Project ReLDI <projectreldi@gmail.com>
MIME-Version: 1.0
Content-type: text/plain
To: <{1}>
Subject: Your ReLDI account has been activated

Hello {0},

your ReLDI account has been activated.

Click the link to go to the login page: {2}""".format(username, email, login_url)

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.ehlo()
            server.starttls()
            server.login('projectreldi@gmail.com', 'linguistics1020')
            server.sendmail(sender, receivers, message)
            server.close()
        except SMTPException:
            print "Error: unable to send email"


    def sendUserReactivatedEmail(self, username, email, login_url):

        sender = 'projectreldi@gmail.com'
        receivers = [email]

        message = """From: Project ReLDI <projectreldi@gmail.com>
MIME-Version: 1.0
Content-type: text/plain
To: <{1}>
Subject: Your ReLDI account has been activated

Hello {0},

your ReLDI account has been re-activated.

Click the link to go to the login page: {2}""".format(username, email, login_url)

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.ehlo()
            server.starttls()
            server.login('projectreldi@gmail.com', 'linguistics1020')
            server.sendmail(sender, receivers, message)
            server.close()
        except SMTPException:
            print "Error: unable to send email"

    def sendUserBlockedEmail(self, username, email):

        sender = 'projectreldi@gmail.com'
        receivers = [email]

        message = """From: Project ReLDI <projectreldi@gmail.com>
MIME-Version: 1.0
Content-type: text/plain
To: <{1}>
Subject: Your ReLDI account has been blocked

Hello {0},

your ReLDI account has been blocked by the administrator.""".format(username, email)

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.ehlo()
            server.starttls()
            server.login('projectreldi@gmail.com', 'linguistics1020')
            server.sendmail(sender, receivers, message)
            server.close()
        except SMTPException:
            print "Error: unable to send email"