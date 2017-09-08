import os
import smtplib
from smtplib import SMTPException
import ConfigParser

class MailService(object):
    """
    Used for sending out emails to clients
    """

    def __init__(self):
        config = ConfigParser.ConfigParser()
        config.read(os.path.realpath('config'))
        self.mailbox_username = config.get("mail", "username")
        self.mailbox_password = config.get("mail", "password")

    def sendEmailConfirmationEmail(self, username, email, confirm_email_url):

        """
        Sends out an email containing a link for confirming a registered user's email address.
        """
        sender = 'projectreldi@gmail.com'
        receivers = [email]

        message = """From: Project ReLDI <projectreldi@gmail.com>
MIME-Version: 1.0
Content-type: text/plain
To: <{1}>
Subject: Confirm your email address

Hello {0},

please click the following link to confirm your email address {1}""".format(username, confirm_email_url)

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.ehlo()
            server.starttls()
            server.login(self.mailbox_username, self.mailbox_password)
            server.sendmail(sender, receivers, message)
            server.close()
        except SMTPException:
            print "Error: unable to send email"

    def sendAccessRequestEmail(self, username, note, login_link):

        """
        Sends out an email to the administrator containing a client's request for accessing the API.
        """
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
            server.login(self.mailbox_username, self.mailbox_password)
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
            server.login(self.mailbox_username, self.mailbox_password)
            server.sendmail(sender, receivers, message)
            server.close()
        except SMTPException:
            print "Error: unable to send email"


    def sendUserReactivatedEmail(self, username, email, login_url):

        """
        Sends out an email to the user once their account has been reactivated
        """
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
            server.login(self.mailbox_username, self.mailbox_password)
            server.sendmail(sender, receivers, message)
            server.close()
        except SMTPException:
            print "Error: unable to send email"

    def sendUserBlockedEmail(self, username, email):

        """
        Sends out an email to the user once their account has been blocked.
        """
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
            server.login(self.mailbox_username, self.mailbox_password)
            server.sendmail(sender, receivers, message)
            server.close()
        except SMTPException:
            print "Error: unable to send email"

    def sendEmailForgotPasswordEmail(self, username, email, forgot_password_email_url):

        """
        Sends out an email containing a password reset link
        """
        sender = 'projectreldi@gmail.com'
        receivers = [email]

        message = """From: Project ReLDI <projectreldi@gmail.com>
MIME-Version: 1.0
Content-type: text/plain
To: <{1}>
Subject: Reset your password

Hello {0},

please click the following link to confirm your password reset {1}""".format(username, forgot_password_email_url)

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.ehlo()
            server.starttls()
            server.login(self.mailbox_username, self.mailbox_password)
            server.sendmail(sender, receivers, message)
            server.close()
        except SMTPException:
            print "Error: unable to send email"
