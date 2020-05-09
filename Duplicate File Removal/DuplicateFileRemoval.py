import time
import os
import sys
import hashlib
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import schedule


def MailSendWithAttachment(file1,receiver):
    fromaddr = "jaydeepvpatil225@gmail.com"
    toaddr =receiver

    # instance of MIMEMultipart
    msg = MIMEMultipart()

    # storing the senders email address
    msg['From'] = fromaddr

    # storing the receivers email address
    msg['To'] = toaddr

    # storing the subject
    msg['Subject'] = "Duplicates Files"

    # string to store the body of the mail
    body = "Duplicate Files Detector"

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

    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    # attach the instance 'p' to instance 'msg'
    msg.attach(p)

    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # start TLS for security
    s.starttls()

    # Authentication
    s.login(fromaddr, "sender pswd")

    # Converts the Multipart msg into a string
    text = msg.as_string()

    # sending the mail
    s.sendmail(fromaddr, toaddr, text)

    # terminating the session
    print("mail Send ")
    s.quit()


def hashFile(path, blocksize=1024):
    afile = open(path, 'rb')
    hasher = hashlib.md5()
    buf = afile.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(blocksize)
    afile.close()
    return hasher.hexdigest()

def DeleteFiles(Dict1):
    DuplicateFiles1 = []
    DuplicatesFileCounter = 0
    results = list(filter(lambda x: len(x) > 1, Dict1.values()))
    if len(results) > 0:
        for result in results:
            icnt = 0
            for subresult in result:
                icnt += 1
                if icnt >= 2:
                    DuplicatesFileCounter += 1
                    DuplicateFiles1.append(subresult)
                    print(subresult)
                    os.remove(subresult)

    else:
        print("No Duplicates Found")
    return DuplicateFiles1,DuplicatesFileCounter


def DuplicateFiles(Directoryname):
    dups = {}
    for Folder, SubFolders, Files in os.walk(Directoryname):
        print(Folder)
        for file in Files:
            path = os.path.join(Folder, file)
            File_hash = hashFile(path)
            if File_hash in dups:
                dups[File_hash].append(path)
            else:
                dups[File_hash] = [path]

    return dups


def DuplicatesFilesWithMail(Dir,Receiver):
    dir2 = "Marvellous"
    filename = os.path.join(dir2, "Log%s.txt" % datetime.datetime.now().strftime("%d-%m-%Y_%I-%M-%S_%p"))
    line = "_" * 60
    fobj = open(filename, "w")

    fobj.write(line + "\n")
    fobj.write("Starting Time Of File Scanning at :")
    fobj.write(time.ctime())
    dups = DuplicateFiles(Dir)
    print("___________________________________________________________")
    DuplicatesFileNames,deletecounter = DeleteFiles(dups)

    fobj.write("\n Total Duplicates Files Are :" + str(deletecounter))

    fobj.write("\nDeleted Duplicate Files Are !!!!!!")
    fobj.write("\n" + line)

    if len(DuplicatesFileNames) > 0:
        for i in DuplicatesFileNames:
            fobj.write("\n" + i + "\n")
    else:
        fobj.write("\nNo Duplicates File Found")
    fobj.close()
    MailSendWithAttachment(filename,Receiver)


def main():
    print("This Script Is Used For Delete  Duplicates File from The Directory And Send Mail Of the Deleted Duplicate "
          "Files")
    if (len(sys.argv) > 4):
        print("Invalid Number Of Arguments ")
        print("Please use -h or -u for help and usage ");
        exit()
    if sys.argv[1].lower() == "-h":
        print("This Script Is Used For Delete  Duplicates File from The Directory And Send Mail Of the Deleted "
              "Duplicate Files ");
        print("Example :")
        print("python Filename Folder1 Timeinterval EmailOfReceiver")
        print("python DuplicateFileRemoval.py Demo 5 abc@gmail.com")
        print("DuplicateFileRemoval.py : Name Of The file")
        print("Demo : Name of the Folder ")
        print("5 : time interval in minutes")
        print("abc@gmail.com : Email Id OF the Receiver to Send the Mail OF Deleted File")
        exit()
    if sys.argv[1].lower() == "-u":
        print("This Script Is Used For Delete  Duplicates File from The Directory And Send Mail Of the Deleted "
              "Duplicate Files ")
        exit()

    Directoryname = sys.argv[1]
    flag = os.path.isabs(Directoryname)
    if flag == False:
        Directoryname = os.path.abspath(Directoryname)

    isDir = os.path.isfile(Directoryname)
    if isDir == True:
        print("It Is File  Please Enter Directory Name !!!")
        exit()

    DirExits = os.path.exists(Directoryname)
    if DirExits == False:
        print("Directory ", Directoryname, "Does Not Exits  ")
        exit()

    schedule.every(int(sys.argv[2])).minutes.do(DuplicatesFilesWithMail,Dir=Directoryname,Receiver=sys.argv[3])
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
