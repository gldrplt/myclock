########################################
#
#   sendemail.py
#
#   send email to gldrplt@gmail.com
#
########################################
import smtplib

def sendmail(sender, receiver, subject, msg ):

    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # start TLS for security
    s.starttls()

    # Authentication
    senderid = "gldrplt@gmail.com"
    senderpw = "wegrxeuliqnfwvat"
    s.login(senderid, senderpw)

    # message to be sent
    # message = f"""\
    # Subject: {subject}
    # To: {receiver}
    # From: {sender}

    # ---- test msg ---


    # {msg}

    # from {sender}
    # """

    # alternate message
    message='To: '+receiver +'\n'\
           +'From: '+sender+'\n' \
           +'Subject: '+subject+'\n\n' \
           +msg

    # sending the mail
    s.sendmail(sender, receiver, message)

    # terminate smtp session
    s.quit()
pass
################################
#
#   start of program
#
################################
if __name__ == '__main__':
    sender = "myclock.py"
    receiver = "gldrplt@gmail.com"
    subject = "Test sending email from python program"
#    msg = "Program is sending this is a test \n message line 2\n\nmessage sent from sendemail.py"
    msg = "the rain in spain"
    sendmail(sender, receiver, subject, msg)

    print("sendemail.py sent email")





    