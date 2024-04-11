from django.core.mail import EmailMessage
import os

class Utils(object):
    @staticmethod
    def send_mail(data):
        email = EmailMessage(subject= data['subject'],
        body=data['body'],
        from_email=os.environ.get['EMAIL_FORM'],
        to_email=data['to_email']
        )
        email.send()
# this is from the document this is format 