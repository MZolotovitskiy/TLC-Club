import smtplib

server = 'smtp.yandex.ru'
user = 'Bevqnt@ya.ru'
password = '1625341357'

recipients = ['bevqntb@gmail.ru']
subject = 'Тема сообщения 213213 777'
text_test = 'Test Text 123 <b>aaa</b>'
html = '<html><head></head><body><p>' + text_test + '</p></body></html>'

mail = smtplib.SMTP_SSL(server)
mail.login(user, password)
mail.sendmail(user, recipients, html)
mail.quit()
