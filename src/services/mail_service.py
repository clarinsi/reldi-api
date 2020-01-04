import smtplib
from smtplib import SMTPException
from email.mime.text import MIMEText
from ..helpers import config


class MailService(object):
    """
    Used for sending out emails to clients
    """

    def __init__(self):
        self.mailbox_username = config.get("mail", "username")
        self.mailbox_password = config.get("mail", "password")

    def sendEmailConfirmationEmail(self, username, email, confirm_email_url):

        """
        Sends out an email containing a link for confirming a registered user's email address.
        """
        sender = 'Project ReLDI <noreply@cl-services.ijs.si>'
        receiver = email
        subject = "Confirm your email address"
        text = ("Hello {0},\n\n" +
                "please click the following link to confirm your email address {1}").format(username, confirm_email_url)

        self.send(self.create_message(sender, receiver, subject, text))

    def sendAccessRequestEmail(self, username, note, login_link):

        """
        Sends out an email to the administrator containing a client's request for accessing the API.
        """
        sender = 'Project ReLDI <noreply@cl-services.ijs.si>'
        receiver = 'nljubesi@gmail.com'
        subject = "New ReLDI user"
        if note != "":
            note = "The following note has been left by the user: {0}".format(note)

        text = ("A new user with the username *{0}* has requested access.\n" +
                "Click the link to log in and review the user details: {2}\n\n" +
                "{1}").format(username, note, login_link)

        self.send(self.create_message(sender, receiver, subject, text))

    def sendUserActivatedEmail(self, username, email, login_url):

        sender = 'Project ReLDI <noreply@cl-services.ijs.si>'
        receiver = email
        subject = "Your ReLDI account has been activated"
        text = ("Hello {0},\n\n" +
                "your ReLDI account has been activated.\n\n" +
                "Click the link to go to the login page: {2}").format(username, email, login_url)

        self.send(self.create_message(sender, receiver, subject, text))

    def sendUserReactivatedEmail(self, username, email, login_url):

        """
        Sends out an email to the user once their account has been reactivated
        """
        sender = 'Project ReLDI <noreply@cl-services.ijs.si>'
        receiver = email
        subject = "Your ReLDI account has been re-activated"
        text = ("Hello {0},\n\n" +
                "your ReLDI account has been re-activated.\n\n" +
                "Click the link to go to the login page: {2}").format(username, email, login_url)

        self.send(self.create_message(sender, receiver, subject, text))

    def sendUserBlockedEmail(self, username, email):

        """
        Sends out an email to the user once their account has been blocked.
        """
        sender = 'Project ReLDI <noreply@cl-services.ijs.si>'
        receiver = email
        subject = "Your ReLDI account has been blocked"
        text = ("Hello {0},\n\n" +
                "your ReLDI account has been blocked by the administrator.").format(username, email)

        self.send(self.create_message(sender, receiver, subject, text))

    def sendEmailForgotPasswordEmail(self, username, email, forgot_password_email_url):

        """
        Sends out an email containing a password reset link
        """
        sender = 'Project ReLDI <noreply@cl-services.ijs.si>'
        receiver = email
        subject = "Reset your password"
        text = ("Hello {0},\n\n" +
                "please click the following link to confirm your password reset {1}").format(username, forgot_password_email_url)

        self.send(self.create_message(sender, receiver, subject, text))

    @staticmethod
    def send(message):
        try:
            server = smtplib.SMTP('localhost')
            server.sendmail(message['From'], message['To'], message.as_string())
        except SMTPException, e:
            print "Error: unable to send email " + str(e)
        finally:
            server.quit()

    @staticmethod
    def create_message(sender, receiver, subject, text):
        msg = MIMEText(text)
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = receiver
        return msg
