def get_user():
    f = open('/home/DaTo/service/system/base.txt')
    line = f.read(4)
    return line

def get_password():
    f = open('/home/DaTo/service/system/base.txt')
    line = f.readline()
    line = f.read(10)
    return line

def get_token():
    f = open('/home/DaTo/service/system/token.txt')
    line = f.readline()
    return line
def get_mail():
    f = open('/home/DaTo/service/system/mail.txt')
    line = f.readline()
    return line
def get_mail_password():
    f = open('/home/DaTo/service/system/mail_password.txt')
    line = f.readline()
    return line