from django.conf import settings
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.core.mail import EmailMessage
from django.template.loader import get_template,render_to_string
from django.contrib.auth.decorators import login_required
import socket

def send_email(subject,to_mail,message,tmp_url):
    flag = ''
    try:
        # connect to the host -- tells us if the host is actually
        # reachable
        socket.create_connection(("1.1.1.1", 53))
        flag='net_on'
    except OSError:
        flag='net_off'

    e_tmp = tmp_url
    c = {
            
            'msg':message
        }
    content = render_to_string(e_tmp,c)
    img_data = open('static/email_img/logo_2.png', 'rb').read()
    html_part = MIMEMultipart(_subtype='related')
    body = MIMEText(content, _subtype='html')
    html_part.attach(body)
    # Now create the MIME container for the image
    img = MIMEImage(img_data, 'png')
    img.add_header('Content-Id', '<myimage>')  # angle brackets are important
    img_data2 = open('static/email_img/logo_small.jpg', 'rb').read()
    img2 = MIMEImage(img_data2, 'jpg')
    img2.add_header('Content-Id', '<myimage2>')  # angle brackets are important
    # img.add_header("Content-Disposition", "inline", filename="myimage") # David Hess recommended this edit
    html_part.attach(img)
    html_part.attach(img2)
    msg = EmailMessage(subject, None,  settings.EMAIL_HOST_USER,  [to_mail])
    msg.attach(html_part) # Attach the raw MIMEBase descendant. This is a public method on EmailMessage
    if flag == 'net_on':
        msg.send()
    else:
        print('network is not on')


def send_email_manager(subject,message,tmp_url,name):
    flag = ''
    try:
        # connect to the host -- tells us if the host is actually
        # reachable
        socket.create_connection(("1.1.1.1", 53))
        flag='net_on'
    except OSError:
        flag='net_off'

    e_tmp = tmp_url
    c = {
            'name':name,
            'msg':message
        }
    content = render_to_string(e_tmp,c)
    img_data = open('static/email_img/logo_2.png', 'rb').read()
    html_part = MIMEMultipart(_subtype='related')
    body = MIMEText(content, _subtype='html')
    html_part.attach(body)
    # Now create the MIME container for the image
    img = MIMEImage(img_data, 'png')
    img.add_header('Content-Id', '<myimage>')  # angle brackets are important
    img_data2 = open('static/email_img/logo_small.jpg', 'rb').read()
    img2 = MIMEImage(img_data2, 'jpg')
    img2.add_header('Content-Id', '<myimage2>')  # angle brackets are important
    # img.add_header("Content-Disposition", "inline", filename="myimage") # David Hess recommended this edit
    html_part.attach(img)
    html_part.attach(img2)
    msg = EmailMessage(subject, None,  settings.EMAIL_HOST_USER,  [settings.EMAIL_HOST_USER])
    msg.attach(html_part) # Attach the raw MIMEBase descendant. This is a public method on EmailMessage
    if flag == 'net_on':
        msg.send()
    else:
        print('network is not on')