import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email():
    sender_email = "mateus.silva@globaltirh.com.br"
    receiver_email = "LucrilhasBR@hotmail.com"
    password = "qemi brbt hcfz wpia"  # Use uma senha de app, não sua senha real

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = "Assunto do Email"
    
    body = "Este é o corpo do e-mail. Mudei de mensagem"
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, password)
    server.send_message(msg)
    server.quit()

send_email()