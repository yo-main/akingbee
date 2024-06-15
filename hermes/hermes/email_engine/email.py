import email

from hermes.constants import SENDER, TO, SUBJECT, CC, BCC


class Email:
    def __init__(self, sender, receiver, subject, body, cc="", bcc=""):
        self.email = email.message.EmailMessage()

        self.email[SENDER] = sender
        self.email[TO] = receiver
        self.email[SUBJECT] = subject
        self.email[CC] = cc
        self.email[BCC] = bcc
        self.email.set_content(body)
