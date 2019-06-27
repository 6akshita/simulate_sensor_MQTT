

import smtplib

def send_alert_email(msg):
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    # Authentication
    s.login("username", "password")
    # sending the mail
    s.sendmail("from_user_email_address", "to_user_email_address", msg)
    # terminating the session
    s.quit()
