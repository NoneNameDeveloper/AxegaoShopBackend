import yagmail

#
# def render_template(template_filename, context):
#     with open(template_filename) as file_:
#         template = Template(file_.read())
#     return template.render(context)
#
#
# s = smtplib.SMTP_SSL(host="mail.vulpine.email", port=465)
#

# yagmail.register("loftsoft@vulpine.email", "#,31,ellEYm")
yag = yagmail.SMTP(host="mail.vulpine.email", port=465, user="loftsoft@vulpine.email", password="#,31,ellEYm")

yag.send(
    "homycoder@gmail.com",
    "Subject",
    contents=open("templates/purchase.html").read(),
    prettify_html=False
)
# msg = EmailMessage()  # create a message
#
# # add in the actual person name to the message template
# # message = render_template("templates/purchase.html", {"name": "Shit"})
#
# # setup the parameters of the message
# msg['From'] = "loftsoft@vulpine.email"
# msg['To'] = "homycoder@gmail.com"
# msg['Subject'] = "This is TEST"
#
# msg.set_content(open("templates/purchase.html").read(), subtype="html")
#
# # add in the message body
# # msg.attach(MIMEText(message, 'html'))
#
# # send the message via the server set up earlier.
# s.send_message(msg)
