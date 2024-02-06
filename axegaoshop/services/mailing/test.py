import smtplib

from string import Template

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


s = smtplib.SMTP_SSL(host="mail.vulpine.email", port=465)


s.login("loftsoft@vulpine.email", "#,31,ellEYm")

msg = MIMEMultipart()  # create a message

# add in the actual person name to the message template
message = "Hello dude"

# setup the parameters of the message
msg['From'] = "loftsoft@vulpine.email"
msg['To'] = "homycoder@gmail.com"
msg['Subject'] = "This is TEST"

# add in the message body
msg.attach(MIMEText(message, 'plain'))

# send the message via the server set up earlier.
s.send_message(msg)

