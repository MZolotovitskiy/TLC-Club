import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from random import randrange

server = 'smtp.yandex.ru'
user = 'tlc.club@ya.ru'
password = 'ubwvlzqvqnvujupz'


def send_email(recipient, subject, text):
    html = '<html><head></head><body><p>' + text + '</p></body></html>'

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = 'TLC-Club <' + user + '>'
    msg['To'] = recipient
    msg['Reply-To'] = user
    msg['Return-Path'] = user
    msg['X-Mailer'] = 'Python'

    part_text = MIMEText(text, 'plain')
    part_html = MIMEText(html, 'html')

    msg.attach(part_text)
    msg.attach(part_html)

    # print(msg.as_string())

    mail = smtplib.SMTP_SSL(server)
    mail.login(user, password)
    mail.sendmail(user, recipient, msg.as_string())
    mail.quit()


class EMailText:
    def __init__(self):
        self.text_registration = '''<p>Спасибо за регистрацию на сайте TLC-club!
        Для подтверждения регистрации введите код {} на сайте.</p>

        <p><b>С уважением, команда TLC-Club!</b></p>'''

    def registration(self):
        code = str(randrange(1000, 9999))
        text = self.text_registration.replace('{}', code)
        return text, code
