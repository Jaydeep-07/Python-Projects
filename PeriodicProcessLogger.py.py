
import psutil
import sys
import os
import datetime
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import urllib.request as urllib2


def is_connected():
    try:
        urllib2.urlopen('http://216.58.192.142', timeout=1)
        return True
    except urllib2.URLError as err:
        return False


def MailSendWithAttachment(file1, receiver):
    fromaddr = "jaydeepvpatil225@gmail.com"
    toaddr = receiver

    # instance of MIMEMultipart
    msg = MIMEMultipart()

    # storing the senders email address
    msg['From'] = fromaddr

    # storing the receivers email address
    msg['To'] = toaddr

    # storing the subject
    msg['Subject'] = "Running Process"

    # string to store the body of the mail
    body = "Names Of Running Process"

    # attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))

    # open the file to be sent
    filename = file1
    attachment = open(filename, "rb")

    # instance of MIMEBase and named as p
    p = MIMEBase('application', 'octet-stream')

    # To change the payload into encoded form
    p.set_payload((attachment).read())

    # encode into base64
    encoders.encode_base64(p)

    filename = os.path.split(str(filename))

    p.add_header('Content-Disposition', "attachment; filename= %s" % filename[1])

    # attach the instance 'p' to instance 'msg'
    msg.attach(p)

    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # start TLS for security
    s.starttls()

    # Authentication
    s.login(fromaddr, "Sender Password")

    # Converts the Multipart msg into a string
    text = msg.as_string()

    # sending the mail
    s.sendmail(fromaddr, toaddr, text)

    # terminating the session
    print("mail Send ")
    s.quit()


def ProcessInformation():
    listProcess = []

    for proc in psutil.process_iter():
        try:
            pinfo = proc.as_dict(attrs=['pid', 'name', 'username'])
            listProcess.append(pinfo)
        except Exception:
            pass
    return listProcess


def main():
    if len(sys.argv) > 3:
        print("Invalid Number of Arguments !")
        print("Please use -h Or -u for help and usage")
        exit()
    if sys.argv[1].lower() == "-h":
        print("This Script Is Used for Finding The Running Process And Store in log File ");
        print("To Run The Script use Following Command")
        print("Example :")
        print("python Filename FolderName EmailOFReceiver")
        print("python ProcessInfoMail.py Demo Abc@gmail.com")
        exit()
    if sys.argv[1].lower() == "-u":
        print("This Script Is Used for Finding The Running Process And Store in log File")
        exit()

    Directoryname = sys.argv[1]
    Receiver = sys.argv[2]
    isDir = os.path.isfile(Directoryname)
    if isDir == True:
        print("It Is File  Please Enter Directory Name !!!")
        exit()

    DirExits = os.path.exists(Directoryname)

    if DirExits == False:
        os.mkdir(Directoryname)

    flag = os.path.isabs(Directoryname)
    if flag == False:
        Directoryname = os.path.abspath(Directoryname)

    isDir = os.path.isfile(Directoryname)
    if isDir == True:
        print("It Is File  Please Enter Directory Name !!!")
        exit()

    filename = os.path.join(Directoryname,
                            "ProcessLog%s.txt" % datetime.datetime.now().strftime("%d-%m-%Y_%I-%M-%S_%p"))

    line = "_" * 60
    fobj = open(filename, "w")

    fobj.write(line + "\n")
    fobj.write("Running Process at :")
    fobj.write(time.ctime())
    fobj.write(line + "\n")

    listProc = ProcessInformation()
    for element in listProc:
        fobj.write("%s\n"%element)
    fobj.close()
    connected = is_connected()
    if connected:

        pass
        MailSendWithAttachment(filename, Receiver)
    else:
        print("There Is No InterNet Connection")



if __name__ == "__main__":
    main()
