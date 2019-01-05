import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

# Email you want to send the update from (only works with gmail)
fromEmail = '******'
fromEmailPassword = '******'

# Email you want to send the update to
toEmail = '******'


def send_email(image):
    msg_root = MIMEMultipart('related')
    msg_root['Subject'] = 'Security Update'
    msg_root['From'] = fromEmail
    msg_root['To'] = toEmail
    msg_root.preamble = 'Raspberry pi security camera update'

    msg_alternative = MIMEMultipart('alternative')
    msg_root.attach(msg_alternative)
    msg_text = MIMEText('Smart security cam found object')
    msg_alternative.attach(msg_text)

    msg_text = MIMEText('<img src="cid:image1">', 'html')
    msg_alternative.attach(msg_text)

    msg_image = MIMEImage(image)
    msg_image.add_header('Content-ID', '<image1>')
    msg_root.attach(msg_image)

    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.starttls()
    smtp.login(fromEmail, fromEmailPassword)
    smtp.sendmail(fromEmail, toEmail, msg_root.as_string())
    smtp.quit()
