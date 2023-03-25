#!/usr/bin/env python

## ip.py version 4

# email's libraries
import smtplib
import ssl
#options
import argparse
#others
import sys
import traceback
import datetime

from email.mime.text import MIMEText

    

def sendemail(from_addr, to_addr_list, cc_addr_list,
              subject, message, login, password, server, port, attachList):

    msgMIME=MIMEText(message)

    header = 'From: %s\n' % from_addr
    header += "Content-Type: text/plain \n"
    header += "MIME-Version: 1.0 \n"
    header += "Content-Transfer-Encoding: 7bit \n"

    #header += "Mime-Version: 1.0 ";
    #header += "Content-Transfer-Encoding: quoted-printable ";
    header += 'To: %s\n' % ','.join(to_addr_list)
    if len(cc_addr_list) > 0:
        header += 'Cc: %s\n' % ','.join(cc_addr_list)
    header += 'Subject: %s\n\n' % subject
    message = header + message # msgMIME.as_string()

    txtout = 'login:'+login+'\n'
    txtout += 'password:' + password+'\n'
    txtout += 'server:' + server+'\n'
    txtout += 'port:' + port+'\n'
    txtout += '\n'
    txtout += message
    txtout += '\n'
    # Create a secure SSL context
    context = ssl.create_default_context()


    try:
        with smtplib.SMTP_SSL(server, port, context=context) as server:
            server.login(login, password)
            problems = server.sendmail(from_addr, (to_addr_list+cc_addr_list), message)
            server.quit()
        error=0
        if len(problems) > 0:
            errore=3
    except Exception as e:
        error=1
        problems=str(e)
    return error, problems, txtout

parser = argparse.ArgumentParser(description='List of parameters.')
parser.add_argument("-l", "--log", dest="filename_cli",default="",
                  help="write report to FILE", metavar="FILE")
parser.add_argument("-f", "--from", dest="from_email_cli",required=True,
                  help="from (sender) email address")
parser.add_argument("-t", "--to", dest="to_email_cli",required=True,
                  help="to email address(es); e.g.: \"a@b.c\" or \"a@b.c,b@b.c\"")
parser.add_argument("-u", "--subject", dest="subject_cli", default="",
                  help="message subject")
parser.add_argument("-m", "--message", dest="message_cli", default="",
                  help="message body")
parser.add_argument("-s", "--server", dest="server_cli", required=True,
                  help="smtp mail relay, default is localhost:25, e.g. servername[:port]")
parser.add_argument("-a", "--attach", dest="attach_cli", default="",
                  help="file attachment(s) - a list of files to attach has to be comma separated")
parser.add_argument("-c", "--carbon copy", dest="cc_email_cli", default="",
                  help="cc email address(es); e.g.: \"[a@b.c]\" or \"a@b.c,b@b.c\"")
parser.add_argument("-x", "--username", dest="username_cli", required=True,
                  help="username for SMTP authentication")
parser.add_argument("-p", "--password", dest="password_cli", required=True,
                  help="password for SMTP authentication")
parser.add_argument("-v", "--verbose", dest="outverbose", action='store_true', default=False, required=False,
                  help="password for SMTP authentication")

args = parser.parse_args()

toList = args.to_email_cli.split(",")
ccList = args.cc_email_cli.split(",")
attachList_files=args.attach_cli.split(",")
server= args.server_cli.split(":")
smtp_port=25

smtp_server=server[0]
if len(server) == 2:
    smtp_port=server[1]

if len(server) > 2:
    sys.exit(-1)

error, problems, txt = sendemail(
    from_addr    = args.from_email_cli,
    to_addr_list = toList,
    cc_addr_list = ccList,
    subject      = args.subject_cli,
    message      = args.message_cli,
    login        = args.username_cli,
    password     = args.password_cli,
    server       = smtp_server,
    port         = smtp_port,
    attachList   = attachList_files
)

message_to_print = ""

if args.outverbose:
    message_to_print = txt+"\n"

date = str(datetime.datetime.now())
if error>0:
    if error == 1:
        message_to_print += message_to_print + date + "\n" + "ERROR: " + problems +"\n"
    if error != 1:
        message_to_print += message_to_print + date + "\n" + "WARNING: " + problems +"\n"
    print(message_to_print)
    if len(args.filename_cli) > 0:
        file = open(args.filename_cli, "a")
        file.write('date :'+date+'\n'+message_to_print)
        file.close()
if args.outverbose & error == 0:
    print(message_to_print)
    if len(args.filename_cli) > 0:
        file = open(args.filename_cli, "a")
        file.write('date :'+date+'\n'+message_to_print)
        file.close()
sys.exit(error)

